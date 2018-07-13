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
#include "libqos/e1000e.h"

#define E1000E_TXD_LEN              (16)
#define E1000E_RXD_LEN              (16)

static int test_sockets[2];

static void e1000e_tx_ring_push(QE1000E *d, void *descr)
{
    uint32_t tail = d->readl(d, E1000E_TDT);
    uint32_t len = d->readl(d, E1000E_TDLEN) / E1000E_TXD_LEN;

    memwrite(d->tx_ring + tail * E1000E_TXD_LEN, descr, E1000E_TXD_LEN);
    d->writel(d, E1000E_TDT, (tail + 1) % len);

    /* Read WB data for the packet transmitted */
    memread(d->tx_ring + tail * E1000E_TXD_LEN, descr, E1000E_TXD_LEN);
}

static void e1000e_rx_ring_push(QE1000E *d, void *descr)
{
    uint32_t tail = d->readl(d, E1000E_RDT);
    uint32_t len = d->readl(d, E1000E_RDLEN) / E1000E_RXD_LEN;

    memwrite(d->rx_ring + tail * E1000E_RXD_LEN, descr, E1000E_RXD_LEN);
    d->writel(d, E1000E_RDT, (tail + 1) % len);

    /* Read WB data for the packet received */
    memread(d->rx_ring + tail * E1000E_RXD_LEN, descr, E1000E_RXD_LEN);
}

static void e1000e_send_verify(QE1000E *d, QGuestAllocator *alloc)
{
    struct {
        uint64_t buffer_addr;
        union {
            uint32_t data;
            struct {
                uint16_t length;
                uint8_t cso;
                uint8_t cmd;
            } flags;
        } lower;
        union {
            uint32_t data;
            struct {
                uint8_t status;
                uint8_t css;
                uint16_t special;
            } fields;
        } upper;
    } descr;

    static const uint32_t dtyp_data = BIT(20);
    static const uint32_t dtyp_ext  = BIT(29);
    static const uint32_t dcmd_rs   = BIT(27);
    static const uint32_t dcmd_eop  = BIT(24);
    static const uint32_t dsta_dd   = BIT(0);
    static const int data_len = 64;
    char buffer[64];
    int ret;
    uint32_t recv_len;

    /* Prepare test data buffer */
    uint64_t data = guest_alloc(alloc, data_len);
    memwrite(data, "TEST", 5);

    /* Prepare TX descriptor */
    memset(&descr, 0, sizeof(descr));
    descr.buffer_addr = cpu_to_le64(data);
    descr.lower.data = cpu_to_le32(dcmd_rs   |
                                   dcmd_eop  |
                                   dtyp_ext  |
                                   dtyp_data |
                                   data_len);

    /* Put descriptor to the ring */
    e1000e_tx_ring_push(d, &descr);

    /* Wait for TX WB interrupt */
    d->wait_isr(d, E1000E_TX0_MSG_ID);

    /* Check DD bit */
    g_assert_cmphex(le32_to_cpu(descr.upper.data) & dsta_dd, ==, dsta_dd);

    /* Check data sent to the backend */
    ret = qemu_recv(test_sockets[0], &recv_len, sizeof(recv_len), 0);
    g_assert_cmpint(ret, == , sizeof(recv_len));
    qemu_recv(test_sockets[0], buffer, 64, 0);
    g_assert_cmpstr(buffer, == , "TEST");

    /* Free test data buffer */
    guest_free(alloc, data);
}

static void e1000e_receive_verify(QE1000E *d, QGuestAllocator *alloc)
{
    union {
        struct {
            uint64_t buffer_addr;
            uint64_t reserved;
        } read;
        struct {
            struct {
                uint32_t mrq;
                union {
                    uint32_t rss;
                    struct {
                        uint16_t ip_id;
                        uint16_t csum;
                    } csum_ip;
                } hi_dword;
            } lower;
            struct {
                uint32_t status_error;
                uint16_t length;
                uint16_t vlan;
            } upper;
        } wb;
    } descr;

    static const uint32_t esta_dd = BIT(0);

    char test[] = "TEST";
    int len = htonl(sizeof(test));
    struct iovec iov[] = {
        {
            .iov_base = &len,
            .iov_len = sizeof(len),
        },{
            .iov_base = test,
            .iov_len = sizeof(test),
        },
    };

    static const int data_len = 64;
    char buffer[64];
    int ret;

    /* Send a dummy packet to device's socket*/
    ret = iov_send(test_sockets[0], iov, 2, 0, sizeof(len) + sizeof(test));
    g_assert_cmpint(ret, == , sizeof(test) + sizeof(len));

    /* Prepare test data buffer */
    uint64_t data = guest_alloc(alloc, data_len);

    /* Prepare RX descriptor */
    memset(&descr, 0, sizeof(descr));
    descr.read.buffer_addr = cpu_to_le64(data);

    /* Put descriptor to the ring */
    e1000e_rx_ring_push(d, &descr);

    /* Wait for TX WB interrupt */
    d->wait_isr(d, E1000E_RX0_MSG_ID);

    /* Check DD bit */
    g_assert_cmphex(le32_to_cpu(descr.wb.upper.status_error) &
        esta_dd, ==, esta_dd);

    /* Check data sent to the backend */
    memread(data, buffer, sizeof(buffer));
    g_assert_cmpstr(buffer, == , "TEST");

    /* Free test data buffer */
    guest_free(alloc, data);
}

static void test_e1000e_init(void *obj, void *data, QGuestAllocator * alloc)
{
    /* init does nothing */
}

static void test_e1000e_tx(void *obj, void *data, QGuestAllocator * alloc)
{
    QE1000E *d = obj;

    e1000e_send_verify(d, alloc);
}

static void test_e1000e_rx(void *obj, void *data, QGuestAllocator * alloc)
{
    QE1000E *d = obj;

    e1000e_receive_verify(d, alloc);
}

static void test_e1000e_multiple_transfers(void *obj, void *data,
                                           QGuestAllocator * alloc)
{
    static const long iterations = 4 * 1024;
    long i;

    QE1000E *d = obj;

    for (i = 0; i < iterations; i++) {
        e1000e_send_verify(d, alloc);
        e1000e_receive_verify(d, alloc);
    }

}

static void test_e1000e_hotplug(void *obj, void *data, QGuestAllocator * alloc)
{
    static const uint8_t slot = 0x06;

    qpci_plug_device_test("e1000e", "e1000e_net", slot, NULL);
    qpci_unplug_acpi_device_test("e1000e_net", slot);
}

static void data_test_init(char **cmd_line)
{
    char *new_cmdline;

    int ret = socketpair(PF_UNIX, SOCK_STREAM, 0, test_sockets);
    g_assert_cmpint(ret, != , -1);

    new_cmdline = g_strdup_printf("%s -netdev socket,fd=%d,id=hs0 ", *cmd_line,
                              test_sockets[1]);
    g_assert_nonnull(new_cmdline);

    g_free(*cmd_line);
    *cmd_line = new_cmdline;
}

static void data_test_clear(void)
{
    close(test_sockets[0]);
}

static void e1000e_test(void)
{
    QOSGraphTestOptions *opts = g_new0(QOSGraphTestOptions, 1);
    opts->edge_args = "netdev=hs0";
    opts->before = data_test_init;
    opts->after = data_test_clear;
    qos_add_test_args("e1000e/init", "e1000e-if", test_e1000e_init, opts);
    qos_add_test_args("e1000e/tx", "e1000e-if", test_e1000e_tx, opts);
    qos_add_test_args("e1000e/rx", "e1000e-if", test_e1000e_rx, opts);
    qos_add_test_args("e1000e/multiple_transfers", "e1000e-if", 
                      test_e1000e_multiple_transfers, opts);
    qos_add_test("e1000e/hotplug", "e1000e-if", test_e1000e_hotplug);

    g_free(opts);
}

libqos_init(e1000e_test);
