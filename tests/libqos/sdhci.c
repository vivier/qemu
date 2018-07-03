/*
 * libqos driver framework
 *
 * Copyright (c) 2018 Emanuele Giuseppe Esposito <e.emanuelegiuseppe@gmail.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License version 2 as published by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, see <http://www.gnu.org/licenses/>
 */

#include "qemu/osdep.h"
#include "libqtest.h"
#include "qgraph.h"
#include "pci.h"
#include "sdhci.h"
#include "hw/pci/pci.h"

static void set_qsdhci_fields(QSDHCI *s, uint8_t version, uint8_t baseclock,
                              bool sdma, uint64_t reg)
{
    s->props.version = version;
    s->props.baseclock = baseclock;
    s->props.capab.sdma = sdma;
    s->props.capab.reg = reg;
}

/* Memory mapped implementation of QSDHCI */

static uint16_t sdhci_mm_readw(QSDHCI *s, uint32_t reg)
{
    QSDHCI_MemoryMapped *smm = container_of(s, QSDHCI_MemoryMapped, sdhci);
    return qtest_readw(global_qtest, smm->addr + reg);
}

static uint64_t sdhci_mm_readq(QSDHCI *s, uint32_t reg)
{
    QSDHCI_MemoryMapped *smm = container_of(s, QSDHCI_MemoryMapped, sdhci);
    return qtest_readq(global_qtest, smm->addr + reg);
}

static void sdhci_mm_writeq(QSDHCI *s, uint32_t reg, uint64_t val)
{
    QSDHCI_MemoryMapped *smm = container_of(s, QSDHCI_MemoryMapped, sdhci);
    qtest_writeq(global_qtest, smm->addr + reg, val);
}

static void *sdhci_mm_get_driver(void *obj, const char *interface)
{
    QSDHCI_MemoryMapped *spci = obj;
    if (!g_strcmp0(interface, "sdhci")) {
        return &spci->sdhci;
    }
    printf("%s not present in generic-sdhci\n", interface);
    abort();
}

void qos_create_sdhci_mm(QSDHCI_MemoryMapped *sdhci, uint32_t addr,
                         QSDHCIProperties *common)
{
    sdhci->obj.get_driver = sdhci_mm_get_driver;
    sdhci->sdhci.readw = sdhci_mm_readw;
    sdhci->sdhci.readq = sdhci_mm_readq;
    sdhci->sdhci.writeq = sdhci_mm_writeq;
    memcpy(&sdhci->sdhci.props, common, sizeof(QSDHCIProperties));
    sdhci->addr = addr;
}

/* PCI implementation of QSDHCI */

static uint16_t sdhci_pci_readw(QSDHCI *s, uint32_t reg)
{
    QSDHCI_PCI *spci = container_of(s, QSDHCI_PCI, sdhci);
    return qpci_io_readw(&spci->dev, spci->mem_bar, reg);
}

static uint64_t sdhci_readq(QSDHCI *s, uint32_t reg)
{
    QSDHCI_PCI *spci = container_of(s, QSDHCI_PCI, sdhci);
    return qpci_io_readq(&spci->dev, spci->mem_bar, reg);
}

static void sdhci_writeq(QSDHCI *s, uint32_t reg, uint64_t val)
{
    QSDHCI_PCI *spci = container_of(s, QSDHCI_PCI, sdhci);
    return qpci_io_writeq(&spci->dev, spci->mem_bar, reg, val);
}

static void *sdhci_pci_get_driver(void *object, const char *interface)
{
    QSDHCI_PCI *spci = object;
    if (!g_strcmp0(interface, "sdhci")) {
        return &spci->sdhci;
    }

    printf("%s not present in sdhci-pci\n", interface);
    abort();
}

static void sdhci_destroy(QOSGraphObject *obj)
{
    QSDHCI_PCI *spci = (QSDHCI_PCI *)obj;
    qpci_iounmap(&spci->dev, spci->mem_bar);
    g_free(spci);
}

static void *sdhci_pci_create(void *pci_bus, QGuestAllocator *alloc, void *addr)
{
    QSDHCI_PCI *spci = g_new0(QSDHCI_PCI, 1);
    QPCIBus *bus = pci_bus;
    uint64_t barsize;

    qpci_device_init(&spci->dev, bus, addr);
    spci->mem_bar = qpci_iomap(&spci->dev, 0, &barsize);
    spci->obj.get_driver = sdhci_pci_get_driver;
    spci->obj.destructor = sdhci_destroy;
    spci->sdhci.readw = sdhci_pci_readw;
    spci->sdhci.readq = sdhci_readq;
    spci->sdhci.writeq = sdhci_writeq;
    set_qsdhci_fields(&spci->sdhci, 2, 0, 1, 0x057834b4);
    return &spci->obj;
}

static void qsdhci(void)
{
    QPCIAddress addr = {
        .devfn = QPCI_DEVFN(4, 0),
        .vendor_id = PCI_VENDOR_ID_REDHAT,
        .device_id = PCI_DEVICE_ID_REDHAT_SDHCI,
    };

    qos_node_create_interface("sdhci");
    qos_node_create_driver("generic-sdhci", NULL);
    qos_node_produces("generic-sdhci", "sdhci");
    qos_node_create_driver("sdhci-pci", sdhci_pci_create);
    qos_node_produces("sdhci-pci", "sdhci");
    qos_node_consumes_args("sdhci-pci", "pci-bus", &(QOSGraphEdgeOptions) {
        .arg = &addr,
        .size_arg = sizeof(QPCIAddress),
        .cmd_line = "addr=04.0",
    });
}

libqos_init(qsdhci);
