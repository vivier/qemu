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
#include "qgraph.h"

static void qpci_pc_register_nodes(void)
{
    qos_node_create_driver("pcie-bus-pc", NULL);
    qos_node_produces("pcie-bus-pc", "pcie-bus");
}

libqos_init(qpci_pc_register_nodes);
