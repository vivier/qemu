/*
 * This work is licensed under the terms of the GNU GPL, version 2 or later.
 * See the COPYING file in the top-level directory.
 */

#include "qemu/osdep.h"
#include "libqtest.h"
#include "libqos/rtas.h"

#define RTAS_BUSY               -2
#define RTAS_EXTENDED_DELAY_MIN 9900
#define RTAS_EXTENDED_DELAY_MAX 9905

static void qrtas_copy_args(QTestState *qts, uint64_t target_args,
                            uint32_t nargs, uint32_t *args)
{
    int i;

    for (i = 0; i < nargs; i++) {
        qtest_writel(qts, target_args + i * sizeof(uint32_t), args[i]);
    }
}

static void qrtas_copy_ret(QTestState *qts, uint64_t target_ret,
                           uint32_t nret, uint32_t *ret)
{
    int i;

    for (i = 0; i < nret; i++) {
        ret[i] = qtest_readl(qts, target_ret + i * sizeof(uint32_t));
    }
}

static uint64_t qrtas_call(QTestState *qts, QGuestAllocator *alloc,
                           const char *name,
                           uint32_t nargs, uint32_t *args,
                           uint32_t nret, uint32_t *ret)
{
    uint64_t res;
    uint64_t target_args, target_ret;

    target_args = guest_alloc(alloc, nargs * sizeof(uint32_t));
    target_ret = guest_alloc(alloc, nret * sizeof(uint32_t));

    qrtas_copy_args(qts, target_args, nargs, args);
    res = qtest_rtas_call(qts, name, nargs, target_args, nret, target_ret);
    qrtas_copy_ret(qts, target_ret, nret, ret);

    guest_free(alloc, target_ret);
    guest_free(alloc, target_args);

    return res;
}

static unsigned int qrtas_busy_delay(int status)
{
    unsigned int ret = 0;

    if (status == RTAS_BUSY) {
        ret = 1;
        usleep(1000);
    } else if (RTAS_EXTENDED_DELAY_MIN <= status &&
               status <= RTAS_EXTENDED_DELAY_MAX) {
        status -= RTAS_EXTENDED_DELAY_MIN;
        for (ret = 1; status > 0; status--)
            ret *= 10;
        usleep(1000 * ret);
    }
    return ret;
}

int qrtas_get_time_of_day(QTestState *qts, QGuestAllocator *alloc,
                          struct tm *tm, uint32_t *ns)
{
    int res;
    uint32_t ret[8];

    res = qrtas_call(qts, alloc, "get-time-of-day", 0, NULL, 8, ret);
    if (res != 0) {
        return res;
    }

    res = ret[0];
    memset(tm, 0, sizeof(*tm));
    tm->tm_year = ret[1] - 1900;
    tm->tm_mon = ret[2] - 1;
    tm->tm_mday = ret[3];
    tm->tm_hour = ret[4];
    tm->tm_min = ret[5];
    tm->tm_sec = ret[6];
    *ns = ret[7];

    return res;
}

uint32_t qrtas_ibm_read_pci_config(QTestState *qts, QGuestAllocator *alloc,
                                   uint64_t buid,
                                   uint32_t addr, uint32_t size)
{
    int res;
    uint32_t args[4], ret[2];

    args[0] = addr;
    args[1] = buid >> 32;
    args[2] = buid & 0xffffffff;
    args[3] = size;
    res = qrtas_call(qts, alloc, "ibm,read-pci-config", 4, args, 2, ret);
    if (res != 0) {
        return -1;
    }

    if (ret[0] != 0) {
        return -1;
    }

    return ret[1];
}

int qrtas_ibm_write_pci_config(QTestState *qts, QGuestAllocator *alloc,
                               uint64_t buid,
                               uint32_t addr, uint32_t size, uint32_t val)
{
    int res;
    uint32_t args[5], ret[1];

    args[0] = addr;
    args[1] = buid >> 32;
    args[2] = buid & 0xffffffff;
    args[3] = size;
    args[4] = val;
    res = qrtas_call(qts, alloc, "ibm,write-pci-config", 5, args, 1, ret);
    if (res != 0) {
        return -1;
    }

    if (ret[0] != 0) {
        return -1;
    }

    return 0;
}

int qrtas_ibm_change_msi(QTestState *qts,  QGuestAllocator *alloc,
                         uint64_t buid,
                         uint32_t addr, uint32_t func, uint32_t req_num,
                         uint32_t *intr_type)
{
    int res;
    uint32_t args[6], ret[4];

    args[0] = addr;
    args[1] = buid >> 32;
    args[2] = buid & 0xffffffff;
    args[3] = func;
    args[4] = req_num;
    args[5] = 1; /* sequence number, first call */

    do {
        res = qrtas_call(qts, alloc, "ibm,change-msi", 6, args,
                         intr_type ? 4 : 3, ret);
        if (res != 0) {
            return -1;
        }
        args[5] = ret[1]; /* sequence number, next calls */
    } while (qrtas_busy_delay(res));

    res = ret[0];
    if (res < 0) {
        return res;
    }

    if (intr_type) {
        *intr_type = ret[3];
    }

    return ret[1];
}

uint32_t qrtas_ibm_query_interrupt_source_number(QTestState *qts,
                                                 QGuestAllocator *alloc,
                                                 uint64_t buid, uint32_t addr,
                                                 uint32_t ioa_intr_num)
{
    int res;
    uint32_t args[4], ret[3];

    args[0] = addr;
    args[1] = buid >> 32;
    args[2] = buid & 0xffffffff;
    args[3] = ioa_intr_num;

    res = qrtas_call(qts, alloc, "ibm,query-interrupt-source-number", 4, args,
                     3, ret);
    if (res != 0) {
        return -1;
    }

    if (ret[0] != 0) {
        return -1;
    }

    return ret[1];
}
