/*
 * libqos driver framework
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License version 2.1 as published by the Free Software Foundation.
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
#include "pci-pc.h"
#include "qemu/module.h"
#include "malloc-pc.h"

typedef struct QX86Q35Machine QX86Q35Machine;
typedef struct q35_pcihost q35_pcihost;

struct q35_pcihost {
    QOSGraphObject obj;
    QPCIBusPC pci;
};

struct QX86Q35Machine {
    QOSGraphObject obj;
    QGuestAllocator alloc;
    q35_pcihost bridge;
};

/* q35_pcihost */

static QOSGraphObject *q35_host_get_device(void *obj, const char *device)
{
    q35_pcihost *host = obj;
    if (!g_strcmp0(device, "pcie-bus-pc")) {
        return &host->pci.obj;
    }
    fprintf(stderr, "%s not present in q35-pcihost\n", device);
    g_assert_not_reached();
}

static void qos_create_q35_host(q35_pcihost *host,
                                   QTestState *qts,
                                   QGuestAllocator *alloc)
{
    host->obj.get_device = q35_host_get_device;
    qpci_init_pc(&host->pci, qts, alloc);
}

/* x86_64/q35 machine */

static void q35_destructor(QOSGraphObject *obj)
{
    QX86Q35Machine *machine = (QX86Q35Machine *) obj;
    alloc_destroy(&machine->alloc);
}

static void *q35_get_driver(void *object, const char *interface)
{
    QX86Q35Machine *machine = object;
    if (!g_strcmp0(interface, "memory")) {
        return &machine->alloc;
    }

    fprintf(stderr, "%s not present in x86_64/q35\n", interface);
    g_assert_not_reached();
}

static QOSGraphObject *q35_get_device(void *obj, const char *device)
{
    QX86Q35Machine *machine = obj;
    if (!g_strcmp0(device, "q35-pcihost")) {
        return &machine->bridge.obj;
    }

    fprintf(stderr, "%s not present in x86_64/q35\n", device);
    g_assert_not_reached();
}

static void *qos_create_machine_q35(QTestState *qts)
{
    QX86Q35Machine *machine = g_new0(QX86Q35Machine, 1);
    machine->obj.get_device = q35_get_device;
    machine->obj.get_driver = q35_get_driver;
    machine->obj.destructor = q35_destructor;
    pc_alloc_init(&machine->alloc, qts, ALLOC_NO_FLAGS);
    qos_create_q35_host(&machine->bridge, qts, &machine->alloc);

    return &machine->obj;
}

static void q35_machine_register_nodes(void)
{
    qos_node_create_machine("i386/q35", qos_create_machine_q35);
    qos_node_contains("i386/q35", "q35-pcihost", NULL);

    qos_node_create_machine("x86_64/q35", qos_create_machine_q35);
    qos_node_contains("x86_64/q35", "q35-pcihost", NULL);

    qos_node_create_driver("q35-pcihost", NULL);
    qos_node_contains("q35-pcihost", "pcie-bus-pc", NULL);
}

libqos_init(q35_machine_register_nodes);
