/*
 * QEMU PC System Emulator
 *
 * Copyright (c) 2003-2004 Fabrice Bellard
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <glib.h>

#include "hw/hw.h"
#include "hw/loader.h"
#include "hw/i386/pc.h"
#include "hw/i386/apic.h"
#include "hw/i386/smbios.h"
#include "hw/pci/pci.h"
#include "hw/pci/pci_ids.h"
#include "hw/usb.h"
#include "net/net.h"
#include "hw/boards.h"
#include "hw/ide.h"
#include "sysemu/kvm.h"
#include "hw/kvm/clock.h"
#include "sysemu/sysemu.h"
#include "hw/sysbus.h"
#include "hw/cpu/icc_bus.h"
#include "sysemu/arch_init.h"
#include "sysemu/blockdev.h"
#include "hw/i2c/smbus.h"
#include "hw/xen/xen.h"
#include "exec/memory.h"
#include "exec/address-spaces.h"
#include "hw/acpi/acpi.h"
#include "cpu.h"
#ifdef CONFIG_XEN
#  include <xen/hvm/hvm_info_table.h>
#endif

#define MAX_IDE_BUS 2

static const int ide_iobase[MAX_IDE_BUS] = { 0x1f0, 0x170 };
static const int ide_iobase2[MAX_IDE_BUS] = { 0x3f6, 0x376 };
static const int ide_irq[MAX_IDE_BUS] = { 14, 15 };

static bool smbios_type1_defaults = true;
static bool has_pci_info;
static bool has_acpi_build = true;
/* Make sure that guest addresses aligned at 1Gbyte boundaries get mapped to
 * host addresses aligned at 1Gbyte boundaries.  This way we can use 1GByte
 * pages in the host.
 */
static bool gigabyte_align = true;

/* PC hardware initialisation */
static void pc_init1(QEMUMachineInitArgs *args,
                     MemoryRegion *system_memory,
                     MemoryRegion *system_io,
                     int pci_enabled,
                     int kvmclock_enabled)
{
    int i;
    ram_addr_t below_4g_mem_size, above_4g_mem_size;
    PCIBus *pci_bus;
    ISABus *isa_bus;
    PCII440FXState *i440fx_state;
    int piix3_devfn = -1;
    qemu_irq *cpu_irq;
    qemu_irq *gsi;
    qemu_irq *i8259;
    qemu_irq *smi_irq;
    GSIState *gsi_state;
    DriveInfo *hd[MAX_IDE_BUS * MAX_IDE_DEVS];
    BusState *idebus[MAX_IDE_BUS];
    ISADevice *rtc_state;
    ISADevice *floppy;
    MemoryRegion *ram_memory;
    MemoryRegion *pci_memory;
    MemoryRegion *rom_memory;
    DeviceState *icc_bridge;
    FWCfgState *fw_cfg = NULL;
    PcGuestInfo *guest_info;

    icc_bridge = qdev_create(NULL, TYPE_ICC_BRIDGE);
    object_property_add_child(qdev_get_machine(), "icc-bridge",
                              OBJECT(icc_bridge), NULL);

    pc_cpus_init(args->cpu_model, icc_bridge);

    if (kvmclock_enabled) {
        kvmclock_create();
    }

    /* Check whether RAM fits below 4G (leaving 1/2 GByte for IO memory).
     * If it doesn't, we need to split it in chunks below and above 4G.
     * In any case, try to make sure that guest addresses aligned at
     * 1G boundaries get mapped to host addresses aligned at 1G boundaries.
     * For old machine types, use whatever split we used historically to avoid
     * breaking migration.
     */
    if (args->ram_size >= 0xe0000000) {
        ram_addr_t lowmem = gigabyte_align ? 0xc0000000 : 0xe0000000;
        above_4g_mem_size = args->ram_size - lowmem;
        below_4g_mem_size = lowmem;
    } else {
        above_4g_mem_size = 0;
        below_4g_mem_size = args->ram_size;
    }

    if (pci_enabled) {
        pci_memory = g_new(MemoryRegion, 1);
        memory_region_init(pci_memory, "pci", INT64_MAX);
        rom_memory = pci_memory;
    } else {
        pci_memory = NULL;
        rom_memory = system_memory;
    }

    if (smbios_type1_defaults) {
        /* These values are guest ABI, do not change */
        smbios_set_type1_defaults("Red Hat", "KVM", args->machine->desc);
    }

    guest_info = pc_guest_info_init(below_4g_mem_size, above_4g_mem_size);

    guest_info->has_acpi_build = has_acpi_build;

    guest_info->has_pci_info = has_pci_info;
    guest_info->isapc_ram_fw = !pci_enabled;

    /* allocate ram and load rom/bios */
    if (!xen_enabled()) {
        fw_cfg = pc_memory_init(system_memory,
                       args->kernel_filename, args->kernel_cmdline,
                       args->initrd_filename,
                       below_4g_mem_size, above_4g_mem_size,
                       rom_memory, &ram_memory, guest_info);
    }

    gsi_state = g_malloc0(sizeof(*gsi_state));
    if (kvm_irqchip_in_kernel()) {
        kvm_pc_setup_irq_routing(pci_enabled);
        gsi = qemu_allocate_irqs(kvm_pc_gsi_handler, gsi_state,
                                 GSI_NUM_PINS);
    } else {
        gsi = qemu_allocate_irqs(gsi_handler, gsi_state, GSI_NUM_PINS);
    }

    if (pci_enabled) {
        pci_bus = i440fx_init(&i440fx_state, &piix3_devfn, &isa_bus, gsi,
                              system_memory, system_io, args->ram_size,
                              below_4g_mem_size,
                              0x100000000ULL - below_4g_mem_size,
                              above_4g_mem_size,
                              pci_memory, ram_memory);
    } else {
        pci_bus = NULL;
        i440fx_state = NULL;
        isa_bus = isa_bus_new(NULL, system_io);
        no_hpet = 1;
    }
    isa_bus_irqs(isa_bus, gsi);

    if (kvm_irqchip_in_kernel()) {
        i8259 = kvm_i8259_init(isa_bus);
    } else if (xen_enabled()) {
        i8259 = xen_interrupt_controller_init();
    } else {
        cpu_irq = pc_allocate_cpu_irq();
        i8259 = i8259_init(isa_bus, cpu_irq[0]);
    }

    for (i = 0; i < ISA_NUM_IRQS; i++) {
        gsi_state->i8259_irq[i] = i8259[i];
    }
    if (pci_enabled) {
        ioapic_init_gsi(gsi_state, "i440fx");
    }
    qdev_init_nofail(icc_bridge);

    pc_register_ferr_irq(gsi[13]);

    pc_vga_init(isa_bus, pci_enabled ? pci_bus : NULL);
    if (xen_enabled()) {
        pci_create_simple(pci_bus, -1, "xen-platform");
    }

    /* init basic PC hardware */
    pc_basic_device_init(isa_bus, gsi, &rtc_state, &floppy, xen_enabled());

    pc_nic_init(isa_bus, pci_bus);

    ide_drive_get(hd, MAX_IDE_BUS);
    if (pci_enabled) {
        PCIDevice *dev;
        if (xen_enabled()) {
            dev = pci_piix3_xen_ide_init(pci_bus, hd, piix3_devfn + 1);
        } else {
            dev = pci_piix3_ide_init(pci_bus, hd, piix3_devfn + 1);
        }
        idebus[0] = qdev_get_child_bus(&dev->qdev, "ide.0");
        idebus[1] = qdev_get_child_bus(&dev->qdev, "ide.1");
    } else {
        for(i = 0; i < MAX_IDE_BUS; i++) {
            ISADevice *dev;
            dev = isa_ide_init(isa_bus, ide_iobase[i], ide_iobase2[i],
                               ide_irq[i],
                               hd[MAX_IDE_DEVS * i], hd[MAX_IDE_DEVS * i + 1]);
            idebus[i] = qdev_get_child_bus(&dev->qdev, "ide.0");
        }
    }

    pc_cmos_init(below_4g_mem_size, above_4g_mem_size, args->boot_device,
                 floppy, idebus[0], idebus[1], rtc_state);

    if (pci_enabled && usb_enabled(false)) {
        pci_create_simple(pci_bus, piix3_devfn + 2, "piix3-usb-uhci");
    }

    if (pci_enabled && acpi_enabled) {
        i2c_bus *smbus;

        smi_irq = qemu_allocate_irqs(pc_acpi_smi_interrupt,
                                     x86_env_get_cpu(first_cpu), 1);
        /* TODO: Populate SPD eeprom data.  */
        smbus = piix4_pm_init(pci_bus, piix3_devfn + 3, 0xb100,
                              gsi[9], *smi_irq,
                              kvm_enabled(), fw_cfg);
        smbus_eeprom_init(smbus, 8, NULL, 0);
    }

    if (pci_enabled) {
        pc_pci_device_init(pci_bus);
    }
}

static void pc_init_pci(QEMUMachineInitArgs *args)
{
    pc_init1(args, get_system_memory(), get_system_io(), 1, 1);
}

#if 0 /* Disabled for Red Hat Enterprise Linux */

static void pc_init_pci_1_5(QEMUMachineInitArgs *args)
{
    has_pci_info = false;
    pc_init_pci(args);
}

static void pc_init_pci_1_4(QEMUMachineInitArgs *args)
{
    has_pci_info = false;
    x86_cpu_compat_set_features("n270", FEAT_1_ECX, 0, CPUID_EXT_MOVBE);
    x86_cpu_compat_set_features("Westmere", FEAT_1_ECX, 0, CPUID_EXT_PCLMULQDQ);
    pc_init_pci(args);
}

static void pc_init_pci_1_3(QEMUMachineInitArgs *args)
{
    has_pci_info = false;
    enable_compat_apic_id_mode();
    pc_init_pci(args);
}

/* PC machine init function for pc-1.1 to pc-1.2 */
static void pc_init_pci_1_2(QEMUMachineInitArgs *args)
{
    has_pci_info = false;
    disable_kvm_pv_eoi();
    enable_compat_apic_id_mode();
    pc_init_pci(args);
}

/* PC machine init function for pc-0.14 to pc-1.0 */
static void pc_init_pci_1_0(QEMUMachineInitArgs *args)
{
    has_pci_info = false;
    disable_kvm_pv_eoi();
    enable_compat_apic_id_mode();
    pc_init_pci(args);
}

/* PC init function for pc-0.10 to pc-0.13, and reused by xenfv */
static void pc_init_pci_no_kvmclock(QEMUMachineInitArgs *args)
{
    has_pci_info = false;
    disable_kvm_pv_eoi();
    enable_compat_apic_id_mode();
    pc_init1(args, get_system_memory(), get_system_io(), 1, 0);
}

static void pc_init_isa(QEMUMachineInitArgs *args)
{
    if (!args->cpu_model) {
        args->cpu_model = "486";
    }
    has_pci_info = false;
    disable_kvm_pv_eoi();
    enable_compat_apic_id_mode();
    pc_init1(args, get_system_memory(), get_system_io(), 0, 1);
}

#ifdef CONFIG_XEN
static void pc_xen_hvm_init(QEMUMachineInitArgs *args)
{
    if (xen_hvm_init() != 0) {
        hw_error("xen hardware virtual machine initialisation failed");
    }
    pc_init_pci_no_kvmclock(args);
    xen_vcpu_init();
}
#endif

static QEMUMachine pc_i440fx_machine_v1_5 = {
    .name = "pc-i440fx-1.5",
    .alias = "pc",
    .desc = "Standard PC (i440FX + PIIX, 1996)",
    .init = pc_init_pci_1_5,
    .hot_add_cpu = pc_hot_add_cpu,
    .max_cpus = 255,
    .is_default = 1,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_1_5,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

static QEMUMachine pc_i440fx_machine_v1_4 = {
    .name = "pc-i440fx-1.4",
    .desc = "Standard PC (i440FX + PIIX, 1996)",
    .init = pc_init_pci_1_4,
    .max_cpus = 255,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_1_4,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_COMPAT_1_3 \
	PC_COMPAT_1_4, \
        {\
            .driver   = "usb-tablet",\
            .property = "usb_version",\
            .value    = stringify(1),\
        },{\
            .driver   = "virtio-net-pci",\
            .property = "ctrl_mac_addr",\
            .value    = "off",      \
        },{ \
            .driver   = "virtio-net-pci", \
            .property = "mq", \
            .value    = "off", \
        }, {\
            .driver   = "e1000",\
            .property = "autonegotiation",\
            .value    = "off",\
        }

static QEMUMachine pc_machine_v1_3 = {
    .name = "pc-1.3",
    .desc = "Standard PC",
    .init = pc_init_pci_1_3,
    .max_cpus = 255,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_1_3,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_COMPAT_1_2 \
        PC_COMPAT_1_3,\
        {\
            .driver   = "nec-usb-xhci",\
            .property = "msi",\
            .value    = "off",\
        },{\
            .driver   = "nec-usb-xhci",\
            .property = "msix",\
            .value    = "off",\
        },{\
            .driver   = "ivshmem",\
            .property = "use64",\
            .value    = "0",\
        },{\
            .driver   = "qxl",\
            .property = "revision",\
            .value    = stringify(3),\
        },{\
            .driver   = "qxl-vga",\
            .property = "revision",\
            .value    = stringify(3),\
        },{\
            .driver   = "VGA",\
            .property = "mmio",\
            .value    = "off",\
        }

static QEMUMachine pc_machine_v1_2 = {
    .name = "pc-1.2",
    .desc = "Standard PC",
    .init = pc_init_pci_1_2,
    .max_cpus = 255,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_1_2,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_COMPAT_1_1 \
        PC_COMPAT_1_2,\
        {\
            .driver   = "virtio-scsi-pci",\
            .property = "hotplug",\
            .value    = "off",\
        },{\
            .driver   = "virtio-scsi-pci",\
            .property = "param_change",\
            .value    = "off",\
        },{\
            .driver   = "VGA",\
            .property = "vgamem_mb",\
            .value    = stringify(8),\
        },{\
            .driver   = "vmware-svga",\
            .property = "vgamem_mb",\
            .value    = stringify(8),\
        },{\
            .driver   = "qxl-vga",\
            .property = "vgamem_mb",\
            .value    = stringify(8),\
        },{\
            .driver   = "qxl",\
            .property = "vgamem_mb",\
            .value    = stringify(8),\
        },{\
            .driver   = "virtio-blk-pci",\
            .property = "config-wce",\
            .value    = "off",\
        }

static QEMUMachine pc_machine_v1_1 = {
    .name = "pc-1.1",
    .desc = "Standard PC",
    .init = pc_init_pci_1_2,
    .max_cpus = 255,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_1_1,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_COMPAT_1_0 \
        PC_COMPAT_1_1,\
        {\
            .driver   = TYPE_ISA_FDC,\
            .property = "check_media_rate",\
            .value    = "off",\
        }, {\
            .driver   = "virtio-balloon-pci",\
            .property = "class",\
            .value    = stringify(PCI_CLASS_MEMORY_RAM),\
        },{\
            .driver   = "apic",\
            .property = "vapic",\
            .value    = "off",\
        },{\
            .driver   = TYPE_USB_DEVICE,\
            .property = "full-path",\
            .value    = "no",\
        }

static QEMUMachine pc_machine_v1_0 = {
    .name = "pc-1.0",
    .desc = "Standard PC",
    .init = pc_init_pci_1_0,
    .max_cpus = 255,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_1_0,
        { /* end of list */ }
    },
    .hw_version = "1.0",
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_COMPAT_0_15 \
        PC_COMPAT_1_0

static QEMUMachine pc_machine_v0_15 = {
    .name = "pc-0.15",
    .desc = "Standard PC",
    .init = pc_init_pci_1_0,
    .max_cpus = 255,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_0_15,
        { /* end of list */ }
    },
    .hw_version = "0.15",
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_COMPAT_0_14 \
        PC_COMPAT_0_15,\
        {\
            .driver   = "virtio-blk-pci",\
            .property = "event_idx",\
            .value    = "off",\
        },{\
            .driver   = "virtio-serial-pci",\
            .property = "event_idx",\
            .value    = "off",\
        },{\
            .driver   = "virtio-net-pci",\
            .property = "event_idx",\
            .value    = "off",\
        },{\
            .driver   = "virtio-balloon-pci",\
            .property = "event_idx",\
            .value    = "off",\
        }

static QEMUMachine pc_machine_v0_14 = {
    .name = "pc-0.14",
    .desc = "Standard PC",
    .init = pc_init_pci_1_0,
    .max_cpus = 255,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_0_14, 
        {
            .driver   = "qxl",
            .property = "revision",
            .value    = stringify(2),
        },{
            .driver   = "qxl-vga",
            .property = "revision",
            .value    = stringify(2),
        },
        { /* end of list */ }
    },
    .hw_version = "0.14",
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_COMPAT_0_13 \
        PC_COMPAT_0_14,\
        {\
            .driver   = TYPE_PCI_DEVICE,\
            .property = "command_serr_enable",\
            .value    = "off",\
        },{\
            .driver   = "AC97",\
            .property = "use_broken_id",\
            .value    = stringify(1),\
        }

static QEMUMachine pc_machine_v0_13 = {
    .name = "pc-0.13",
    .desc = "Standard PC",
    .init = pc_init_pci_no_kvmclock,
    .max_cpus = 255,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_0_13,
        {
            .driver   = "virtio-9p-pci",
            .property = "vectors",
            .value    = stringify(0),
        },{
            .driver   = "VGA",
            .property = "rombar",
            .value    = stringify(0),
        },{
            .driver   = "vmware-svga",
            .property = "rombar",
            .value    = stringify(0),
        },
        { /* end of list */ }
    },
    .hw_version = "0.13",
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_COMPAT_0_12 \
        PC_COMPAT_0_13,\
        {\
            .driver   = "virtio-serial-pci",\
            .property = "max_ports",\
            .value    = stringify(1),\
        },{\
            .driver   = "virtio-serial-pci",\
            .property = "vectors",\
            .value    = stringify(0),\
        }

static QEMUMachine pc_machine_v0_12 = {
    .name = "pc-0.12",
    .desc = "Standard PC",
    .init = pc_init_pci_no_kvmclock,
    .max_cpus = 255,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_0_12,
        {
            .driver   = "VGA",
            .property = "rombar",
            .value    = stringify(0),
        },{
            .driver   = "vmware-svga",
            .property = "rombar",
            .value    = stringify(0),
        },
        { /* end of list */ }
    },
    .hw_version = "0.12",
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_COMPAT_0_11 \
        PC_COMPAT_0_12,\
        {\
            .driver   = "virtio-blk-pci",\
            .property = "vectors",\
            .value    = stringify(0),\
        },{\
            .driver   = TYPE_PCI_DEVICE,\
            .property = "rombar",\
            .value    = stringify(0),\
        }

static QEMUMachine pc_machine_v0_11 = {
    .name = "pc-0.11",
    .desc = "Standard PC, qemu 0.11",
    .init = pc_init_pci_no_kvmclock,
    .max_cpus = 255,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_0_11,
        {
            .driver   = "ide-drive",
            .property = "ver",
            .value    = "0.11",
        },{
            .driver   = "scsi-disk",
            .property = "ver",
            .value    = "0.11",
        },
        { /* end of list */ }
    },
    .hw_version = "0.11",
    DEFAULT_MACHINE_OPTIONS,
};

static QEMUMachine pc_machine_v0_10 = {
    .name = "pc-0.10",
    .desc = "Standard PC, qemu 0.10",
    .init = pc_init_pci_no_kvmclock,
    .max_cpus = 255,
    .compat_props = (GlobalProperty[]) {
        PC_COMPAT_0_11,
        {
            .driver   = "virtio-blk-pci",
            .property = "class",
            .value    = stringify(PCI_CLASS_STORAGE_OTHER),
        },{
            .driver   = "virtio-serial-pci",
            .property = "class",
            .value    = stringify(PCI_CLASS_DISPLAY_OTHER),
        },{
            .driver   = "virtio-net-pci",
            .property = "vectors",
            .value    = stringify(0),
        },{
            .driver   = "ide-drive",
            .property = "ver",
            .value    = "0.10",
        },{
            .driver   = "scsi-disk",
            .property = "ver",
            .value    = "0.10",
        },
        { /* end of list */ }
    },
    .hw_version = "0.10",
    DEFAULT_MACHINE_OPTIONS,
};

static QEMUMachine isapc_machine = {
    .name = "isapc",
    .desc = "ISA-only PC",
    .init = pc_init_isa,
    .max_cpus = 1,
    .compat_props = (GlobalProperty[]) {
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

#ifdef CONFIG_XEN
static QEMUMachine xenfv_machine = {
    .name = "xenfv",
    .desc = "Xen Fully-virtualized PC",
    .init = pc_xen_hvm_init,
    .max_cpus = HVM_MAX_VCPUS,
    .default_machine_opts = "accel=xen",
    DEFAULT_MACHINE_OPTIONS,
};
#endif

static void pc_machine_init(void)
{
    qemu_register_machine(&pc_i440fx_machine_v1_5);
    qemu_register_machine(&pc_i440fx_machine_v1_4);
    qemu_register_machine(&pc_machine_v1_3);
    qemu_register_machine(&pc_machine_v1_2);
    qemu_register_machine(&pc_machine_v1_1);
    qemu_register_machine(&pc_machine_v1_0);
    qemu_register_machine(&pc_machine_v0_15);
    qemu_register_machine(&pc_machine_v0_14);
    qemu_register_machine(&pc_machine_v0_13);
    qemu_register_machine(&pc_machine_v0_12);
    qemu_register_machine(&pc_machine_v0_11);
    qemu_register_machine(&pc_machine_v0_10);
    qemu_register_machine(&isapc_machine);
#ifdef CONFIG_XEN
    qemu_register_machine(&xenfv_machine);
#endif
}

machine_init(pc_machine_init);

#endif  /* Disabled for Red Hat Enterprise Linux */

/* Red Hat Enterprise Linux machine types */

static void pc_compat_rhel700(QEMUMachineInitArgs *args)
{
    x86_cpu_compat_set_features("Conroe", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Penryn", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Nehalem", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Westmere", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    /* SandyBridge and Haswell already have x2apic enabled */
    x86_cpu_compat_set_features("Opteron_G1", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Opteron_G2", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Opteron_G3", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Opteron_G4", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Opteron_G5", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);

    /* KVM can't expose RDTSCP on AMD CPUs, so there's no point in enabling it
     * on AMD CPU models.
     */
    x86_cpu_compat_set_features("phenom", FEAT_8000_0001_EDX, 0,
                                CPUID_EXT2_RDTSCP);
    x86_cpu_compat_set_features("Opteron_G2", FEAT_8000_0001_EDX, 0,
                                CPUID_EXT2_RDTSCP);
    x86_cpu_compat_set_features("Opteron_G3", FEAT_8000_0001_EDX, 0,
                                CPUID_EXT2_RDTSCP);
    x86_cpu_compat_set_features("Opteron_G4", FEAT_8000_0001_EDX, 0,
                                CPUID_EXT2_RDTSCP);
    x86_cpu_compat_set_features("Opteron_G5", FEAT_8000_0001_EDX, 0,
                                CPUID_EXT2_RDTSCP);
}

static void pc_init_rhel700(QEMUMachineInitArgs *args)
{
    pc_compat_rhel700(args);
    pc_init_pci(args);
}

static QEMUMachine pc_machine_rhel700 = {
    .name = "pc-i440fx-rhel7.0.0",
    .alias = "pc",
    .desc = "RHEL 7.0.0 PC (i440FX + PIIX, 1996)",
    .init = pc_init_rhel700,
    .hot_add_cpu = pc_hot_add_cpu,
    .max_cpus = RHEL_MAX_CPUS,
    .is_default = 1,
    .default_machine_opts = "firmware=bios-256k.bin",
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_RHEL6_6_COMPAT \
    {\
        .driver   = "scsi-hd",\
        .property = "discard_granularity",\
        .value    = stringify(0),\
    },{\
        .driver   = "scsi-cd",\
        .property = "discard_granularity",\
        .value    = stringify(0),\
    },{\
        .driver   = "scsi-disk",\
        .property = "discard_granularity",\
        .value    = stringify(0),\
    },{\
        .driver   = "ide-hd",\
        .property = "discard_granularity",\
        .value    = stringify(0),\
    },{\
        .driver   = "ide-cd",\
        .property = "discard_granularity",\
        .value    = stringify(0),\
    },{\
        .driver   = "ide-drive",\
        .property = "discard_granularity",\
        .value    = stringify(0),\
    },{\
        .driver   = "virtio-blk-pci",\
        .property = "discard_granularity",\
        .value    = stringify(0),\
    },{\
        .driver   = "virtio-serial-pci",\
        .property = "vectors",\
        /* DEV_NVECTORS_UNSPECIFIED as a uint32_t string */\
        .value    = stringify(0xFFFFFFFF),\
    },{\
        .driver   = "486-" TYPE_X86_CPU,\
        .property = "model",\
        .value    = stringify(0),\
    },{\
        .driver   = "usb-tablet",\
        .property = "usb_version",\
        .value    = stringify(1),\
    },{\
        .driver   = "virtio-net-pci",\
        .property = "mq",\
        .value    = "off",\
    },{\
        .driver   = "VGA",\
        .property = "mmio",\
        .value    = "off",\
    },{\
        .driver   = "virtio-blk-pci",\
        .property = "config-wce",\
        .value    = "off",\
    },{\
        .driver   = TYPE_ISA_FDC,\
        .property = "check_media_rate",\
        .value    = "off",\
    },{\
        .driver   = "virtio-balloon-pci",\
        .property = "class",\
        .value    = stringify(PCI_CLASS_MEMORY_RAM),\
    },{\
        .driver   = TYPE_PCI_DEVICE,\
        .property = "command_serr_enable",\
        .value    = "off",\
    },{\
        .driver   = "AC97",\
        .property = "use_broken_id",\
        .value    = stringify(1),\
    },{\
        .driver   = "intel-hda",\
        .property = "msi",\
        .value    = stringify(0),\
    },{\
        .driver = "qemu32-" TYPE_X86_CPU,\
        .property = "xlevel",\
        .value = stringify(0),\
    },{\
        .driver = "486-" TYPE_X86_CPU,\
        .property = "level",\
        .value = stringify(0),\
    },{\
        .driver   = "qemu32-" TYPE_X86_CPU,\
        .property = "model",\
        .value    = stringify(3),\
    },{\
        .driver   = "usb-ccid",\
        .property = "serial",\
        .value    = "1",\
    },{\
        .driver   = "ne2k_pci",\
        .property = "romfile",\
        .value    = "rhel6-ne2k_pci.rom",\
    },{\
        .driver   = "pcnet",\
        .property = "romfile",\
        .value    = "rhel6-pcnet.rom",\
    },{\
        .driver   = "rtl8139",\
        .property = "romfile",\
        .value    = "rhel6-rtl8139.rom",\
    },{\
        .driver   = "e1000",\
        .property = "romfile",\
        .value    = "rhel6-e1000.rom",\
    },{\
        .driver   = "virtio-net-pci",\
        .property = "romfile",\
        .value    = "rhel6-virtio.rom",\
    },{\
        .driver   = "virtio-net-pci",\
        .property = "any_layout",\
        .value    = "off",\
    }

static void pc_compat_rhel660(QEMUMachineInitArgs *args)
{
    pc_compat_rhel700(args);
    if (!args->cpu_model) {
        args->cpu_model = "cpu64-rhel6";
    }
    x86_cpu_compat_set_features("pentium", FEAT_1_EDX, 0, CPUID_APIC);
    x86_cpu_compat_set_features("pentium2", FEAT_1_EDX, 0, CPUID_APIC);
    x86_cpu_compat_set_features("pentium3", FEAT_1_EDX, 0, CPUID_APIC);

    x86_cpu_compat_set_features("Conroe", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Penryn", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Nehalem", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Westmere", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Westmere", FEAT_1_ECX, 0, CPUID_EXT_PCLMULQDQ);
    x86_cpu_compat_set_features("Westmere", FEAT_8000_0001_EDX,
             CPUID_EXT2_FXSR | CPUID_EXT2_MMX | CPUID_EXT2_PAT |
             CPUID_EXT2_CMOV | CPUID_EXT2_PGE | CPUID_EXT2_APIC |
             CPUID_EXT2_CX8 | CPUID_EXT2_MCE | CPUID_EXT2_PAE | CPUID_EXT2_MSR |
             CPUID_EXT2_TSC | CPUID_EXT2_PSE | CPUID_EXT2_DE | CPUID_EXT2_FPU,
             0);
    x86_cpu_compat_set_features("Broadwell", FEAT_8000_0001_EDX,
                                0, CPUID_EXT2_RDTSCP);
    x86_cpu_compat_set_features("Broadwell", FEAT_7_0_EBX,
                                0, CPUID_7_0_EBX_SMAP);

    /* RHEL-6 kernel never supported exposing RDTSCP */
    x86_cpu_compat_set_features(NULL, FEAT_8000_0001_EDX, 0, CPUID_EXT2_RDTSCP);

    x86_cpu_compat_set_features("Opteron_G1", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Opteron_G2", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Opteron_G3", FEAT_1_ECX, CPUID_EXT_X2APIC, 0);
    x86_cpu_compat_set_features("Opteron_G4", FEAT_1_ECX, 0, CPUID_EXT_X2APIC);
    x86_cpu_compat_set_features("Opteron_G5", FEAT_1_ECX, 0, CPUID_EXT_X2APIC);

    /* RHEL-6 had 3dnow & 3dnowext unconditionally disabled on all models */
    x86_cpu_compat_set_features(NULL, FEAT_8000_0001_EDX, 0,
                                CPUID_EXT2_3DNOW | CPUID_EXT2_3DNOWEXT);

    disable_kvm_pv_unhalt();

    rom_file_has_mr = false; 
    has_acpi_build = false;
    gigabyte_align = false;
    shadow_bios_after_incoming = true;
    ich9_uhci123_irqpin_override = true;
}

static void pc_init_rhel660(QEMUMachineInitArgs *args)
{
    pc_compat_rhel660(args);
    pc_init_pci(args);
}

static QEMUMachine pc_machine_rhel660 = {
    .name = "rhel6.6.0",
    .desc = "RHEL 6.6.0 PC",
    .init = pc_init_rhel660,
    .hot_add_cpu = pc_hot_add_cpu,
    .max_cpus = RHEL_MAX_CPUS,
    .compat_props = (GlobalProperty[]) {
        PC_RHEL6_6_COMPAT,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_RHEL6_5_COMPAT \
    PC_RHEL6_6_COMPAT,\
    {\
        .driver   = TYPE_USB_DEVICE,\
        .property = "msos-desc",\
        .value    = "no",\
    }

static void pc_compat_rhel650(QEMUMachineInitArgs *args)
{
    pc_compat_rhel660(args);
}

static void pc_init_rhel650(QEMUMachineInitArgs *args)
{
    pc_compat_rhel650(args);
    pc_init_pci(args);
}

static QEMUMachine pc_machine_rhel650 = {
    .name = "rhel6.5.0",
    .desc = "RHEL 6.5.0 PC",
    .init = pc_init_rhel650,
    .hot_add_cpu = pc_hot_add_cpu,
    .max_cpus = RHEL_MAX_CPUS,
    .compat_props = (GlobalProperty[]) {
        PC_RHEL6_5_COMPAT,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_RHEL6_4_COMPAT \
    PC_RHEL6_5_COMPAT,\
    {\
        .driver   = "virtio-scsi-pci",\
        .property = "vectors",\
        .value    = stringify(2),\
    },{\
        .driver   = "hda-micro",\
        .property = "mixer",\
        .value    = "off",\
    },{\
        .driver   = "hda-duplex",\
        .property = "mixer",\
        .value    = "off",\
    },{\
        .driver   = "hda-output",\
        .property = "mixer",\
        .value    = "off",\
    },{\
        .driver   = "virtio-net-pci",\
        .property = "ctrl_mac_addr",\
        .value    = "off",\
    }

static void pc_compat_rhel640(QEMUMachineInitArgs *args)
{
    pc_compat_rhel650(args);
    x86_cpu_compat_set_features(NULL, FEAT_1_EDX, 0, CPUID_SEP);
}

static void pc_init_rhel640(QEMUMachineInitArgs *args)
{
    pc_compat_rhel640(args);
    pc_init_pci(args);
}

static QEMUMachine pc_machine_rhel640 = {
    .name = "rhel6.4.0",
    .desc = "RHEL 6.4.0 PC",
    .init = pc_init_rhel640,
    .hot_add_cpu = pc_hot_add_cpu,
    .max_cpus = RHEL_MAX_CPUS,
    .compat_props = (GlobalProperty[]) {
        PC_RHEL6_4_COMPAT,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_RHEL6_3_COMPAT \
    PC_RHEL6_4_COMPAT,\
    {\
        .driver   = "Conroe-" TYPE_X86_CPU,\
        .property = "level",\
        .value    = stringify(2),\
    },{\
        .driver   = "Penryn-" TYPE_X86_CPU,\
        .property = "level",\
        .value    = stringify(2),\
    },{\
        .driver   = "Nehalem-" TYPE_X86_CPU,\
        .property = "level",\
        .value    = stringify(2),\
    },{\
        .driver   = "e1000",\
        .property = "autonegotiation",\
        .value    = "off",\
    },{\
        .driver   = "qxl",\
        .property = "revision",\
        .value    = stringify(3),\
    },{\
        .driver   = "qxl-vga",\
        .property = "revision",\
        .value    = stringify(3),\
    },{\
        .driver   = "virtio-scsi-pci",\
        .property = "hotplug",\
        .value    = "off",\
    },{\
        .driver   = "virtio-scsi-pci",\
        .property = "param_change",\
        .value    = "off",\
    },{\
        .driver = TYPE_X86_CPU,\
        .property = "pmu",\
        .value = "on",\
    },{\
        .driver   = "usb-hub",\
        .property = "serial",\
        .value    = "314159",\
    },{\
        .driver   = "usb-storage",\
        .property = "serial",\
        .value    = "1",\
    }

static void pc_compat_rhel630(QEMUMachineInitArgs *args)
{
    pc_compat_rhel640(args);
    disable_kvm_pv_eoi();
    enable_compat_apic_id_mode();
    x86_cpu_compat_set_features("SandyBridge", FEAT_1_ECX,
                                0, CPUID_EXT_TSC_DEADLINE_TIMER);
}

static void pc_init_rhel630(QEMUMachineInitArgs *args)
{
    pc_compat_rhel630(args);
    pc_init_pci(args);
}

static QEMUMachine pc_machine_rhel630 = {
    .name = "rhel6.3.0",
    .desc = "RHEL 6.3.0 PC",
    .init = pc_init_rhel630,
    .hot_add_cpu = pc_hot_add_cpu,
    .max_cpus = RHEL_MAX_CPUS,
    .compat_props = (GlobalProperty[]) {
        PC_RHEL6_3_COMPAT,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_RHEL6_2_COMPAT \
    PC_RHEL6_3_COMPAT,\
    {\
        .driver = TYPE_X86_CPU,\
        .property = "pmu",\
        .value = "off",\
    }

static void pc_compat_rhel620(QEMUMachineInitArgs *args)
{
    pc_compat_rhel630(args);
}

static void pc_init_rhel620(QEMUMachineInitArgs *args)
{
    pc_compat_rhel620(args);
    pc_init_pci(args);
}

static QEMUMachine pc_machine_rhel620 = {
    .name = "rhel6.2.0",
    .desc = "RHEL 6.2.0 PC",
    .init = pc_init_rhel620,
    .hot_add_cpu = pc_hot_add_cpu,
    .max_cpus = RHEL_MAX_CPUS,
    .compat_props = (GlobalProperty[]) {
        PC_RHEL6_2_COMPAT,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

/* 
 * NOTE: We don't have the event_idx compat entry for the
 * virtio-balloon-pci driver because RHEL6 doesn't disable
 * it either due to a bug (see RHBZ 1029539 fo more info)
 */
#define PC_RHEL6_1_COMPAT \
    PC_RHEL6_2_COMPAT,\
    {\
        .driver   = "PIIX4_PM",\
        .property = "disable_s3",\
        .value    = "0",\
    },{\
        .driver   = "PIIX4_PM",\
        .property = "disable_s4",\
        .value    = "0",\
    },{\
        .driver   = "qxl",\
        .property = "revision",\
        .value    = stringify(2),\
    },{\
        .driver   = "qxl-vga",\
        .property = "revision",\
        .value    = stringify(2),\
    },{\
        .driver   = "virtio-blk-pci",\
        .property = "event_idx",\
        .value    = "off",\
    },{\
        .driver   = "virtio-serial-pci",\
        .property = "event_idx",\
        .value    = "off",\
    },{\
        .driver   = "virtio-net-pci",\
        .property = "event_idx",\
        .value    = "off",\
    },{\
        .driver   = "usb-kbd",\
        .property = "serial",\
        .value    = "1",\
    },{\
        .driver   = "usb-mouse",\
        .property = "serial",\
        .value    = "1",\
    },{\
        .driver   = "usb-tablet",\
        .property = "serial",\
        .value    = "1",\
    }

static void pc_compat_rhel610(QEMUMachineInitArgs *args)
{
    pc_compat_rhel620(args);
}

static void pc_init_rhel610(QEMUMachineInitArgs *args)
{
    pc_compat_rhel610(args);
    pc_init_pci(args);
}

static QEMUMachine pc_machine_rhel610 = {
    .name = "rhel6.1.0",
    .desc = "RHEL 6.1.0 PC",
    .init = pc_init_rhel610,
    .hot_add_cpu = pc_hot_add_cpu,
    .max_cpus = RHEL_MAX_CPUS,
    .compat_props = (GlobalProperty[]) {
        PC_RHEL6_1_COMPAT,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

#define PC_RHEL6_0_COMPAT \
    PC_RHEL6_1_COMPAT,\
    {\
        .driver   = "qxl",\
        .property = "revision",\
        .value    = stringify(1),\
    },{\
        .driver   = "qxl-vga",\
        .property = "revision",\
        .value    = stringify(1),\
    },{\
        .driver   = "VGA",\
        .property = "rombar",\
        .value    = stringify(0),\
    }

static void pc_compat_rhel600(QEMUMachineInitArgs *args)
{
    pc_compat_rhel610(args);
}

static void pc_init_rhel600(QEMUMachineInitArgs *args)
{
    pc_compat_rhel600(args);
    pc_init_pci(args);
}

static QEMUMachine pc_machine_rhel600 = {
    .name = "rhel6.0.0",
    .desc = "RHEL 6.0.0 PC",
    .init = pc_init_rhel600,
    .hot_add_cpu = pc_hot_add_cpu,
    .max_cpus = RHEL_MAX_CPUS,
    .compat_props = (GlobalProperty[]) {
        PC_RHEL6_0_COMPAT,
        { /* end of list */ }
    },
    DEFAULT_MACHINE_OPTIONS,
};

static void rhel_machine_init(void)
{
    qemu_register_machine(&pc_machine_rhel700);
    qemu_register_machine(&pc_machine_rhel660);
    qemu_register_machine(&pc_machine_rhel650);
    qemu_register_machine(&pc_machine_rhel640);
    qemu_register_machine(&pc_machine_rhel630);
    qemu_register_machine(&pc_machine_rhel620);
    qemu_register_machine(&pc_machine_rhel610);
    qemu_register_machine(&pc_machine_rhel600);
}

machine_init(rhel_machine_init);
