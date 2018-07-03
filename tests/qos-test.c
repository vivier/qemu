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
#include "qapi/qmp/qdict.h"
#include "qapi/qmp/qstring.h"
#include "qapi/qmp/qlist.h"
#include "libqos/malloc.h"
#include "libqos/qgraph.h"
#include "libqos/qgraph_extra.h"

/**
 * create_machine_name(): appends the architecture to @name if
 * @is_machine is valid.
 */
static void create_machine_name(const char **name, bool is_machine)
{
    const char *arch;
    if (!is_machine) {
        return;
    }
    arch = qtest_get_arch();
    *name = g_strconcat(arch, "/", *name, NULL);
}

/**
 * destroy_machine_name(): frees the given @name if
 * @is_machine is valid.
 */
static void destroy_machine_name(const char *name, bool is_machine)
{
    if (!is_machine) {
        return;
    }
    g_free((char *)name);
}

/**
 * apply_to_qlist(): using QMP queries QEMU for a list of
 * machines and devices available, and sets the respective node
 * as TRUE. If a node is found, also all its produced and contained
 * child are marked available.
 *
 * See qos_graph_node_set_availability() for more info
 */
static void apply_to_qlist(QList *list, bool is_machine)
{
    const QListEntry *p;
    const char *name;
    QDict *minfo;
    QObject *qobj;
    QString *qstr;

    for (p = qlist_first(list); p; p = qlist_next(p)) {
        minfo = qobject_to(QDict, qlist_entry_obj(p));
        g_assert(minfo);
        qobj = qdict_get(minfo, "name");
        g_assert(qobj);
        qstr = qobject_to(QString, qobj);
        g_assert(qstr);
        name = qstring_get_str(qstr);
        create_machine_name(&name, is_machine);
        qos_graph_node_set_availability(name, TRUE);
        destroy_machine_name(name, is_machine);
        qobj = qdict_get(minfo, "alias");
        if (qobj) {
            g_assert(qobj);
            qstr = qobject_to(QString, qobj);
            g_assert(qstr);
            name = qstring_get_str(qstr);
            create_machine_name(&name, is_machine);
            qos_graph_node_set_availability(name, TRUE);
            destroy_machine_name(name, is_machine);
        }
    }
}

/**
 * qos_set_machines_devices_available(): sets availability of qgraph
 * machines and devices.
 *
 * This function firstly starts QEMU with "-machine none" option,
 * and then executes the QMP protocol asking for the list of devices
 * and machines available.
 *
 * for each of these items, it looks up the corresponding qgraph node,
 * setting it as available. The list currently returns all devices that
 * are either machines or QEDGE_CONSUMED_BY other nodes.
 * Therefore, in order to mark all other nodes, it recursively sets
 * all its QEDGE_CONTAINS and QEDGE_PRODUCES child as available too.
 */
static void qos_set_machines_devices_available(void)
{
    QDict *response;
    QDict *args = qdict_new();
    QList *list;

    qtest_start("-machine none");
    response = qmp("{ 'execute': 'query-machines' }");
    g_assert(response);
    list = qdict_get_qlist(response, "return");
    g_assert(list);

    apply_to_qlist(list, TRUE);

    qobject_unref(response);

    qdict_put_bool(args, "abstract", TRUE);
    qdict_put_str(args, "implements", "device");

    response = qmp("{'execute': 'qom-list-types',"
                   " 'arguments': %p }", args);
    g_assert(qdict_haskey(response, "return"));
    list = qdict_get_qlist(response, "return");

    apply_to_qlist(list, FALSE);

    qtest_end();
    qobject_unref(response);

}

/**
 * allocate_objects(): given an array of nodes @arg,
 * walks the path invoking all constructors and
 * passing the corresponding parameter in order to
 * continue the objects allocation.
 * Once the test is reached, its function is executed.
 *
 * Since only the machine and QEDGE_CONSUMED_BY nodes actually
 * allocate something in the constructor, a garbage collector
 * saves their pointer in an array, so that after execution
 * they can be safely free'd.
 *
 * Note: as specified in walk_path() too, @arg is an array of
 * char *, where arg[0] is a pointer to the command line
 * string that will be used to properly start QEMU when executing
 * the test, and the remaining elements represent the actual objects
 * that will be allocated.
 */
static void allocate_objects(const void *arg)
{
    QOSGraphObject *garbage_collector[(QOS_PATH_MAX_ELEMENT_SIZE * 2)];
    int g_size = 0;
    QOSEdgeType etype;
    QOSGraphEdge * edge = NULL;
    QOSGraphNode *node, *test_node;
    QOSGraphObject *o;
    QGuestAllocator *machine_o = NULL;
    int current = 1, has_to_allocate = 0;
    void *obj = NULL;
    char **path = (char **) arg;

    node = qos_graph_get_node(path[current]);

    test_node = qos_graph_get_node(path[(g_strv_length(path) - 1)]);
    if (test_node->u.test.before) {
        test_node->u.test.before(&path[0]);
    }
    
    while (current < QOS_PATH_MAX_ELEMENT_SIZE) {

        if (node->type == QNODE_MACHINE) {
            global_qtest = qtest_start(path[0]);

            obj = node->u.machine.constructor();
            o = obj;
            if (o->get_driver) {
                machine_o = o->get_driver(obj, "guest_allocator");
            } else {
                printf("Warning: machine %s does not produce"
                       "guest_allocator\n", node->name);
            }
            garbage_collector[g_size++] = obj;

        } else if (has_to_allocate && node->type == QNODE_DRIVER) {
            obj = node->u.driver.constructor(obj, machine_o,
                                             qos_graph_get_edge_arg(edge));
            garbage_collector[g_size++] = obj;

        } else if (!path[(current + 1)] && node->type == QNODE_TEST) {
            g_assert(test_node == node);
            node->u.test.function(obj, node->u.test.arg, machine_o);
            break;
        }

        edge = qos_graph_get_edge(path[current], path[(current + 1)]);
        etype = qos_graph_get_edge_type(path[current], path[(current + 1)]);
        current++;
        node = qos_graph_get_node(path[current]);

        o = obj;

        switch (etype) {
        case QEDGE_PRODUCES:
            obj = o->get_driver(obj, path[current]);
            break;
        case QEDGE_CONSUMED_BY:
            has_to_allocate = 1;
            break;
        case QEDGE_CONTAINS:
            obj = o->get_device(obj, path[current]);
            break;
        }

    }

    if (test_node->u.test.after) {
        test_node->u.test.after();
    }

    g_free(path[0]);
    g_free(path);
    for (; g_size >= 0; g_size--) {
        garbage_collector[g_size]->destructor(garbage_collector[g_size]);
    }
    qtest_end();
}

/*
 * in this function, 2 path will be built:
 * str_path, a one-string path (ex "pc/i440FX-pcihost/...")
 * ro_path, a string-array path (ex [0] = "pc", [1] = "i440FX-pcihost").
 *
 * str_path will be only used to build the test name, and won't need the
 * architecture name at beginning, since it will be added by qtest_add_func().
 *
 * ro_path is used to allocate all constructors of the path nodes.
 * Each name in this array except position 0 must correspond to a valid
 * QOSGraphNode name.
 * Position 0 is special, initially contains just the <machine> name of
 * the node, (ex for "x86_64/pc" it will be "pc"), used to build the test
 * path (see below). After it will contain the command line used to start
 * qemu with all required devices.
 *
 * Note that the machine node name must be with format <arch>/<machine>
 * (ex "x86_64/pc"), because it will identify the node "x86_64/pc"
 * and start QEMU with "-M pc". For this reason,
 * when building str_path, ro_path
 * initially contains the <machine> at position 0 ("pc"),
 * and the node name at position 1 (<arch>/<machine>)
 * ("x86_64/pc"), followed by the rest of the nodes.
 */
static void walk_path(QOSGraphNode *orig_path, int len)
{
    QOSGraphNode *path;
    /* twice QOS_PATH_MAX_ELEMENT_SIZE since each edge can have its arg */
    char **ro_path = g_new0(char *, (QOS_PATH_MAX_ELEMENT_SIZE * 2));
    int ro_path_size = 0;
    char *machine = NULL, *arch = NULL, *tmp_cmd = NULL, *str_path;
    char *tmp = orig_path->name, *gfreed;
    GString *cmd_line = g_string_new("");

    do {
        path = qos_graph_get_node(tmp);
        tmp = qos_graph_get_edge_dest(path->path_edge);

        if (path->type == QNODE_MACHINE) {
            qos_separate_arch_machine(path->name, &arch, &machine);
            ro_path[ro_path_size++] = arch;
            ro_path[ro_path_size++] = machine;
            g_string_append_printf(cmd_line, "%s ", path->command_line);
        } else {

            /* append node command line + previous edge command line */
            if (path->command_line && tmp_cmd) {
                g_string_append(cmd_line, path->command_line);
                g_string_append_printf(cmd_line, "%s ", tmp_cmd);
            }

            /* detect if edge has command line args */
            ro_path[ro_path_size++] = path->name;
            tmp_cmd = qos_graph_get_edge_cmd_line(path->path_edge);
        }

    } while (path->path_edge);


    /* here position 0 has <arch>/<machine>, position 1 <machine>.
     * the path must not have the <arch>, that's why ro_path  + 1
     */
    str_path = g_strjoinv("/", (ro_path + 1));
    gfreed = g_string_free(cmd_line, FALSE);
    /* put arch/machine in position 1 so allocate_objects can do its work
     * and add the command line at position 0.
     */
    ro_path[0] = g_strdup(gfreed);
    ro_path[1] = arch;

    qtest_add_data_func(str_path, ro_path, allocate_objects);
    g_free(str_path);
}

/**
 * main(): heart of the qgraph framework.
 *
 * - Initializes the glib test framework
 * - Creates the graph by invoking the various _init constructors
 * - Starts QEMU to mark the available devices
 * - Walks the graph, and each path is added to
 *   the glib test framework (walk_path)
 * - Runs the tests, calling allocate_object() and allocating the
 *   machine/drivers/test objects
 * - Cleans up everything
 */
int main(int argc, char **argv)
{
    g_test_init(&argc, &argv, NULL);
    qos_graph_init();
    module_call_init(MODULE_INIT_LIBQOS);
    qos_set_machines_devices_available();

    qos_graph_foreach_test_path(walk_path);
    g_test_run();
    qos_graph_destroy();
    return 0;
}
