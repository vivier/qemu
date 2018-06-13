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

#ifndef QGRAPH_H
#define QGRAPH_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <gmodule.h>
#include <glib.h>
#include "qemu/module.h"
#include "malloc.h"

/* maximum path length */
#define QOS_PATH_MAX_ELEMENT_SIZE 50

typedef struct QOSGraphObject QOSGraphObject;
typedef struct QOSGraphNode QOSGraphNode;
typedef struct QOSGraphEdge QOSGraphEdge;
typedef struct QOSGraphNodeOptions QOSGraphNodeOptions;
typedef struct QOSGraphEdgeOptions QOSGraphEdgeOptions;
typedef struct QOSGraphTestOptions QOSGraphTestOptions;

typedef void *(*QOSCreateDriverFunc) (void *parent, QGuestAllocator *alloc,
                                      void *addr);
typedef void *(*QOSCreateMachineFunc) (void);
typedef void (*QOSTestFunc) (void *parent, void *arg, QGuestAllocator *alloc);

typedef void (*QOSTestCallback) (QOSGraphNode *path, int len);

typedef void *(*QOSGetDriver) (void *object, const char *interface);
typedef QOSGraphObject *(*QOSGetDevice) (void *object, const char *name);
typedef void (*QOSDestructorFunc) (QOSGraphObject *object);

typedef void (*QOSBeforeTest) (char **cmd_line);
typedef void (*QOSAfterTest) (void);

/**
 * SECTION:qgraph.h
 * @title: Qtest Driver Framework
 * @short_description: interfaces to organize drivers and tests
 *                     as nodes in a graph
 *
 * This Qgraph API provides all basic functions to create a graph
 * and instantiate nodes representing machines, drivers and tests
 * representing their relations with CONSUMES, PRODUCES, and CONTAINS
 * edges. 
 * 
 * The idea is to have a framework where each test asks for a specific
 * driver, and the framework takes care of allocating the proper devices
 * required and passing the correct command line arguments to QEMU.
 * 
 * A node can be of four types:
 * - QNODE_MACHINE:   for example "arm/raspi2"
 * - QNODE_DRIVER:    for example "generic-sdhci"
 * - QNODE_INTERFACE: for example "sdhci" (interface for all "-sdhci" drivers)
 * - QNODE_TEST:      for example "sdhci-test", consumes an interface and tests
 *                    the functions provided
 * 
 * Notes for the nodes:
 * - QNODE_MACHINE: each machine struct must have a QGuestAllocator and 
 *                  implement get_driver to return the allocator passing
 *                  "guest_allocator"
 * - QNODE_DRIVER:  driver names must be unique, and machines and nodes
 *                  planned to be "consumed" by other nodes must match QEMU
 *                  drivers name, otherwise they won't be discovered
 * 
 * An edge relation between two nodes (drivers or machines) X and Y can be:
 * - X CONSUMES Y: Y can be plugged into X
 * - X PRODUCES Y: X provides the interface Y
 * - X CONTAINS Y: Y is part of X component
 * 
 * Basic framework steps are the following:
 * - All nodes and edges are created in their respective machine/driver/test files
 * - The framework starts QEMU and asks for a list of available devices
 *   and machines (note that only machines and "consumed" nodes are mapped
 *   1:1 with QEMU devices)
 * - The framework walks the graph starting from the available machines and
 *   performs a Depth First Search for tests
 * - Once a test is found, the path is walked again and all drivers are
 *   allocated accordingly and the final interface is passed to the test
 * - The test is executed
 * - Unused objects are cleaned and the path discovery is continued
 * 
 * Depending on the QEMU binary used, only some drivers/machines will be available
 * and only test that are reached by them will be executed.
 *
 * <example>
 *   <title>Creating new driver an its interface</title>
 *   <programlisting>
 * #include "qgraph.h"

 struct My_driver {
     QOSGraphObject obj;
     Node_produced prod;
     Node_contained cont;
 }
 *
 static void my_destructor(QOSGraphObject *obj)
 {
     g_free(obj);
 }

 static void my_get_driver(void *object, const char *interface) {
     My_driver *dev = object;
     if (!g_strcmp0(interface, "my_interface")) {
        return &dev->prod;
    }
    abort();
 }

 static void my_get_device(void *object, const char *device) {
     My_driver *dev = object;
     if (!g_strcmp0(device, "my_driver_contained")) {
        return &dev->cont;
    }
    abort();
 }

 * static void *my_driver_constructor(void *node_consumed,
 *                                    QOSGraphObject *alloc)
 * {
 *     My_driver dev = g_new(My_driver, 1);
        // get the node pointed by the produce edge
        dev->obj.get_driver = my_get_driver;
        // get the node pointed by the contains
        dev->obj.get_device = my_get_device;
        // free the object
        dev->obj.destructor = my_destructor;
        do_something_with_node_consumed(node_consumed);
        // set all fields of contained device
        init_contained_device(&dev->cont); 
        return &dev->obj;
 * }
 *
 static void register_my_driver(void)
 {
     qos_node_create_driver("my_driver", my_driver_constructor);
     // interface does not have to be in this file!
     qos_node_create_interface("my_interface");
     // contained drivers don't need a constructor, 
     // they will be init by the parent.
     qos_node_create_driver("my_driver_contained", NULL);

    // For the sake of this example, assume machine x86_64/pc contains 
    // "other_node".
    // This relation, along with the machine and "other_node" creation,
    // should be defined in the x86_64_pc-machine.c file.
    // "my_driver" will then consume "other_node"
    qos_node_contains("my_driver", "my_driver_contained");
    qos_node_produces("my_driver", "my_interface");
    qos_node_consumes("my_driver", "other_node");
 }
 *   </programlisting>
 * </example>
 *
 * In the above example, all possible types of relations are created: 
 * node "my_driver" consumes, contains and produces other nodes. 
 * more specifically:
 * x86_64/pc -->contains--> other_node <--consumes-- my_driver
 *                                                       |
 *                      my_driver_contained <--contains--+
 *                                                       |
 *                             my_interface <--produces--+
 * 
 * or inverting the consumes edge in consumed_by:
 *
 * x86_64/pc -->contains--> other_node --consumed_by--> my_driver
 *                                                           |
 *                          my_driver_contained <--contains--+
 *                                                           |
 *                                 my_interface <--produces--+
 * 
 * <example>
 *   <title>Creating new test</title>
 *   <programlisting>
 * #include "qgraph.h"
 *
 * static void my_test_function(void *obj, void *data)
 * {
 *    Node_produced *interface_to_test = obj;
 *    // test interface_to_test
 * }
 * 
 * static void register_my_test(void)
 * {
 *    qos_add_test("my_interface", "my_test", my_test_function);
 * }
 * 
 * libqos_init(register_my_test);
 * 
 *   </programlisting>
 * </example>
 *
 * Here a new test is created, consuming "my_interface" node
 * and creating a valid path from a machine to a test. 
 * Final graph will be like this:
 * x86_64/pc -->contains--> other_node <--consumes-- my_driver
 *                                                        |
 *                       my_driver_contained <--contains--+
 *                                                        |
 *        my_test --consumes--> my_interface <--produces--+
 * 
 * or inverting the consumes edge in consumed_by:
 *
 * x86_64/pc -->contains--> other_node --consumed_by--> my_driver
 *                                                           |
 *                          my_driver_contained <--contains--+
 *                                                           |
 *        my_test <--consumed_by-- my_interface <--produces--+
 * 
 * Assuming there the binary is 
 * QTEST_QEMU_BINARY=x86_64-softmmu/qemu-system-x86_64
 * a valid test path will be:
 * "/x86_64/pc/other_node/my_driver/my_interface/my_test".
 * 
 * Additional examples are also in libqos/test-qgraph.c 
 */

/**
 * Node options to be passed to the machine/driver/test *_args function.
 */
struct QOSGraphNodeOptions {
    const char *extra_args; /* optional extra command line */
};

/**
 * Edge options to be passed to the contains/consumes *_args function.
 */
struct QOSGraphEdgeOptions {
    void *arg;           /* optional arg that will be used by dest edge */
    uint32_t size_arg;   /* optional arg size that will be used by dest edge */
    const char *cmd_line;/* optional additional command line for dest edge */
};

struct QOSGraphTestOptions {
    void *test_arg;         /* used by test, the optional data arg */
    uint32_t size_test_arg; /* used by test, the optional data arg size */
    const char *test_extra_args; /* extra args for test (add device) */
    const char *edge_args;  /* args for the QEDGE_CONSUMES edge */
    QOSBeforeTest before;
    QOSAfterTest after;
};

/**
 * Each driver, test or machine will have this as first field.
 * Depending on the edge, the node will call the corresponding
 * function when walking the path.
 *
 * QOSGraphObject also provides a destructor, used to deallocate the
 * after the test has been executed.
 */
struct QOSGraphObject {
    /* for produces, returns void * */
    QOSGetDriver get_driver;
    /* for contains, returns a QOSGraphObject * */
    QOSGetDevice get_device;
    /* destroy this QOSGraphObject */
    QOSDestructorFunc destructor;
};

/**
 * qos_graph_init(): initialize the framework, creates two hash
 * tables: one for the nodes and another for the edges.
 */
void qos_graph_init(void);

/**
 * qos_graph_destroy(): deallocates all the hash tables,
 * freeing all nodes and edges.
 */
void qos_graph_destroy(void);

/**
 * qos_node_destroy(): removes and frees a node from the,
 * nodes hash table.
 */
void qos_node_destroy(void *key);

/**
 * qos_edge_destroy(): removes and frees an edge from the,
 * edges hash table.
 */
void qos_edge_destroy(void *key);

/**
 * qos_add_test(): adds a test node @name to the nodes hash table.
 *
 * The test will consume a @driver node, and once the
 * graph walking algorithm has found it, the @test_func will be
 * executed.
 */
void qos_add_test(const char *name, const char *driver, QOSTestFunc test_func);

/**
 * qos_add_test_args(): same as qos_add_test, with the possibility to
 * add an optional @opts (see %QOSGraphNodeOptions).
 */
void qos_add_test_args(const char *name, const char *driver,
                       QOSTestFunc test_func,
                       QOSGraphTestOptions * opts);

/**
 * qos_node_create_machine(): creates the machine @name and
 * adds it to the node hash table.
 *
 * This node will be of type QNODE_MACHINE and have @function
 * as constructor
 */
void qos_node_create_machine(const char *name, QOSCreateMachineFunc function);

/**
 * qos_node_create_machine_args(): same as qos_node_create_machine,
 * but with the possibility to add an optional @opts (see %QOSGraphNodeOptions)
 */
void qos_node_create_machine_args(const char *name,
                                  QOSCreateMachineFunc function,
                                  QOSGraphNodeOptions *opts);

/**
 * qos_node_create_driver(): creates the driver @name and
 * adds it to the node hash table.
 *
 * This node will be of type QNODE_DRIVER and have @function
 * as constructor
 */
void qos_node_create_driver(const char *name, QOSCreateDriverFunc function);

/**
 * qos_node_create_driver_args(): same as qos_node_create_driver,
 * but with the possibility to add an optional @opts (see %QOSGraphNodeOptions)
 */
void qos_node_create_driver_args(const char *name,
                                 QOSCreateDriverFunc function,
                                 QOSGraphNodeOptions *opts);

/**
 * qos_node_create_interface(): creates the interface @name and
 * adds it to the node hash table.
 *
 * This node will be of type QNODE_INTERFACE and won't have
 * any constructor
 */
void qos_node_create_interface(const char *name);

/**
 * qos_node_contains(): creates the edge QEDGE_CONTAINS and
 * adds it to the edge list mapped to @container in the
 * edge hash table.
 *
 * This edge will have @container as source and @contained as destination.
 */
void qos_node_contains(const char *container, const char *contained);

/**
 * qos_node_contains_args(): same as qos_node_contains,
 * but with the possibility to add an optional @opts (see %QOSGraphEdgeOptions)
 */
void qos_node_contains_args(const char *container, const char *contained,
                            QOSGraphEdgeOptions *opts);

/**
 * qos_node_produces(): creates the edge QEDGE_PRODUCES and
 * adds it to the edge list mapped to @producer in the
 * edge hash table.
 *
 * This edge will have @producer as source and @produced as destination.
 */
void qos_node_produces(const char *producer, const char *produced);

/**
 * qos_node_consumes(): creates the edge QEDGE_CONSUMED_BY and
 * adds it to the edge list mapped to @consumed in the
 * edge hash table.
 *
 * This edge will have @consumed as source and @consumer as destination.
 */
void qos_node_consumes(const char *consumer, const char *consumed);

/**
 * qos_node_consumes_args(): same as qos_node_consumes,
 * but with the possibility to add an optional @opts (see %QOSGraphEdgeOptions)
 */
void qos_node_consumes_args(const char *consumer, const char *consumed,
                            QOSGraphEdgeOptions *opts);

/**
 * qos_graph_node_set_availability(): sets the node identified
 * by @node with availability @av.
 */
void qos_graph_node_set_availability(const char *node, bool av);

#endif
