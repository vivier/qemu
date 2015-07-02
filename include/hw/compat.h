#ifndef HW_COMPAT_H
#define HW_COMPAT_H

#define HW_COMPAT_2_1 \
        {\
            .driver   = "intel-hda",\
            .property = "old_msi_addr",\
            .value    = "on",\
        },{\
            .driver   = "VGA",\
            .property = "qemu-extended-regs",\
            .value    = "off",\
        },{\
            .driver   = "secondary-vga",\
            .property = "qemu-extended-regs",\
            .value    = "off",\
        },{\
            .driver   = "virtio-scsi-pci",\
            .property = "any_layout",\
            .value    = "off",\
        },{\
            .driver   = "usb-mouse",\
            .property = "usb_version",\
            .value    = stringify(1),\
        },{\
            .driver   = "usb-kbd",\
            .property = "usb_version",\
            .value    = stringify(1),\
        },{\
            .driver   = "virtio-pci",\
            .property = "virtio-pci-bus-master-bug-migration",\
            .value    = "on",\
        }

/* Mostly like HW_COMPAT_2_1 but:
 *    we don't need virtio-scsi-pci since 7.0 already had that on
 */
#define HW_COMPAT_RHEL7_1 \
        {\
            .driver   = "intel-hda-generic",\
            .property = "old_msi_addr",\
            .value    = "on",\
        },{\
            .driver   = "VGA",\
            .property = "qemu-extended-regs",\
            .value    = "off",\
        },{\
            .driver   = "secondary-vga",\
            .property = "qemu-extended-regs",\
            .value    = "off",\
        },{\
            .driver   = "usb-mouse",\
            .property = "usb_version",\
            .value    = stringify(1),\
        },{\
            .driver   = "usb-kbd",\
            .property = "usb_version",\
            .value    = stringify(1),\
        },{\
            .driver   = "virtio-pci",\
            .property = "virtio-pci-bus-master-bug-migration",\
            .value    = "on",\
        }

#endif /* HW_COMPAT_H */
