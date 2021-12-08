/*
 * Virtio net PCI Device
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#ifndef HW_VIRTIO_NET_PCI_H
#define HW_VIRTIO_NET_PCI_H

#include "hw/virtio/virtio-pci.h"
#include "hw/virtio/virtio-net.h"
#include "qom/object.h"

typedef struct VirtIONetPCI VirtIONetPCI;

/*
 * virtio-net-pci: This extends VirtioPCIProxy.
 */
#define TYPE_VIRTIO_NET_PCI "virtio-net-pci-base"
DECLARE_INSTANCE_CHECKER(VirtIONetPCI, VIRTIO_NET_PCI,
                         TYPE_VIRTIO_NET_PCI)

struct VirtIONetPCI {
    VirtIOPCIProxy parent_obj;
    VirtIONet vdev;
};

#endif /* HW_VIRTIO_NET_PCI_H */
