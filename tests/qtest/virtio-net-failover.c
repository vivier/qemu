#include "qemu/osdep.h"
#include "libqos/libqtest.h"
#include "libqos/pci.h"
#include "libqos/pci-pc.h"
#include "qapi/qmp/qdict.h"
#include "qapi/qmp/qlist.h"
#include "libqos/malloc-pc.h"
#include "libqos/virtio-pci.h"
#include "standard-headers/linux/pci_regs.h"
#include "standard-headers/linux/virtio_net.h"
#include "hw/pci/pci.h"
#include "hw/pci/pci_bridge.h"

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

static void get_pcibus(QPCIBus *bus, int devfn)
{
    QPCIDevice *root;

    root = qpci_device_find(bus, devfn);
    g_assert_nonnull(root);

    g_assert_cmpint(qpci_config_readw(root, PCI_VENDOR_ID), ==,
                    PCI_VENDOR_ID_REDHAT);
    g_assert_cmpint(qpci_config_readw(root, PCI_CLASS_DEVICE), ==,
                    PCI_CLASS_BRIDGE_PCI);

    qpci_config_writeb(root, PCI_SECONDARY_BUS, devfn >> 3);
    qpci_config_writeb(root, PCI_SUBORDINATE_BUS, devfn >> 3);

    g_assert_cmpint(qpci_config_readw(root, PCI_HEADER_TYPE), ==,
                    PCI_HEADER_TYPE_BRIDGE);

    qpci_device_enable(root);
}

static uint8_t qpci_find_resource_reserve_capability(QPCIDevice *dev)
{
    uint16_t device_id;
    uint8_t cap = 0;

    if (qpci_config_readw(dev, PCI_VENDOR_ID) != PCI_VENDOR_ID_REDHAT) {
        return 0;
    }

    device_id = qpci_config_readw(dev, PCI_DEVICE_ID);

    if (device_id != PCI_DEVICE_ID_REDHAT_PCIE_RP &&
        device_id != PCI_DEVICE_ID_REDHAT_BRIDGE) {
        return 0;
    }

    do {
        cap = qpci_find_capability(dev, PCI_CAP_ID_VNDR, cap);
    } while (cap &&
             qpci_config_readb(dev, cap + REDHAT_PCI_CAP_TYPE_OFFSET) != REDHAT_PCI_CAP_RESOURCE_RESERVE);
    if (cap) {
        uint8_t cap_len = qpci_config_readb(dev, cap + PCI_CAP_FLAGS);
        if (cap_len < REDHAT_PCI_CAP_RES_RESERVE_CAP_SIZE) {
            return 0;
        }
    }
    return cap;
}

static void qpci_init_all_buses(QPCIBus *qbus, int bus, int *pci_bus)
{
    QPCIDevice *dev;
    uint16_t class;
    uint8_t pribus, secbus, subbus;
    int i;

    for (i = bus; i < 32; i++ ) {
        dev = qpci_device_find(qbus, QPCI_DEVFN(i, 0));
        if (dev == NULL) {
            continue;
        }
        class = qpci_config_readw(dev, PCI_CLASS_DEVICE);
        if (class == PCI_CLASS_BRIDGE_PCI) {
            qpci_config_writeb(dev, PCI_SECONDARY_BUS, 255);
            qpci_config_writeb(dev, PCI_SUBORDINATE_BUS, 0);
        }
        g_free(dev);
    }

    for (i = bus; i < 32; i++ ) {
        dev = qpci_device_find(qbus, QPCI_DEVFN(i, 0));
	if (dev == NULL) {
            continue;
        }
        class = qpci_config_readw(dev, PCI_CLASS_DEVICE);
        if (class != PCI_CLASS_BRIDGE_PCI) {
            continue;
        }

        pribus = qpci_config_readb(dev, PCI_PRIMARY_BUS);
        if (pribus != bus) {
            qpci_config_writeb(dev, PCI_PRIMARY_BUS, bus);
        }

        secbus = qpci_config_readb(dev, PCI_SECONDARY_BUS);
        (*pci_bus)++;
        if (*pci_bus != secbus) {
            secbus = *pci_bus;
            qpci_config_writeb(dev, PCI_SECONDARY_BUS, secbus);
        }

        subbus = qpci_config_readb(dev, PCI_SUBORDINATE_BUS);
        qpci_config_writeb(dev, PCI_SUBORDINATE_BUS, 255);

        qpci_init_all_buses(qbus, secbus << 5, pci_bus);

        if (subbus != *pci_bus) {
            uint8_t res_bus = *pci_bus;
            uint8_t cap = qpci_find_resource_reserve_capability(dev);

            if (cap) {
                uint32_t tmp_res_bus;

                tmp_res_bus = qpci_config_readl(dev, cap + REDHAT_PCI_CAP_RES_RESERVE_BUS_RES);
                if (tmp_res_bus != (uint32_t)-1) {
                    res_bus = tmp_res_bus & 0xFF;
                    if ((uint8_t)(res_bus + secbus) < secbus ||
                        (uint8_t)(res_bus + secbus) < res_bus) {
                        res_bus = 0;
                    }
                    if (secbus + res_bus > *pci_bus) {
                        res_bus = secbus + res_bus;
                    }
                }
            }
            subbus = res_bus;
            *pci_bus = res_bus;
        }

        qpci_config_writeb(dev, PCI_SUBORDINATE_BUS, subbus);
        g_free(dev);
    }
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
                     "-device virtio-net,bus=root0,id=standby0,failover=off,netdev=hs0,mac=52:54:00:11:11:11 "
                     "-netdev user,id=hs1 "
                     "-device pcie-root-port,id=root1,addr=0x2,bus=pcie.0,chassis=2 "
                     "-device virtio-net,bus=root1,id=primary0,failover_pair_id=standby0,netdev=hs1,mac=52:54:00:11:11:11 "
                     "-trace enable=pci*");
    pc_alloc_init(&guest_malloc, qts, 0);
    pcibus = qpci_new_pc(qts, &guest_malloc);

int nb_bus = 0;
    qpci_init_all_buses(pcibus, 0, &nb_bus);
fprintf(stderr, "nb_bus %d\n", nb_bus);
    if (0) get_pcibus(pcibus, QPCI_DEVFN(1, 0));
    //get_pcibus(pcibus, QPCI_DEVFN(2, 0));

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
