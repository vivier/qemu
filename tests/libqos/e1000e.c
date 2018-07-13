 /*
 * QTest testcase for e1000e NIC
 *
 * Copyright (c) 2015 Ravello Systems LTD (http://ravellosystems.com)
 * Developed by Daynix Computing LTD (http://www.daynix.com)
 *
 * Authors:
 * Dmitry Fleytman <dmitry@daynix.com>
 * Leonid Bloch <leonid@daynix.com>
 * Yan Vugenfirer <yan@daynix.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, see <http://www.gnu.org/licenses/>.
 */

#include "qemu/osdep.h"
#include "libqtest.h"
#include "qemu-common.h"
#include "libqos/pci-pc.h"
#include "qemu/sockets.h"
#include "qemu/iov.h"
#include "qemu/bitops.h"
#include "libqos/malloc.h"
#include "libqos/malloc-pc.h"
#include "libqos/malloc-generic.h"
#include "qgraph.h"
#include "e1000e.h"

#define E1000E_IMS      (0x00d0)

#define E1000E_STATUS   (0x0008)
#define E1000E_STATUS_LU BIT(1)
#define E1000E_STATUS_ASDV1000 BIT(9)

#define E1000E_CTRL     (0x0000)
#define E1000E_CTRL_RESET BIT(26)

#define E1000E_RCTL     (0x0100)
#define E1000E_RCTL_EN  BIT(1)
#define E1000E_RCTL_UPE BIT(3)
#define E1000E_RCTL_MPE BIT(4)

#define E1000E_RFCTL     (0x5008)
#define E1000E_RFCTL_EXTEN  BIT(15)

#define E1000E_TCTL     (0x0400)
#define E1000E_TCTL_EN  BIT(1)

#define E1000E_CTRL_EXT             (0x0018)
#define E1000E_CTRL_EXT_DRV_LOAD    BIT(28)
#define E1000E_CTRL_EXT_TXLSFLOW    BIT(22)

#define E1000E_IVAR                 (0x00E4)
#define E1000E_IVAR_TEST_CFG        ((E1000E_RX0_MSG_ID << 0)    | BIT(3)  | \
                                     (E1000E_TX0_MSG_ID << 8)    | BIT(11) | \
                                     (E1000E_OTHER_MSG_ID << 16) | BIT(19) | \
                                     BIT(31))

#define E1000E_RING_LEN             (0x1000)

#define E1000E_TDBAL    (0x3800)

#define E1000E_TDBAH    (0x3804)
#define E1000E_TDH      (0x3810)

#define E1000E_RDBAL    (0x2800)
#define E1000E_RDBAH    (0x2804)
#define E1000E_RDH      (0x2810)

static void e1000e_macreg_write(QE1000E *d, uint32_t reg, uint32_t val)
{
    QE1000E_PCI *d_pci = container_of(d, QE1000E_PCI, e1000e);
    qpci_io_writel(&d_pci->pci_dev, d_pci->mac_regs, reg, val);
}

static uint32_t e1000e_macreg_read(QE1000E *d, uint32_t reg)
{
    QE1000E_PCI *d_pci = container_of(d, QE1000E_PCI, e1000e);
    return qpci_io_readl(&d_pci->pci_dev, d_pci->mac_regs, reg);
}

static void e1000e_pci_foreach_callback(QPCIDevice *dev, int devfn, void *data)
{
    QPCIDevice *res = data;
    memcpy(res, dev, sizeof(QPCIDevice));
}

static void e1000e_device_set_find(QPCIDevice *e1000e_dev, QPCIBus *bus,
                                   QPCIAddress *addr)
{
    qpci_device_foreach(bus, addr->vendor_id, addr->device_id,
                        e1000e_pci_foreach_callback, e1000e_dev);
}

static void e1000e_wait_isr(QE1000E *d, uint16_t msg_id)
{
    QE1000E_PCI *d_pci = container_of(d, QE1000E_PCI, e1000e);
    guint64 end_time = g_get_monotonic_time() + 5 * G_TIME_SPAN_SECOND;

    do {
        if (qpci_msix_pending(&d_pci->pci_dev, msg_id)) {
            return;
        }
        clock_step(10000);
    } while (g_get_monotonic_time() < end_time);

    g_error("Timeout expired");
}

static void e1000e_destroy(QOSGraphObject *obj)
{
    QE1000E_PCI *epci = (QE1000E_PCI *) obj;
    qpci_msix_disable(&epci->pci_dev);
    g_free(epci);
}

static void *e1000e_pci_get_driver(void *obj, const char *interface)
{
    QE1000E_PCI *epci = obj;
    if (!g_strcmp0(interface, "e1000e")) {
        return &epci->e1000e;
    }
    printf("%s not present in e1000e\n", interface);
    abort();
}

static void *e1000e_pci_create(void *pci_bus, QGuestAllocator *alloc, void *addr)
{
    QE1000E_PCI *d = g_new0(QE1000E_PCI, 1);
    QPCIBus *bus = pci_bus;
    uint32_t val;

    e1000e_device_set_find(&d->pci_dev, bus, addr);

    /* Enable the device */
    qpci_device_enable(&d->pci_dev);

    /* Map BAR0 (mac registers) */
    d->mac_regs = qpci_iomap(&d->pci_dev, 0, NULL);

    /* Reset the device */
    val = e1000e_macreg_read(&d->e1000e, E1000E_CTRL);
    e1000e_macreg_write(&d->e1000e, E1000E_CTRL, val | E1000E_CTRL_RESET);

    /* Enable and configure MSI-X */
    qpci_msix_enable(&d->pci_dev);
    e1000e_macreg_write(&d->e1000e, E1000E_IVAR, E1000E_IVAR_TEST_CFG);

    /* Check the device status - link and speed */
    val = e1000e_macreg_read(&d->e1000e, E1000E_STATUS);
    g_assert_cmphex(val & (E1000E_STATUS_LU | E1000E_STATUS_ASDV1000),
        ==, E1000E_STATUS_LU | E1000E_STATUS_ASDV1000);

    /* Initialize TX/RX logic */
    e1000e_macreg_write(&d->e1000e, E1000E_RCTL, 0);
    e1000e_macreg_write(&d->e1000e, E1000E_TCTL, 0);

    /* Notify the device that the driver is ready */
    val = e1000e_macreg_read(&d->e1000e, E1000E_CTRL_EXT);
    e1000e_macreg_write(&d->e1000e, E1000E_CTRL_EXT,
        val | E1000E_CTRL_EXT_DRV_LOAD | E1000E_CTRL_EXT_TXLSFLOW);

    /* Allocate and setup TX ring */
    d->e1000e.tx_ring = guest_alloc(alloc, E1000E_RING_LEN);
    g_assert(d->e1000e.tx_ring != 0);

    e1000e_macreg_write(&d->e1000e, E1000E_TDBAL, (uint32_t) d->e1000e.tx_ring);
    e1000e_macreg_write(&d->e1000e, E1000E_TDBAH, (uint32_t) (d->e1000e.tx_ring >> 32));
    e1000e_macreg_write(&d->e1000e, E1000E_TDLEN, E1000E_RING_LEN);
    e1000e_macreg_write(&d->e1000e, E1000E_TDT, 0);
    e1000e_macreg_write(&d->e1000e, E1000E_TDH, 0);

    /* Enable transmit */
    e1000e_macreg_write(&d->e1000e, E1000E_TCTL, E1000E_TCTL_EN);

    /* Allocate and setup RX ring */
    d->e1000e.rx_ring = guest_alloc(alloc, E1000E_RING_LEN);
    g_assert(d->e1000e.rx_ring != 0);

    e1000e_macreg_write(&d->e1000e, E1000E_RDBAL, (uint32_t)d->e1000e.rx_ring);
    e1000e_macreg_write(&d->e1000e, E1000E_RDBAH, (uint32_t)(d->e1000e.rx_ring >> 32));
    e1000e_macreg_write(&d->e1000e, E1000E_RDLEN, E1000E_RING_LEN);
    e1000e_macreg_write(&d->e1000e, E1000E_RDT, 0);
    e1000e_macreg_write(&d->e1000e, E1000E_RDH, 0);

    /* Enable receive */
    e1000e_macreg_write(&d->e1000e, E1000E_RFCTL, E1000E_RFCTL_EXTEN);
    e1000e_macreg_write(&d->e1000e, E1000E_RCTL, E1000E_RCTL_EN  |
                                        E1000E_RCTL_UPE |
                                        E1000E_RCTL_MPE);

    /* Enable all interrupts */
    e1000e_macreg_write(&d->e1000e, E1000E_IMS, 0xFFFFFFFF);

    d->obj.get_driver = e1000e_pci_get_driver;
    d->obj.destructor = e1000e_destroy;
    d->e1000e.readl = e1000e_macreg_read;
    d->e1000e.writel = e1000e_macreg_write;
    d->e1000e.wait_isr = e1000e_wait_isr;

    return &d->obj;
}

static void e1000e(void)
{
    QPCIAddress addr = {
        .devfn = 0,
        .vendor_id = 0x8086,
        .device_id = 0x10D3,
    };

    qos_node_create_interface("e1000e-if");
    qos_node_create_driver("e1000e", e1000e_pci_create);
    qos_node_produces("e1000e", "e1000e-if");
    qos_node_consumes_args("e1000e", "pci-bus", &(QOSGraphEdgeOptions) {
        .arg = &addr,
        .size_arg = sizeof(QPCIAddress),
        .cmd_line = "netdev=hs0",
    });
}

libqos_init(e1000e);
