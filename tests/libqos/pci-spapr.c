/*
 * libqos PCI bindings for SPAPR
 *
 * This work is licensed under the terms of the GNU GPL, version 2 or later.
 * See the COPYING file in the top-level directory.
 */

#include "qemu/osdep.h"
#include "libqtest.h"
#include "libqos/pci-spapr.h"
#include "libqos/rtas.h"
#include "qgraph.h"

#include "hw/pci/pci_regs.h"

#include "qemu-common.h"
#include "qemu/host-utils.h"

/*
 * PCI devices are always little-endian
 * SPAPR by default is big-endian
 * so PCI accessors need to swap data endianness
 */

static uint8_t qpci_spapr_pio_readb(QPCIBus *bus, uint32_t addr)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    return readb(s->pio_cpu_base + addr);
}

static void qpci_spapr_pio_writeb(QPCIBus *bus, uint32_t addr, uint8_t val)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    writeb(s->pio_cpu_base + addr, val);
}

static uint16_t qpci_spapr_pio_readw(QPCIBus *bus, uint32_t addr)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    return bswap16(readw(s->pio_cpu_base + addr));
}

static void qpci_spapr_pio_writew(QPCIBus *bus, uint32_t addr, uint16_t val)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    writew(s->pio_cpu_base + addr, bswap16(val));
}

static uint32_t qpci_spapr_pio_readl(QPCIBus *bus, uint32_t addr)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    return bswap32(readl(s->pio_cpu_base + addr));
}

static void qpci_spapr_pio_writel(QPCIBus *bus, uint32_t addr, uint32_t val)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    writel(s->pio_cpu_base + addr, bswap32(val));
}

static uint64_t qpci_spapr_pio_readq(QPCIBus *bus, uint32_t addr)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    return bswap64(readq(s->pio_cpu_base + addr));
}

static void qpci_spapr_pio_writeq(QPCIBus *bus, uint32_t addr, uint64_t val)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    writeq(s->pio_cpu_base + addr, bswap64(val));
}

static void qpci_spapr_memread(QPCIBus *bus, uint32_t addr,
                               void *buf, size_t len)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    memread(s->mmio32_cpu_base + addr, buf, len);
}

static void qpci_spapr_memwrite(QPCIBus *bus, uint32_t addr,
                                const void *buf, size_t len)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    memwrite(s->mmio32_cpu_base + addr, buf, len);
}

static uint8_t qpci_spapr_config_readb(QPCIBus *bus, int devfn, uint8_t offset)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    uint32_t config_addr = (devfn << 8) | offset;
    return qrtas_ibm_read_pci_config(bus->qts, s->alloc, s->buid,
                                     config_addr, 1);
}

static uint16_t qpci_spapr_config_readw(QPCIBus *bus, int devfn, uint8_t offset)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    uint32_t config_addr = (devfn << 8) | offset;
    return qrtas_ibm_read_pci_config(bus->qts, s->alloc, s->buid,
                                     config_addr, 2);
}

static uint32_t qpci_spapr_config_readl(QPCIBus *bus, int devfn, uint8_t offset)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    uint32_t config_addr = (devfn << 8) | offset;
    return qrtas_ibm_read_pci_config(bus->qts, s->alloc, s->buid,
                                     config_addr, 4);
}

static void qpci_spapr_config_writeb(QPCIBus *bus, int devfn, uint8_t offset,
                                     uint8_t value)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    uint32_t config_addr = (devfn << 8) | offset;
    qrtas_ibm_write_pci_config(bus->qts, s->alloc, s->buid,
                               config_addr, 1, value);
}

static void qpci_spapr_config_writew(QPCIBus *bus, int devfn, uint8_t offset,
                                     uint16_t value)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    uint32_t config_addr = (devfn << 8) | offset;
    qrtas_ibm_write_pci_config(bus->qts, s->alloc, s->buid,
                               config_addr, 2, value);
}

static void qpci_spapr_config_writel(QPCIBus *bus, int devfn, uint8_t offset,
                                     uint32_t value)
{
    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);
    uint32_t config_addr = (devfn << 8) | offset;
    qrtas_ibm_write_pci_config(bus->qts, s->alloc, s->buid,
                               config_addr, 4, value);
}

static void qpci_spapr_msix_enable(QPCIDevice *dev)
{
    QPCIBusSPAPR *s = container_of(dev->bus, QPCIBusSPAPR, bus);
    uint32_t config_addr = dev->devfn << 8;
    uint8_t addr;
    uint16_t val;
    uint32_t table, irq;
    uint8_t bir_table;
    uint8_t bir_pba;
    int ret;

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

    ret = qrtas_change_msi(dev->bus->qts, s->alloc, s->buid, config_addr,
                                 RTAS_CHANGE_MSIX_FN, 1);
    g_assert_cmpint(ret, ==, 1);

    irq = qrtas_query_irq_number(dev->bus->qts, s->alloc, s->buid,
                                 config_addr, 0);
    ret = qrtas_ibm_int_on(dev->bus->qts, s->alloc, irq);
    g_assert_cmpint(ret, ==, 0);

    dev->msix_enabled = true;
}

static void qpci_spapr_msix_disable(QPCIDevice *dev)
{
    QPCIBusSPAPR *s = container_of(dev->bus, QPCIBusSPAPR, bus);
    uint32_t config_addr = dev->devfn << 8;
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

    if (qrtas_change_msi(dev->bus->qts, s->alloc, s->buid, config_addr,
                        RTAS_CHANGE_MSI_FN, 0) != 0) {
        qrtas_change_msi(dev->bus->qts, s->alloc, s->buid, config_addr, RTAS_CHANGE_FN, 0);
    }
}

static bool qpci_spapr_msix_pending(QPCIDevice *dev, uint16_t entry)
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

static bool qpci_spapr_msix_masked(QPCIDevice *dev, uint16_t entry)
{
    uint8_t addr;
    uint16_t val;
    uint64_t vector_off = dev->msix_table_off + entry * PCI_MSIX_ENTRY_SIZE;

fprintf(stderr, "qpci_spapr_msix_masked\n");
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

static uint16_t qpci_spapr_msix_table_size(QPCIDevice *dev)
{
    uint8_t addr;
    uint16_t control;

    addr = qpci_find_capability(dev, PCI_CAP_ID_MSIX);
    g_assert_cmphex(addr, !=, 0);

    control = qpci_config_readw(dev, addr + PCI_MSIX_FLAGS);
    return (control & PCI_MSIX_FLAGS_QSIZE) + 1;
}

#define SPAPR_PCI_BASE               (1ULL << 45)

#define SPAPR_PCI_MMIO32_WIN_SIZE    0x80000000 /* 2 GiB */
#define SPAPR_PCI_IO_WIN_SIZE        0x10000

static void *qspapr_get_driver(void *obj, const char *interface)
{
    QPCIBusSPAPR *qpci = obj;
    if (!g_strcmp0(interface, "pci-bus")) {
        return &qpci->bus;
    }
    printf("%s not present in pci-bus-spapr", interface);
    abort();
}

void qpci_set_spapr(QPCIBusSPAPR *ret, QTestState *qts, QGuestAllocator *alloc)
{
    assert(qts);

    ret->alloc = alloc;

    ret->bus.pio_readb = qpci_spapr_pio_readb;
    ret->bus.pio_readw = qpci_spapr_pio_readw;
    ret->bus.pio_readl = qpci_spapr_pio_readl;
    ret->bus.pio_readq = qpci_spapr_pio_readq;

    ret->bus.pio_writeb = qpci_spapr_pio_writeb;
    ret->bus.pio_writew = qpci_spapr_pio_writew;
    ret->bus.pio_writel = qpci_spapr_pio_writel;
    ret->bus.pio_writeq = qpci_spapr_pio_writeq;

    ret->bus.memread = qpci_spapr_memread;
    ret->bus.memwrite = qpci_spapr_memwrite;

    ret->bus.config_readb = qpci_spapr_config_readb;
    ret->bus.config_readw = qpci_spapr_config_readw;
    ret->bus.config_readl = qpci_spapr_config_readl;

    ret->bus.config_writeb = qpci_spapr_config_writeb;
    ret->bus.config_writew = qpci_spapr_config_writew;
    ret->bus.config_writel = qpci_spapr_config_writel;

    /* FIXME: We assume the default location of the PHB for now.
     * Ideally we'd parse the device tree deposited in the guest to
     * get the window locations */
    ret->buid = 0x800000020000000ULL;

    ret->pio_cpu_base = SPAPR_PCI_BASE;
    ret->pio.pci_base = 0;
    ret->pio.size = SPAPR_PCI_IO_WIN_SIZE;

    /* 32-bit portion of the MMIO window is at PCI address 2..4 GiB */
    ret->mmio32_cpu_base = SPAPR_PCI_BASE;
    ret->mmio32.pci_base = SPAPR_PCI_MMIO32_WIN_SIZE;
    ret->mmio32.size = SPAPR_PCI_MMIO32_WIN_SIZE;

    ret->bus.msix_enable = qpci_spapr_msix_enable;
    ret->bus.msix_disable = qpci_spapr_msix_disable;
    ret->bus.msix_pending = qpci_spapr_msix_pending;
    ret->bus.msix_masked = qpci_spapr_msix_masked;
    ret->bus.msix_table_size = qpci_spapr_msix_table_size;

    ret->bus.qts = qts;
    ret->bus.pio_alloc_ptr = 0xc000;
    ret->bus.mmio_alloc_ptr = ret->mmio32.pci_base;
    ret->bus.mmio_limit = ret->mmio32.pci_base + ret->mmio32.size;

    ret->obj.get_driver = qspapr_get_driver;
}

QPCIBus *qpci_init_spapr(QTestState *qts, QGuestAllocator *alloc)
{
    QPCIBusSPAPR *ret = g_new0(QPCIBusSPAPR, 1);
    qpci_set_spapr(ret, qts, alloc);
    
    return &ret->bus;
}

void qpci_free_spapr(QPCIBus *bus)
{
    if (!bus) {
        return;
    }

    QPCIBusSPAPR *s = container_of(bus, QPCIBusSPAPR, bus);

    g_free(s);
}

static void qpci_spapr(void)
{
    qos_node_create_driver("pci-bus-spapr", NULL);
    qos_node_produces("pci-bus-spapr", "pci-bus");
}

libqos_init(qpci_spapr);
