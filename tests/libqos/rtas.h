/*
 * This work is licensed under the terms of the GNU GPL, version 2 or later.
 * See the COPYING file in the top-level directory.
 */

#ifndef LIBQOS_RTAS_H
#define LIBQOS_RTAS_H
#include "libqos/malloc.h"

/* MSI functions */
#define RTAS_QUERY_FN           0
#define RTAS_CHANGE_FN          1
#define RTAS_RESET_FN           2
#define RTAS_CHANGE_MSI_FN      3
#define RTAS_CHANGE_MSIX_FN     4
#define RTAS_CHANGE_32MSI_FN    5

int qrtas_get_time_of_day(QTestState *qts, QGuestAllocator *alloc,
                          struct tm *tm, uint32_t *ns);
uint32_t qrtas_ibm_read_pci_config(QTestState *qts, QGuestAllocator *alloc,
                                   uint64_t buid, uint32_t addr, uint32_t size);
int qrtas_ibm_write_pci_config(QTestState *qts, QGuestAllocator *alloc,
                               uint64_t buid, uint32_t addr, uint32_t size,
                               uint32_t val);
int qrtas_ibm_int_on(QTestState *qts, QGuestAllocator *alloc, uint32_t irq);
int qrtas_ibm_int_off(QTestState *qts, QGuestAllocator *alloc, uint32_t irq);
int qrtas_change_msi(QTestState *qts, QGuestAllocator *alloc, uint64_t buid,
                     uint32_t addr, uint32_t func, uint32_t num_irqs);
int qrtas_query_irq_number(QTestState *qts, QGuestAllocator *alloc,
                           uint64_t buid, uint32_t addr, int offset);

#endif /* LIBQOS_RTAS_H */
