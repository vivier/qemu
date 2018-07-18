/*
 * libqos PCI bindings for PC
 *
 * Copyright IBM, Corp. 2012-2013
 *
 * Authors:
 *  Anthony Liguori   <aliguori@us.ibm.com>
 *
 * This work is licensed under the terms of the GNU GPL, version 2 or later.
 * See the COPYING file in the top-level directory.
 */

#include "qemu/osdep.h"
#include "libqtest.h"
#include "libqos/pci-pc.h"
#include "qapi/qmp/qdict.h"
#include "hw/pci/pci_regs.h"

#include "qemu-common.h"


#define ACPI_PCIHP_ADDR         0xae00
#define PCI_EJ_BASE             0x0008

typedef struct QPCIBusPC
{
    QPCIBus bus;
} QPCIBusPC;

static uint8_t qpci_pc_pio_readb(QPCIBus *bus, uint32_t addr)
{
    return inb(addr);
}

static void qpci_pc_pio_writeb(QPCIBus *bus, uint32_t addr, uint8_t val)
{
    outb(addr, val);
}

static uint16_t qpci_pc_pio_readw(QPCIBus *bus, uint32_t addr)
{
    return inw(addr);
}

static void qpci_pc_pio_writew(QPCIBus *bus, uint32_t addr, uint16_t val)
{
    outw(addr, val);
}

static uint32_t qpci_pc_pio_readl(QPCIBus *bus, uint32_t addr)
{
    return inl(addr);
}

static void qpci_pc_pio_writel(QPCIBus *bus, uint32_t addr, uint32_t val)
{
    outl(addr, val);
}

static uint64_t qpci_pc_pio_readq(QPCIBus *bus, uint32_t addr)
{
    return (uint64_t)inl(addr) + ((uint64_t)inl(addr + 4) << 32);
}

static void qpci_pc_pio_writeq(QPCIBus *bus, uint32_t addr, uint64_t val)
{
    outl(addr, val & 0xffffffff);
    outl(addr + 4, val >> 32);
}

static void qpci_pc_memread(QPCIBus *bus, uint32_t addr, void *buf, size_t len)
{
    memread(addr, buf, len);
}

static void qpci_pc_memwrite(QPCIBus *bus, uint32_t addr,
                             const void *buf, size_t len)
{
    memwrite(addr, buf, len);
}

static uint8_t qpci_pc_config_readb(QPCIBus *bus, int devfn, uint8_t offset)
{
    outl(0xcf8, (1U << 31) | (devfn << 8) | offset);
    return inb(0xcfc);
}

static uint16_t qpci_pc_config_readw(QPCIBus *bus, int devfn, uint8_t offset)
{
    outl(0xcf8, (1U << 31) | (devfn << 8) | offset);
    return inw(0xcfc);
}

static uint32_t qpci_pc_config_readl(QPCIBus *bus, int devfn, uint8_t offset)
{
    outl(0xcf8, (1U << 31) | (devfn << 8) | offset);
    return inl(0xcfc);
}

static void qpci_pc_config_writeb(QPCIBus *bus, int devfn, uint8_t offset, uint8_t value)
{
    outl(0xcf8, (1U << 31) | (devfn << 8) | offset);
    outb(0xcfc, value);
}

static void qpci_pc_config_writew(QPCIBus *bus, int devfn, uint8_t offset, uint16_t value)
{
    outl(0xcf8, (1U << 31) | (devfn << 8) | offset);
    outw(0xcfc, value);
}

static void qpci_pc_config_writel(QPCIBus *bus, int devfn, uint8_t offset, uint32_t value)
{
    outl(0xcf8, (1U << 31) | (devfn << 8) | offset);
    outl(0xcfc, value);
}

static void qpci_pc_msix_enable(QPCIDevice *dev)
{
    uint8_t addr;
    uint16_t val;
    uint32_t table;
    uint8_t bir_table;
    uint8_t bir_pba;

    addr = qpci_find_capability(dev, PCI_CAP_ID_MSIX);
    g_assert_cmphex(addr, !=, 0);

    val = qpci_config_readw(dev, addr + PCI_MSIX_FLAGS);
    qpci_config_writew(dev, addr + PCI_MSIX_FLAGS, val | PCI_MSIX_FLAGS_ENABLE);

    table = qpci_config_readl(dev, addr + PCI_MSIX_TABLE);
    bir_table = table & PCI_MSIX_FLAGS_BIRMASK;
    dev->msix_table_bar = qpci_iomap(dev, bir_table, NULL);
    dev->msix_table_off = table & ~PCI_MSIX_FLAGS_BIRMASK;

    table = qpci_config_readl(dev, addr + PCI_MSIX_PBA);
    bir_pba = table & PCI_MSIX_FLAGS_BIRMASK;
    if (bir_pba != bir_table) {
        dev->msix_pba_bar = qpci_iomap(dev, bir_pba, NULL);
    } else {
        dev->msix_pba_bar = dev->msix_table_bar;
    }
    dev->msix_pba_off = table & ~PCI_MSIX_FLAGS_BIRMASK;

    dev->msix_enabled = true;
}

static void qpci_pc_msix_disable(QPCIDevice *dev)
{
    uint8_t addr;
    uint16_t val;

    g_assert(dev->msix_enabled);
    addr = qpci_find_capability(dev, PCI_CAP_ID_MSIX);
    g_assert_cmphex(addr, !=, 0);
    val = qpci_config_readw(dev, addr + PCI_MSIX_FLAGS);
    qpci_config_writew(dev, addr + PCI_MSIX_FLAGS,
                                                val & ~PCI_MSIX_FLAGS_ENABLE);

    if (dev->msix_pba_bar.addr != dev->msix_table_bar.addr) {
        qpci_iounmap(dev, dev->msix_pba_bar);
    }
    qpci_iounmap(dev, dev->msix_table_bar);

    dev->msix_enabled = 0;
    dev->msix_table_off = 0;
    dev->msix_pba_off = 0;
}

static bool qpci_pc_msix_pending(QPCIDevice *dev, uint16_t entry)
{
    uint32_t pba_entry;
    uint8_t bit_n = entry % 32;
    uint64_t  off = (entry / 32) * PCI_MSIX_ENTRY_SIZE / 4;

    g_assert(dev->msix_enabled);
    pba_entry = qpci_io_readl(dev, dev->msix_pba_bar, dev->msix_pba_off + off);
    qpci_io_writel(dev, dev->msix_pba_bar, dev->msix_pba_off + off,
                   pba_entry & ~(1 << bit_n));
    return (pba_entry & (1 << bit_n)) != 0;
}

static bool qpci_pc_msix_masked(QPCIDevice *dev, uint16_t entry)
{
    uint8_t addr;
    uint16_t val;
    uint64_t vector_off = dev->msix_table_off + entry * PCI_MSIX_ENTRY_SIZE;

    g_assert(dev->msix_enabled);
    addr = qpci_find_capability(dev, PCI_CAP_ID_MSIX);
    g_assert_cmphex(addr, !=, 0);
    val = qpci_config_readw(dev, addr + PCI_MSIX_FLAGS);

    if (val & PCI_MSIX_FLAGS_MASKALL) {
        return true;
    } else {
        return (qpci_io_readl(dev, dev->msix_table_bar,
                              vector_off + PCI_MSIX_ENTRY_VECTOR_CTRL)
                & PCI_MSIX_ENTRY_CTRL_MASKBIT) != 0;
    }
}

static uint16_t qpci_pc_msix_table_size(QPCIDevice *dev)
{
    uint8_t addr;
    uint16_t control;

    addr = qpci_find_capability(dev, PCI_CAP_ID_MSIX);
    g_assert_cmphex(addr, !=, 0);

    control = qpci_config_readw(dev, addr + PCI_MSIX_FLAGS);
    return (control & PCI_MSIX_FLAGS_QSIZE) + 1;
}

QPCIBus *qpci_init_pc(QTestState *qts, QGuestAllocator *alloc)
{
    QPCIBusPC *ret = g_new0(QPCIBusPC, 1);

    assert(qts);

    ret->bus.pio_readb = qpci_pc_pio_readb;
    ret->bus.pio_readw = qpci_pc_pio_readw;
    ret->bus.pio_readl = qpci_pc_pio_readl;
    ret->bus.pio_readq = qpci_pc_pio_readq;

    ret->bus.pio_writeb = qpci_pc_pio_writeb;
    ret->bus.pio_writew = qpci_pc_pio_writew;
    ret->bus.pio_writel = qpci_pc_pio_writel;
    ret->bus.pio_writeq = qpci_pc_pio_writeq;

    ret->bus.memread = qpci_pc_memread;
    ret->bus.memwrite = qpci_pc_memwrite;

    ret->bus.config_readb = qpci_pc_config_readb;
    ret->bus.config_readw = qpci_pc_config_readw;
    ret->bus.config_readl = qpci_pc_config_readl;

    ret->bus.config_writeb = qpci_pc_config_writeb;
    ret->bus.config_writew = qpci_pc_config_writew;
    ret->bus.config_writel = qpci_pc_config_writel;

    ret->bus.msix_enable = qpci_pc_msix_enable;
    ret->bus.msix_disable = qpci_pc_msix_disable;
    ret->bus.msix_pending = qpci_pc_msix_pending;
    ret->bus.msix_masked = qpci_pc_msix_masked;
    ret->bus.msix_table_size = qpci_pc_msix_table_size;

    ret->bus.qts = qts;
    ret->bus.pio_alloc_ptr = 0xc000;
    ret->bus.mmio_alloc_ptr = 0xE0000000;
    ret->bus.mmio_limit = 0x100000000ULL;

    return &ret->bus;
}

void qpci_free_pc(QPCIBus *bus)
{
    QPCIBusPC *s = container_of(bus, QPCIBusPC, bus);

    g_free(s);
}

void qpci_unplug_acpi_device_test(const char *id, uint8_t slot)
{
    QDict *response;
    char *cmd;

    cmd = g_strdup_printf("{'execute': 'device_del',"
                          " 'arguments': {"
                          "   'id': '%s'"
                          "}}", id);
    response = qmp(cmd);
    g_free(cmd);
    g_assert(response);
    g_assert(!qdict_haskey(response, "error"));
    qobject_unref(response);

    outb(ACPI_PCIHP_ADDR + PCI_EJ_BASE, 1 << slot);

    qmp_eventwait("DEVICE_DELETED");
}
