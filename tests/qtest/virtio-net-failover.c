#include "qemu/osdep.h"
#include "libqos/libqtest.h"
#include "libqos/pci.h"
#include "libqos/pci-pc.h"
#include "qapi/qmp/qdict.h"
#include "qapi/qmp/qlist.h"
#include "libqos/malloc-pc.h"
#include "libqos/virtio-pci.h"
#include "standard-headers/linux/virtio_net.h"

static int qemu_printf(const char *fmt, ...)
{
    va_list ap;
    int ret;

    va_start(ap, fmt);
    ret = vfprintf(stderr, fmt, ap);
    va_end(ap);
    return ret;
}

static void test_error_id(void)
{
    QTestState *qts;
    QDict *resp;
    QDict *err;

    qts = qtest_init("-M q35 -device virtio-net,id=standby0,failover=on");

    resp = qtest_qmp(qts, "{'execute': 'device_add',"
                          "'arguments': {"
                          "'driver': 'virtio-net',"
                          "'failover_pair_id': 'standby0'"
                          "} }");
    g_assert(qdict_haskey(resp, "error"));

    err = qdict_get_qdict(resp, "error");
    g_assert(qdict_haskey(err, "desc"));

    g_assert_cmpstr(qdict_get_str(err, "desc"), ==, "Device with failover_pair_id needs to have id");

    qobject_unref(resp);

    qtest_quit(qts);
}

static void test_error_pcie(void)
{
    QTestState *qts;
    QDict *resp;
    QDict *err;

    qts = qtest_init("-M q35 -device virtio-net,id=standby0,failover=on");
    resp = qtest_qmp(qts, "{'execute': 'device_add',"
                          "'arguments': {"
                          "'driver': 'virtio-net',"
                          "'id': 'primary0',"
                          "'failover_pair_id': 'standby0'"
                          "} }");
    g_assert(qdict_haskey(resp, "error"));

    err = qdict_get_qdict(resp, "error");
    g_assert(qdict_haskey(err, "desc"));

    g_assert_cmpstr(qdict_get_str(err, "desc"), ==, "Bus 'pcie.0' does not support hotplugging");

    qobject_unref(resp);

    qtest_quit(qts);
}

static QDict *find_device(QDict *bus, const char *name)
{
    QList *devices;
    const QObject *obj;

    devices = qdict_get_qlist(bus, "devices");
    if (devices == NULL) {
        return NULL;
    }

    while ((obj = qlist_pop(devices))) {
        QDict *device;

        device = qobject_to(QDict, obj);

        if (!qdict_haskey(device, "qdev_id")) {
            continue;
        }

        if (strcmp(qdict_get_str(device, "qdev_id"), name) == 0) {
            qobject_ref(device);
            return device;
        }
    }

    return NULL;
}

static QDict *get_bus(QTestState *qts, int num)
{
    QObject *obj;
    QDict *resp;
    QList *ret;

    resp = qtest_qmp(qts, "{ 'execute': 'query-pci' }");
    g_assert(qdict_haskey(resp, "return"));

    ret = qdict_get_qlist(resp, "return");
    g_assert_nonnull(ret);

    while ((obj = qlist_pop(ret))) {
        QDict *bus;

        bus = qobject_to(QDict, obj);
        if (!qdict_haskey(bus, "bus")) {
            continue;
        }
        if (qdict_get_int(bus, "bus") == num) {
            qobject_ref(bus);
            qobject_unref(resp);
            return bus;
        }
    }
    qobject_unref(resp);

    return NULL;
}

static char *get_mac(QTestState *qts, const char *name)
{
    QDict *resp;
    char *mac;

    resp = qtest_qmp(qts, "{ 'execute': 'qom-get', "
                     "'arguments': { "
                     "'path': %s, "
                     "'property': 'mac' } }", name);

    g_assert(qdict_haskey(resp, "return"));

    mac = g_strdup( qdict_get_str(resp, "return"));

    qobject_unref(resp);

    return mac;
}

static void test_on(void)
{
    QTestState *qts;
    QDict *bus;
    QDict *device;
    char *mac;

    qts = qtest_init("-M q35 -nodefaults "
                     "-netdev user,id=hs0 "
                     "-device virtio-net,bus=pcie.0,id=standby0,failover=on,netdev=hs0,mac=52:54:00:11:11:11 "
                     "-device virtio-net,bus=pcie.0,id=primary0,failover_pair_id=standby0,netdev=hs1,mac=52:54:00:22:22:22");

    bus = get_bus(qts, 0);

    device = find_device(bus, "standby0");
    g_assert_nonnull(device);
    qobject_unref(device);

    device = find_device(bus, "primary0");
    g_assert_null(device);
    qobject_unref(device);

    qobject_unref(bus);

    mac = get_mac(qts, "/machine/peripheral/standby0");
    g_assert_cmpstr(mac, ==, "52:54:00:11:11:11");
    g_free(mac);

    qtest_quit(qts);
}

static void test_off(void)
{
    QTestState *qts;
    QDict *bus;
    QDict *device;
    char *mac;

    qts = qtest_init("-M q35 -nodefaults "
                     "-netdev user,id=hs0 "
                     "-device virtio-net,bus=pcie.0,id=standby0,failover=off,netdev=hs0,mac=52:54:00:11:11:11 "
                     "-netdev user,id=hs1 "
                     "-device virtio-net,bus=pcie.0,id=primary0,failover_pair_id=standby0,netdev=hs1,mac=52:54:00:22:22:22");

    bus = get_bus(qts, 0);

    device = find_device(bus, "standby0");
    g_assert_nonnull(device);
    qobject_unref(device);

    device = find_device(bus, "primary0");
    g_assert_nonnull(device);
    qobject_unref(device);

    qobject_unref(bus);

    mac = get_mac(qts, "/machine/peripheral/standby0");
    g_assert_cmpstr(mac, ==, "52:54:00:11:11:11");
    g_free(mac);

    mac = get_mac(qts, "/machine/peripheral/primary0");
    g_assert_cmpstr(mac, ==, "52:54:00:22:22:22");
    g_free(mac);

    qtest_quit(qts);
}

static void test_enabled(void)
{
    QTestState *qts;
    QDict *bus;
    QDict *device;
    char *mac;
    QPCIBus *pcibus;
    QGuestAllocator guest_malloc;
    QVirtioPCIDevice *dev;
    uint64_t features;
    //QVirtQueuePCI *tx, *rx;
    QPCIAddress addr;

    qts = qtest_init("-M q35 -nodefaults "
                     "-netdev user,id=hs0 "
                     "-device pcie-root-port,id=root0,addr=0x1,bus=pcie.0,chassis=1 "
                     "-device virtio-net,bus=root0,id=standby0,failover=on,netdev=hs0,mac=52:54:00:11:11:11 "
                     "-netdev user,id=hs1 "
                     "-device pcie-root-port,id=root1,addr=0x2,bus=pcie.0,chassis=2 "
                     "-device virtio-net,bus=root1,id=primary0,failover_pair_id=standby0,netdev=hs1,mac=52:54:00:11:11:11 "
                     "-trace enable=pci*");
    pc_alloc_init(&guest_malloc, qts, 0);
    pcibus = qpci_new_pc(qts, &guest_malloc);

    g_assert(qpci_secondary_buses_init(pcibus) == 2);

    bus = get_bus(qts, 0);
    dump_qdict(4, bus, qemu_printf);
    addr.devfn = QPCI_DEVFN(1 << 5, 0);
    dev = virtio_pci_new(pcibus, &addr);
    g_assert_nonnull(dev);
    qvirtio_pci_device_enable(dev);
    if (0) fprintf(stderr, "%s\n", qtest_hmp(qts, "info mtree"));
    qvirtio_start_device(&dev->vdev);
return;
    features = qvirtio_get_features(&dev->vdev);
    features = features & ~(QVIRTIO_F_BAD_FEATURE |
                            (1ull << VIRTIO_RING_F_INDIRECT_DESC) |
                            (1ull << VIRTIO_RING_F_EVENT_IDX));
    qvirtio_set_features(&dev->vdev, features);
    //rx = (QVirtQueuePCI *)qvirtqueue_setup(&dev->vdev, &guest_malloc, 0);
    //tx = (QVirtQueuePCI *)qvirtqueue_setup(&dev->vdev, &guest_malloc, 1);
    qvirtio_set_driver_ok(&dev->vdev);

    qtest_qmp_eventwait(qts, "FAILOVER_NEGOTIATED");

    bus = get_bus(qts, 0);
    dump_qdict(4, bus, qemu_printf);

return;
    device = find_device(bus, "standby0");
    g_assert_nonnull(device);
    qobject_unref(device);

    device = find_device(bus, "primary0");
    g_assert_nonnull(device);
    qobject_unref(device);

    qobject_unref(bus);

    mac = get_mac(qts, "/machine/peripheral/standby0");
    g_assert_cmpstr(mac, ==, "52:54:00:11:11:11");
    g_free(mac);

    mac = get_mac(qts, "/machine/peripheral/primary0");
    g_assert_cmpstr(mac, ==, "52:54:00:11:11:11");
    g_free(mac);

    qpci_free_pc(pcibus);
    alloc_destroy(&guest_malloc);
    qtest_quit(qts);
}

int main(int argc, char **argv)
{
    g_test_init(&argc, &argv, NULL);

    qtest_add_func("failover-virtio-net/params/error/id", test_error_id);
    qtest_add_func("failover-virtio-net/params/error/pcie", test_error_pcie);
    qtest_add_func("failover-virtio-net/params/error/on", test_on);
    qtest_add_func("failover-virtio-net/params/error/off", test_off);
    qtest_add_func("failover-virtio-net/params/error/enabled", test_enabled);

    return g_test_run();
}
