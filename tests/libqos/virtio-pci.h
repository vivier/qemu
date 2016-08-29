/*
 * libqos virtio PCI definitions
 *
 * Copyright (c) 2014 Marc Marí
 *
 * This work is licensed under the terms of the GNU GPL, version 2 or later.
 * See the COPYING file in the top-level directory.
 */

#ifndef LIBQOS_VIRTIO_PCI_H
#define LIBQOS_VIRTIO_PCI_H

#include "libqos/virtio.h"
#include "libqos/pci.h"

typedef struct QVirtioPCIDevice {
    QVirtioDevice vdev;
    QPCIDevice *pdev;
    QPCIBar bar;
    uint16_t config_msix_entry;
} QVirtioPCIDevice;

typedef struct QVirtQueuePCI {
    QVirtQueue vq;
    uint16_t msix_entry;
} QVirtQueuePCI;

extern const QVirtioBus qvirtio_pci;

QVirtioPCIDevice *qvirtio_pci_device_find(QPCIBus *bus, uint16_t device_type);
QVirtioPCIDevice *qvirtio_pci_device_find_slot(QPCIBus *bus,
                                               uint16_t device_type, int slot);
void qvirtio_pci_device_free(QVirtioPCIDevice *dev);

void qvirtio_pci_device_enable(QVirtioPCIDevice *d);
void qvirtio_pci_device_disable(QVirtioPCIDevice *d);

void qvirtqueue_pci_msix_alloc_irqs(QVirtioPCIDevice *d,
                                    QGuestAllocator *alloc, int num_irqs);
void qvirtio_pci_set_msix_configuration_vector(QVirtioPCIDevice *d,
                                               uint16_t entry);
void qvirtqueue_pci_msix_setup(QVirtioPCIDevice *d, QVirtQueuePCI *vqpci,
                               uint16_t entry);
#endif
