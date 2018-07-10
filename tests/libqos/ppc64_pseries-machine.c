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
#include "pci-spapr.h"
#include "libqos/malloc-spapr.h"

typedef struct QSPAPR_pci_host QSPAPR_pci_host;
typedef struct Qppc64_pseriesMachine Qppc64_pseriesMachine;

struct QSPAPR_pci_host {
    QOSGraphObject obj;
    QPCIBusSPAPR pci;
};

struct Qppc64_pseriesMachine {
    QOSGraphObject obj;
    QGuestAllocator *alloc;
    QSPAPR_pci_host bridge;
};

/* QSPAPR_pci_host */

static QOSGraphObject *QSPAPR_host_get_device(void *obj, const char *device)
{
    QSPAPR_pci_host *host = obj;
    if (!g_strcmp0(device, "pci-bus-spapr")) {
        return &host->pci.obj;
    }
    printf("%s not present in QSPAPR_pci_host", device);
    abort();
}

static void qos_create_QSPAPR_host(QSPAPR_pci_host *host,
                                   QGuestAllocator *alloc)
{
    host->obj.get_device = QSPAPR_host_get_device;
    qpci_set_spapr(&host->pci, global_qtest, alloc);
}

/* ppc64/pseries machine */

static void spapr_destroy(QOSGraphObject *obj)
{
    Qppc64_pseriesMachine *machine = (Qppc64_pseriesMachine *) obj;
    spapr_alloc_uninit(machine->alloc);
    g_free(obj);
}

static void *spapr_get_driver(void *object, const char *interface)
{
    Qppc64_pseriesMachine *machine = object;
    if (!g_strcmp0(interface, "guest_allocator")) {
        return machine->alloc;
    }

    printf("%s not present in ppc64/pseries", interface);
    abort();
}

static QOSGraphObject *spapr_get_device(void *obj, const char *device)
{
    Qppc64_pseriesMachine *machine = obj;
    if (!g_strcmp0(device, "spapr-pci-host-bridge")) {
        return &machine->bridge.obj;
    }

    printf("%s not present in ppc64/pseries", device);
    abort();
}

static void *qos_create_machine_spapr(void)
{
    Qppc64_pseriesMachine *machine = g_new0(Qppc64_pseriesMachine, 1);
    machine->obj.get_device = spapr_get_device;
    machine->obj.get_driver = spapr_get_driver;
    machine->obj.destructor = spapr_destroy;
    machine->alloc =  spapr_alloc_init_flags(global_qtest,
                                                ALLOC_NO_FLAGS);
    qos_create_QSPAPR_host(&machine->bridge, machine->alloc);

    return &machine->obj;
}

static void spapr_machine(void)
{
    qos_node_create_machine("ppc64/pseries", qos_create_machine_spapr);
    qos_node_create_driver("spapr-pci-host-bridge", NULL);
    qos_node_contains("ppc64/pseries", "spapr-pci-host-bridge");
    qos_node_contains("spapr-pci-host-bridge", "pci-bus-spapr");
}

libqos_init(spapr_machine);

