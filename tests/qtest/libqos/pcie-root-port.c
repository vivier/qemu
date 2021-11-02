/*
 * This work is licensed under the terms of the GNU GPL, version 2 or later.
 * See the COPYING file in the top-level directory.
 */

#include "qemu/osdep.h"
#include "qemu/module.h"
#include "libqtest.h"
#include "qgraph.h"

static void qpci_pcie_root_port_register_nodes(void)
{
    QOSGraphEdgeOptions opts = {
        .extra_device_opts = "addr=0x4",
    };

    qos_node_create_driver("pcie-root-port", NULL);
    qos_node_consumes("pcie-root-port", "pcie-bus", &opts);
    qos_node_produces("pcie-root-port", "pci-bus");
}

libqos_init(qpci_pcie_root_port_register_nodes);
