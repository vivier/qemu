Summary: Userspace component of KVM
Name: qemu-kvm
Version: 0.12.1.2
Release: 2.113%{?dist}
# Epoch because we pushed a qemu-1.0 package
Epoch: 2
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.linux-kvm.org
ExclusiveArch: x86_64

Source0: http://downloads.sourceforge.net/sourceforge/kvm/qemu-kvm-%{version}.tar.gz

# Loads kvm kernel modules at boot
Source2: kvm.modules

# Creates /dev/kvm
Source3: 80-kvm.rules

# KSM control scripts
Source4: ksm.init
Source5: ksm.sysconfig
Source6: ksmtuned.init
Source7: ksmtuned
Source8: ksmtuned.conf

# Blacklist vhost-net for RHEL6.0 GA
Source9: blacklist-kvm.conf

# Change datadir to /usr/share/qemu-kvm
Patch1000: qemu-change-share-suffix.patch
# Install manpage as qemu-kvm(1)
Patch1001: qemu-rename-manpage.patch
# Change SASL server name to qemu-kvm
Patch1002: qemu-rename-sasl-server-name.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1003: kvm-virtio-Remove-duplicate-macro-definition-for-max.-vi.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1004: kvm-virtio-console-qdev-conversion-new-virtio-serial-bus.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1005: kvm-virtio-serial-bus-Maintain-guest-and-host-port-open-.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1006: kvm-virtio-serial-bus-Add-a-port-name-property-for-port-.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1007: kvm-virtio-serial-bus-Add-support-for-buffering-guest-ou.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1008: kvm-virtio-serial-bus-Add-ability-to-hot-unplug-ports.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1009: kvm-virtio-serial-Add-a-virtserialport-device-for-generi.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1010: kvm-Move-virtio-serial-to-Makefile.hw.patch
# For bz#556459 - RFE - In-place backing file format change
Patch1011: kvm-block-Introduce-BDRV_O_NO_BACKING.patch
# For bz#556459 - RFE - In-place backing file format change
Patch1012: kvm-block-Add-bdrv_change_backing_file.patch
# For bz#556459 - RFE - In-place backing file format change
Patch1013: kvm-qemu-img-rebase.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1014: kvm-virtio-serial-bus-Remove-guest-buffer-caching-and-th.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1015: kvm-virtio-serial-Make-sure-we-don-t-crash-when-host-por.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1016: kvm-virtio-serial-Use-MSI-vectors-for-port-virtqueues.patch
# For bz#543825 - [RFE] Backport virtio-serial device to qemu
Patch1017: kvm-virtio-serial-bus-Match-upstream-whitespace.patch
# For bz#557435 - KVM: WIN7-32bit blue screen (IMAGE_NAME:  ntkrnlmp.exe).
Patch1018: kvm-reduce-number-of-reinjects-on-ACK.patch
# For bz#558412 - -help output not terminated by newline
Patch1019: kvm-Add-missing-newline-at-the-end-of-options-list.patch
# For bz#558414 - Artifacts in hextile decoding
Patch1020: kvm-vnc-Fix-artifacts-in-hextile-decoding.patch
# For bz#558415 - Assert triggers on qmp commands returning lists
Patch1021: kvm-QMP-Drop-wrong-assert.patch
# For bz#558435 - vmware-svga buffer overflow copying cursor data
Patch1022: kvm-vmware_vga-Check-cursor-dimensions-passed-from-guest.patch
# For bz#558438 - virtio status bits corrupted if guest deasserts bus mastering bit
Patch1023: kvm-virtio-pci-thinko-fix.patch
# For bz#558465 - Double-free of qmp async messages
Patch1024: kvm-QMP-Don-t-free-async-event-s-data.patch
# For bz#558466 - Possible segfault on vnc client disconnect
Patch1025: kvm-vnc_refresh-return-if-vd-timer-is-NULL.patch
# For bz#558477 - Incorrect handling of EINVAL from accept4()
Patch1026: kvm-osdep.c-Fix-accept4-fallback.patch
# For bz#558619 - QMP: Emit asynchronous events on all QMP monitors
Patch1027: kvm-QMP-Emit-asynchronous-events-on-all-QMP-monitors.patch
# For bz#558846 - fix use-after-free in vnc code
Patch1028: kvm-vnc_refresh-calling-vnc_update_client-might-free-vs.patch
# For bz#558416 - Machine check exception injected into qemu reinjected after every reset
Patch1029: kvm-MCE-Fix-bug-of-IA32_MCG_STATUS-after-system-reset.patch
# For bz#558432 - CPU topology not taking effect
Patch1030: kvm-Fix-CPU-topology-initialization.patch
# For bz#558467 - roms potentially loaded twice
Patch1031: kvm-loader-more-ignores-for-rom-intended-to-be-loaded-by.patch
# For bz#558470 - Incorrect machine types
Patch1032: kvm-pc-add-machine-type-for-0.12.patch
# For bz#559089 - Rename virtio-serial.c to virtio-console.c as is upstream.
Patch1033: kvm-virtio-console-Rename-virtio-serial.c-back-to-virtio.patch
# For bz#559503 - virtio-serial: fix multiple devices intialisation
Patch1034: kvm-virtio-serial-bus-Fix-bus-initialisation-and-allow-f.patch
# For bz#549759 - A QMP event notification on VNC client connect/disconnect events
Patch1035: kvm-VNC-Use-enabled-key-instead-of-status.patch
# For bz#549759 - A QMP event notification on VNC client connect/disconnect events
Patch1036: kvm-VNC-Make-auth-key-mandatory.patch
# For bz#549759 - A QMP event notification on VNC client connect/disconnect events
Patch1037: kvm-VNC-Rename-client-s-username-key.patch
# For bz#549759 - A QMP event notification on VNC client connect/disconnect events
Patch1038: kvm-VNC-Add-family-key.patch
# For bz#549759 - A QMP event notification on VNC client connect/disconnect events
Patch1039: kvm-VNC-Cache-client-info-at-connection-time.patch
# For bz#549759 - A QMP event notification on VNC client connect/disconnect events
Patch1040: kvm-QMP-Introduce-VNC_CONNECTED-event.patch
# For bz#549759 - A QMP event notification on VNC client connect/disconnect events
Patch1041: kvm-QMP-Introduce-VNC_DISCONNECTED-event.patch
# For bz#549759 - A QMP event notification on VNC client connect/disconnect events
Patch1042: kvm-QMP-Introduce-VNC_INITIALIZED-event.patch
# For bz#558730 - qemu may create too large iovecs for the kernel
Patch1043: kvm-block-avoid-creating-too-large-iovecs-in-multiwrite_.patch
# For bz#560623 - error codes aren't always propagated up through the block layer (e.g. -ENOSPC)
Patch1044: kvm-Fix-QEMU_WARN_UNUSED_RESULT.patch
# For bz#560623 - error codes aren't always propagated up through the block layer (e.g. -ENOSPC)
Patch1045: kvm-qcow2-Fix-error-handling-in-qcow2_grow_l1_table.patch
# For bz#560623 - error codes aren't always propagated up through the block layer (e.g. -ENOSPC)
Patch1046: kvm-qcow2-Fix-error-handling-in-qcow_save_vmstate.patch
# For bz#560623 - error codes aren't always propagated up through the block layer (e.g. -ENOSPC)
Patch1047: kvm-qcow2-Return-0-errno-in-get_cluster_table.patch
# For bz#560623 - error codes aren't always propagated up through the block layer (e.g. -ENOSPC)
Patch1048: kvm-qcow2-Return-0-errno-in-qcow2_alloc_cluster_offset.patch
# For bz#560623 - error codes aren't always propagated up through the block layer (e.g. -ENOSPC)
Patch1049: kvm-block-Return-original-error-codes-in-bdrv_pread-writ.patch
# For bz#560623 - error codes aren't always propagated up through the block layer (e.g. -ENOSPC)
Patch1050: kvm-qcow2-Fix-error-handling-in-grow_refcount_table.patch
# For bz#560623 - error codes aren't always propagated up through the block layer (e.g. -ENOSPC)
Patch1051: kvm-qcow2-Improve-error-handling-in-update_refcount.patch
# For bz#560623 - error codes aren't always propagated up through the block layer (e.g. -ENOSPC)
Patch1052: kvm-qcow2-Allow-updating-no-refcounts.patch
# For bz#560623 - error codes aren't always propagated up through the block layer (e.g. -ENOSPC)
Patch1053: kvm-qcow2-Don-t-ignore-update_refcount-return-value.patch
# For bz#560623 - error codes aren't always propagated up through the block layer (e.g. -ENOSPC)
Patch1054: kvm-qcow2-Don-t-ignore-qcow2_alloc_clusters-return-value.patch
# For bz#562181 - Small VNC related cleanup
Patch1055: kvm-net-Make-inet_strfamily-public.patch
# For bz#562181 - Small VNC related cleanup
Patch1056: kvm-net-inet_strfamily-Better-unknown-family-report.patch
# For bz#562181 - Small VNC related cleanup
Patch1057: kvm-vnc-Use-inet_strfamily.patch
# For bz#558818 - rom loading
Patch1058: kvm-roms-minor-fixes-and-cleanups.patch
# For bz#558818 - rom loading
Patch1059: kvm-fw_cfg-rom-loader-tweaks.patch
# For bz#558818 - rom loading
Patch1060: kvm-roms-rework-rom-loading-via-fw.patch
# For bz#558818 - rom loading
Patch1061: kvm-pci-allow-loading-roms-via-fw_cfg.patch
# For bz#558818 - rom loading
Patch1062: kvm-pc-add-rombar-to-compat-properties-for-pc-0.10-and-p.patch
# For bz#560942 - virtio-blk error handling doesn't work reliably
Patch1063: kvm-virtio_blk-Factor-virtio_blk_handle_request-out.patch
# For bz#560942 - virtio-blk error handling doesn't work reliably
Patch1064: kvm-virtio-blk-Fix-restart-after-read-error.patch
# For bz#560942 - virtio-blk error handling doesn't work reliably
Patch1065: kvm-virtio-blk-Fix-error-cases-which-ignored-rerror-werr.patch
# For bz#557930 - QMP: Feature Negotiation support
Patch1066: kvm-QMP-Add-QEMU-s-version-to-the-greeting-message.patch
# For bz#557930 - QMP: Feature Negotiation support
Patch1067: kvm-QMP-Introduce-the-qmp_capabilities-command.patch
# For bz#557930 - QMP: Feature Negotiation support
Patch1068: kvm-QMP-Enforce-capability-negotiation-rules.patch
# For bz#557930 - QMP: Feature Negotiation support
Patch1069: kvm-QMP-spec-Capability-negotiation-updates.patch
# For bz#559667 - QMP: JSON parser doesn't escape some control chars
Patch1070: kvm-json-escape-u0000-.-u001F-when-outputting-json.patch
# For bz#563878 - QJSON: Fix PRId64 handling
Patch1071: kvm-json-fix-PRId64-on-Win32.patch
# For bz#563875 - QJSON: Improve debugging
Patch1072: kvm-qjson-Improve-debugging.patch
# For bz#563876 - Monitor: remove unneeded checks
Patch1073: kvm-Monitor-remove-unneeded-checks.patch
# For bz#559635 - QMP: assertion on multiple faults
Patch1074: kvm-QError-Don-t-abort-on-multiple-faults.patch
# For bz#559645 - QMP: leak when a QMP connection is closed
Patch1075: kvm-QMP-Don-t-leak-on-connection-close.patch
# For bz#558623 - QMP: Basic async events are not emitted
Patch1076: kvm-QMP-Emit-Basic-events.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1077: kvm-net-add-API-to-disable-enable-polling.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1078: kvm-virtio-rename-features-guest_features.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1079: kvm-qdev-add-bit-property-type.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1080: kvm-qdev-fix-thinko-leading-to-guest-crashes.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1081: kvm-virtio-add-features-as-qdev-properties-fixup.patch
# For bz#547501 - RFE: a QMP event notification for disk  I/O errors with werror/rerror flags
Patch1082: kvm-QMP-BLOCK_IO_ERROR-event-handling.patch
# For bz#547501 - RFE: a QMP event notification for disk  I/O errors with werror/rerror flags
Patch1083: kvm-block-BLOCK_IO_ERROR-QMP-event.patch
# For bz#547501 - RFE: a QMP event notification for disk  I/O errors with werror/rerror flags
Patch1084: kvm-ide-Generate-BLOCK_IO_ERROR-QMP-event.patch
# For bz#547501 - RFE: a QMP event notification for disk  I/O errors with werror/rerror flags
Patch1085: kvm-scsi-Generate-BLOCK_IO_ERROR-QMP-event.patch
# For bz#547501 - RFE: a QMP event notification for disk  I/O errors with werror/rerror flags
Patch1086: kvm-virtio-blk-Generate-BLOCK_IO_ERROR-QMP-event.patch
# For bz#558838 - add rhel machine types
Patch1087: kvm-add-rhel-machine-types.patch
# For bz#568739 - QMP: Fix 'query-balloon' key
Patch1088: kvm-QMP-Fix-query-balloon-key-change.patch
# For bz#558835 - ide/scsi drive versions
Patch1089: kvm-ide-device-version-property.patch
# For bz#558835 - ide/scsi drive versions
Patch1090: kvm-pc-add-driver-version-compat-properties.patch
# For bz#567602 - qemu-img rebase subcommand got Segmentation fault
Patch1091: kvm-qemu-img-Fix-segfault-during-rebase.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1092: kvm-path.c-fix-warning-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1093: kvm-hw-pc.c-fix-warnings-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1094: kvm-slirp-misc.c-fix-warning-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1095: kvm-savevm.c-fix-warning-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1096: kvm-block-bochs.c-fix-warning-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1097: kvm-block.c-fix-warning-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1098: kvm-Introduce-qemu_write_full.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1099: kvm-force-to-test-result-for-qemu_write_full.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1100: kvm-block-cow.c-fix-warnings-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1101: kvm-block-qcow.c-fix-warnings-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1102: kvm-block-vmdk.o-fix-warnings-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1103: kvm-block-vvfat.c-fix-warnings-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1104: kvm-block-qcow2.c-fix-warnings-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1105: kvm-net-slirp.c-fix-warning-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1106: kvm-usb-linux.c-fix-warning-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1107: kvm-vl.c-fix-warning-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1108: kvm-monitor.c-fix-warnings-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1109: kvm-linux-user-mmap.c-fix-warnings-with-_FORTIFY_SOURCE.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1110: kvm-check-pipe-return-value.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1111: kvm-fix-qemu-kvm-_FORTIFY_SOURCE-compilation.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1112: kvm-Enable-_FORTIFY_SOURCE-2.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1113: kvm-qcow2-Fix-image-creation-regression.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1114: kvm-cow-return-errno-instead-of-1.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1115: kvm-slirp-check-system-success.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1116: kvm-qcow2-return-errno-instead-of-1.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1117: kvm-qcow-return-errno-instead-of-1.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1118: kvm-vmdk-return-errno-instead-of-1.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1119: kvm-vmdk-make-vmdk_snapshot_create-return-errno.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1120: kvm-vmdk-fix-double-free.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1121: kvm-vmdk-share-cleanup-code.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1122: kvm-block-print-errno-on-error.patch
# For bz#567099 - Allow _FORTIFY_SOURCE=2 & --enable-warning
Patch1123: kvm-documentation-qemu_write_full-don-t-work-with-non-bl.patch
# For bz#567035 - Backport changes for virtio-serial from upstream: disabling MSI, backward compat.
Patch1124: kvm-virtio-serial-pci-Allow-MSI-to-be-disabled.patch
# For bz#567035 - Backport changes for virtio-serial from upstream: disabling MSI, backward compat.
Patch1125: kvm-pc-Add-backward-compatibility-options-for-virtio-ser.patch
# For bz#567035 - Backport changes for virtio-serial from upstream: disabling MSI, backward compat.
Patch1126: kvm-virtio-serial-don-t-set-MULTIPORT-for-1-port-dev.patch
# For bz#567035 - Backport changes for virtio-serial from upstream: disabling MSI, backward compat.
Patch1127: kvm-qdev-Add-a-DEV_NVECTORS_UNSPECIFIED-enum-for-unspeci.patch
# For bz#567035 - Backport changes for virtio-serial from upstream: disabling MSI, backward compat.
Patch1128: kvm-virtio-pci-Use-DEV_NVECTORS_UNSPECIFIED-instead-of-1.patch
# For bz#569767 - Caps Lock the key's appearance  of guest is not synchronous as host's --view kvm with vnc
Patch1129: kvm-kbd-leds-infrastructure.patch
# For bz#569767 - Caps Lock the key's appearance  of guest is not synchronous as host's --view kvm with vnc
Patch1130: kvm-kbd-leds-ps-2-kbd.patch
# For bz#569767 - Caps Lock the key's appearance  of guest is not synchronous as host's --view kvm with vnc
Patch1131: kvm-kbd-leds-usb-kbd.patch
# For bz#569767 - Caps Lock the key's appearance  of guest is not synchronous as host's --view kvm with vnc
Patch1132: kvm-kbd-keds-vnc.patch
# For bz#570174 - Restoring a qemu guest from a saved state file using -incoming sometimes fails and hangs
Patch1133: kvm-migration-Clear-fd-also-in-error-cases.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1134: kvm-qemu-memory-notifiers.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1135: kvm-tap-add-interface-to-get-device-fd.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1136: kvm-add-API-to-set-ioeventfd.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1137: kvm-notifier-event-notifier-implementation.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1138: kvm-virtio-add-notifier-support.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1139: kvm-virtio-add-APIs-for-queue-fields.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1140: kvm-virtio-add-set_status-callback.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1141: kvm-virtio-move-typedef-to-qemu-common.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1142: kvm-virtio-pci-fill-in-notifier-support.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1143: kvm-vhost-vhost-net-support.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1144: kvm-tap-add-vhost-vhostfd-options.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1145: kvm-tap-add-API-to-retrieve-vhost-net-header.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1146: kvm-virtio-net-vhost-net-support.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1147: kvm-qemu-kvm-add-vhost.h-header.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1148: kvm-irqfd-support.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1149: kvm-msix-add-mask-unmask-notifiers.patch
# For bz#562958 - RFE: Support vhost net mode
Patch1150: kvm-virtio-pci-irqfd-support.patch
# For bz#549757 - Provide SPICE support  / -spice command line argument
Patch1151: kvm-add-spice-into-the-configure-file.patch
# For bz#549757 - Provide SPICE support  / -spice command line argument
Patch1152: kvm-spice-core-bits.patch
# For bz#549757 - Provide SPICE support  / -spice command line argument
Patch1153: kvm-spice-add-keyboard.patch
# For bz#549757 - Provide SPICE support  / -spice command line argument
Patch1154: kvm-spice-add-mouse.patch
# For bz#549757 - Provide SPICE support  / -spice command line argument
Patch1155: kvm-spice-simple-display.patch
# For bz#549757 - Provide SPICE support  / -spice command line argument
Patch1156: kvm-move-x509-file-name-defines-to-qemu-x509.h.patch
# For bz#549757 - Provide SPICE support  / -spice command line argument
Patch1157: kvm-spice-tls-support.patch
# For bz#549757 - Provide SPICE support  / -spice command line argument
Patch1158: kvm-spice-configure-listening-addr.patch
# For bz#549757 - Provide SPICE support  / -spice command line argument
Patch1159: kvm-spice-add-qxl-device.patch
# For bz#574211 - spice: add tablet support
Patch1160: kvm-spice-add-tablet.patch
# For bz#574212 - spice:wake spice server only when idle
Patch1161: kvm-spice-simple-display-wake-spice-server-only-when-idl.patch
# For bz#574214 - qxl: switch qxl from native into vga mode on vga register access
Patch1162: kvm-spice-qxl-switch-back-to-vga-mode-on-register-access.patch
# For bz#568820 - EMBARGOED CVE-2010-0431 qemu: Insufficient guest provided pointers validation [rhel-6.0]
Patch1163: kvm-spice-qxl-ring-access-security-fix.patch
# For bz#525935 - RFE: expire vnc password
Patch1164: kvm-vnc-support-password-expire.patch
# For bz#525935 - RFE: expire vnc password
Patch1165: kvm-spice-vnc-add-__com.redhat_set_password-monitor-comm.patch
# For bz#574222 - spice: add audio support
Patch1166: kvm-spice-add-audio-support.patch
# For bz#574225 - spice: add config options
Patch1167: kvm-spice-make-image-compression-configurable.patch
# For bz#574225 - spice: add config options
Patch1168: kvm-spice-configure-channel-security.patch
# For bz#574225 - spice: add config options
Patch1169: kvm-spice-configure-renderer.patch
# For bz#558957 - A QMP event notification on SPICE client connect/disconnect events
Patch1170: kvm-spice-send-connect-disconnect-monitor-events.patch
# For bz#574853 - spice/qxl: add qxl to -vga help text
Patch1171: kvm-spice-qxl-update-vga-help-text-indicating-qxl-is-the.patch
# For bz#574849 - spice: client migration support
Patch1172: kvm-spice-notifying-spice-when-migration-starts-and-ends.patch
# For bz#574849 - spice: client migration support
Patch1173: kvm-spice-add-__com.redhat_spice_migrate_info-monitor-co.patch
# For bz#567940 - qcow2 corruption with I/O error during refcount block allocation
Patch1174: kvm-qcow2-Factor-next_refcount_table_size-out.patch
# For bz#567940 - qcow2 corruption with I/O error during refcount block allocation
Patch1175: kvm-qcow2-Rewrite-alloc_refcount_block-grow_refcount_tab.patch
# For bz#567940 - qcow2 corruption with I/O error during refcount block allocation
Patch1176: kvm-qcow2-More-checks-for-qemu-img-check.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1177: kvm-spice-virtual-machine-channel-replacement-for-remove.patch
# For bz#558835 - ide/scsi drive versions
Patch1178: kvm-scsi-device-version-property.patch
# For bz#558835 - ide/scsi drive versions
Patch1179: kvm-scsi-disk-fix-buffer-overflow.patch
# For bz#574939 - Memory statistics support
Patch1180: kvm-New-API-for-asynchronous-monitor-commands.patch
# For bz#574939 - Memory statistics support
Patch1181: kvm-Revert-QMP-Fix-query-balloon-key-change.patch
# For bz#574939 - Memory statistics support
Patch1182: kvm-virtio-Add-memory-statistics-reporting-to-the-balloo.patch
# For bz#574525 - Align qemu-kvm guest memory for transparent hugepage support
Patch1183: kvm-Transparent-Hugepage-Support-3.patch
# For bz#574642 - QMP: Convert do_cpu_set() to QObject
Patch1184: kvm-monitor-Don-t-check-for-mon_get_cpu-failure.patch
# For bz#574642 - QMP: Convert do_cpu_set() to QObject
Patch1185: kvm-QError-New-QERR_OPEN_FILE_FAILED.patch
# For bz#574642 - QMP: Convert do_cpu_set() to QObject
Patch1186: kvm-monitor-convert-do_memory_save-to-QError.patch
# For bz#574642 - QMP: Convert do_cpu_set() to QObject
Patch1187: kvm-monitor-convert-do_physical_memory_save-to-QError.patch
# For bz#574642 - QMP: Convert do_cpu_set() to QObject
Patch1188: kvm-QError-New-QERR_INVALID_CPU_INDEX.patch
# For bz#574642 - QMP: Convert do_cpu_set() to QObject
Patch1189: kvm-monitor-convert-do_cpu_set-to-QObject-QError.patch
# For bz#575800 - Monitor: Backport a collection of fixes
Patch1190: kvm-monitor-Use-QERR_INVALID_PARAMETER-instead-of-QERR_I.patch
# For bz#575800 - Monitor: Backport a collection of fixes
Patch1191: kvm-Revert-QError-New-QERR_INVALID_CPU_INDEX.patch
# For bz#575800 - Monitor: Backport a collection of fixes
Patch1192: kvm-json-parser-Fix-segfault-on-malformed-input.patch
# For bz#575800 - Monitor: Backport a collection of fixes
Patch1193: kvm-fix-i-format-handling-in-memory-dump.patch
# For bz#575800 - Monitor: Backport a collection of fixes
Patch1194: kvm-Don-t-set-default-monitor-when-there-is-a-mux-ed-one.patch
# For bz#575821 - QMP: Convert migrate_set_speed, migrate_set_downtime to QObject
Patch1195: kvm-monitor-Document-argument-type-M.patch
# For bz#575821 - QMP: Convert migrate_set_speed, migrate_set_downtime to QObject
Patch1196: kvm-QDict-New-qdict_get_double.patch
# For bz#575821 - QMP: Convert migrate_set_speed, migrate_set_downtime to QObject
Patch1197: kvm-monitor-New-argument-type-b.patch
# For bz#575821 - QMP: Convert migrate_set_speed, migrate_set_downtime to QObject
Patch1198: kvm-monitor-Use-argument-type-b-for-migrate_set_speed.patch
# For bz#575821 - QMP: Convert migrate_set_speed, migrate_set_downtime to QObject
Patch1199: kvm-monitor-convert-do_migrate_set_speed-to-QObject.patch
# For bz#575821 - QMP: Convert migrate_set_speed, migrate_set_downtime to QObject
Patch1200: kvm-monitor-New-argument-type-T.patch
# For bz#575821 - QMP: Convert migrate_set_speed, migrate_set_downtime to QObject
Patch1201: kvm-monitor-Use-argument-type-T-for-migrate_set_downtime.patch
# For bz#575821 - QMP: Convert migrate_set_speed, migrate_set_downtime to QObject
Patch1202: kvm-monitor-convert-do_migrate_set_downtime-to-QObject.patch
# For bz#575912 - QMP: Backport event related fixes
Patch1203: kvm-block-Emit-BLOCK_IO_ERROR-before-vm_stop-call.patch
# For bz#575912 - QMP: Backport event related fixes
Patch1204: kvm-QMP-Move-STOP-event-into-do_vm_stop.patch
# For bz#575912 - QMP: Backport event related fixes
Patch1205: kvm-QMP-Move-RESET-event-into-qemu_system_reset.patch
# For bz#575912 - QMP: Backport event related fixes
Patch1206: kvm-QMP-Sync-with-upstream-event-changes.patch
# For bz#575912 - QMP: Backport event related fixes
Patch1207: kvm-QMP-Drop-DEBUG-event.patch
# For bz#575912 - QMP: Backport event related fixes
Patch1208: kvm-QMP-Revamp-the-qmp-events.txt-file.patch
# For bz#547534 - RFE: a QMP event notification for RTC clock changes
Patch1209: kvm-QMP-Introduce-RTC_CHANGE-event.patch
# For bz#557083 - QMP events for watchdog events
Patch1210: kvm-QMP-Introduce-WATCHDOG-event.patch
# For bz#576561 - spice: add more config options
Patch1211: kvm-spice-add-more-config-options.patch
# For bz#576561 - spice: add more config options
Patch1212: kvm-Revert-spice-add-more-config-options.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1213: kvm-Fix-kvm_load_mpstate-for-vcpu-hot-add.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1214: kvm-qemu-kvm-enable-get-set-vcpu-events-on-reset-and-mig.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1215: kvm-Synchronize-kvm-headers.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1216: kvm-Increase-VNC_MAX_WIDTH.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1217: kvm-device-assignment-default-requires-IOMMU.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1218: kvm-Do-not-allow-vcpu-stop-with-in-progress-PIO.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1219: kvm-fix-savevm-command-without-id-or-tag.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1220: kvm-Do-not-ignore-error-if-open-file-failed-serial-dev-t.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1221: kvm-segfault-due-to-buffer-overrun-in-usb-serial.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1222: kvm-fix-inet_parse-typo.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1223: kvm-virtio-net-fix-network-stall-under-load.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1224: kvm-don-t-dereference-NULL-after-failed-strdup.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1225: kvm-net-Remove-unused-net_client_uninit.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1226: kvm-net-net_check_clients-runs-too-early-to-see-device-f.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1227: kvm-net-Fix-bogus-Warning-vlan-0-with-no-nics-with-devic.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1228: kvm-net-net_check_clients-checks-only-VLAN-clients-fix.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1229: kvm-net-info-network-shows-only-VLAN-clients-fix.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1230: kvm-net-Monitor-command-set_link-finds-only-VLAN-clients.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1231: kvm-ide-save-restore-pio-atapi-cmd-transfer-fields-and-i.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1232: kvm-cirrus-Properly-re-register-cirrus_linear_io_addr-on.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1233: kvm-Monitor-Introduce-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1234: kvm-Monitor-Convert-simple-handlers-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1235: kvm-Monitor-Convert-do_cont-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1236: kvm-Monitor-Convert-do_eject-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1237: kvm-Monitor-Convert-do_cpu_set-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1238: kvm-Monitor-Convert-do_block_set_passwd-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1239: kvm-Monitor-Convert-do_getfd-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1240: kvm-Monitor-Convert-do_closefd-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1241: kvm-Monitor-Convert-pci_device_hot_add-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1242: kvm-Monitor-Convert-pci_device_hot_remove-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1243: kvm-Monitor-Convert-do_migrate-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1244: kvm-Monitor-Convert-do_memory_save-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1245: kvm-Monitor-Convert-do_physical_memory_save-to-cmd_new_r.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1246: kvm-Monitor-Convert-do_info-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1247: kvm-Monitor-Convert-do_change-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1248: kvm-Monitor-Convert-to-mon_set_password-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1249: kvm-Monitor-Convert-mon_spice_migrate-to-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1250: kvm-Monitor-Rename-cmd_new_ret.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1251: kvm-Monitor-Debugging-support.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1252: kvm-Monitor-Drop-the-print-disabling-mechanism.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1253: kvm-Monitor-Audit-handler-return.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1254: kvm-Monitor-Debug-stray-prints-the-right-way.patch
# For bz#563491 - QMP: New internal error handling mechanism
Patch1255: kvm-Monitor-Report-more-than-one-error-in-handlers.patch
# For bz#563641 - QMP: Wrong error message in block_passwd command
Patch1256: kvm-QError-New-QERR_DEVICE_NOT_ENCRYPTED.patch
# For bz#563641 - QMP: Wrong error message in block_passwd command
Patch1257: kvm-Wrong-error-message-in-block_passwd-command.patch
# For bz#578493 - QMP: Fix spice event names
Patch1258: kvm-Monitor-Introduce-RFQDN_REDHAT-and-use-it.patch
# For bz#578493 - QMP: Fix spice event names
Patch1259: kvm-QMP-Fix-Spice-event-names.patch
# For bz#558236 - qemu-kvm monitor corrupts tty on exit
Patch1260: kvm-char-Remove-redundant-qemu_chr_generic_open-call.patch
# For bz#558236 - qemu-kvm monitor corrupts tty on exit
Patch1261: kvm-add-close-callback-for-tty-based-char-device.patch
# For bz#558236 - qemu-kvm monitor corrupts tty on exit
Patch1262: kvm-Restore-terminal-attributes-for-tty-based-monitor.patch
# For bz#558236 - qemu-kvm monitor corrupts tty on exit
Patch1263: kvm-Restore-terminal-monitor-attributes-addition.patch
# For bz#578912 - Monitor: Overflow in 'info balloon'
Patch1264: kvm-balloon-Fix-overflow-when-reporting-actual-memory-si.patch
# For bz#576544 - Error message doesn't contain the content of invalid keyword
Patch1265: kvm-json-parser-Output-the-content-of-invalid-keyword.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1266: kvm-read-only-Make-CDROM-a-read-only-drive.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1267: kvm-read-only-BDRV_O_FLAGS-cleanup.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1268: kvm-read-only-Added-drives-readonly-option.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1269: kvm-read-only-Disable-fall-back-to-read-only.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1270: kvm-read-only-No-need-anymoe-for-bdrv_set_read_only.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1271: kvm-read_only-Ask-for-read-write-permissions-when-openin.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1272: kvm-read-only-Read-only-device-changed-to-opens-it-s-fil.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1273: kvm-read-only-qemu-img-Fix-qemu-img-can-t-create-qcow-im.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1274: kvm-block-clean-up-bdrv_open2-structure-a-bit.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1275: kvm-block-saner-flags-filtering-in-bdrv_open2.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1276: kvm-block-flush-backing_hd-in-the-right-place.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1277: kvm-block-fix-cache-flushing-in-bdrv_commit.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1278: kvm-block-more-read-only-changes-related-to-backing-file.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1279: kvm-read-only-minor-cleanup.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1280: kvm-read-only-Another-minor-cleanup.patch
# For bz#537164 - -drive arg has no way to request a read only disk
Patch1281: kvm-read-only-allow-read-only-CDROM-with-any-interface.patch
# For bz#580028 - 'qemu-img re-base' broken on block devices
Patch1282: kvm-qemu-img-rebase-Add-f-option.patch
# For bz#579974 - Get segmentation fault when creating qcow2 format image on block device with "preallocation=metadata"
Patch1283: kvm-qemu-io-Fix-return-value-handling-of-bdrv_open.patch
# For bz#579974 - Get segmentation fault when creating qcow2 format image on block device with "preallocation=metadata"
Patch1284: kvm-qemu-nbd-Fix-return-value-handling-of-bdrv_open.patch
# For bz#579974 - Get segmentation fault when creating qcow2 format image on block device with "preallocation=metadata"
Patch1285: kvm-qemu-img-Fix-error-message.patch
# For bz#579974 - Get segmentation fault when creating qcow2 format image on block device with "preallocation=metadata"
Patch1286: kvm-Replace-calls-of-old-bdrv_open.patch
# For bz#564101 - [RFE] topology support in the virt block layer
Patch1287: kvm-virtio-blk-revert-serial-number-support.patch
# For bz#564101 - [RFE] topology support in the virt block layer
Patch1288: kvm-block-add-topology-qdev-properties.patch
# For bz#564101 - [RFE] topology support in the virt block layer
Patch1289: kvm-virtio-blk-add-topology-support.patch
# For bz#564101 - [RFE] topology support in the virt block layer
Patch1290: kvm-scsi-add-topology-support.patch
# For bz#564101 - [RFE] topology support in the virt block layer
Patch1291: kvm-ide-add-topology-support.patch
# For bz#580140 - emulated pcnet nic in qemu-kvm has wrong PCI subsystem ID for Windows XP driver
Patch1292: kvm-pcnet-make-subsystem-vendor-id-match-hardware.patch
# For bz#569661 - RHEL6.0 requires backport of upstream cpu model support..
Patch1293: cpu-model-config-1.patch
# For bz#569661 - RHEL6.0 requires backport of upstream cpu model support..
Patch1294: cpu-model-config-2.patch
# For bz#569661 - RHEL6.0 requires backport of upstream cpu model support..
Patch1295: cpu-model-config-3.patch
# For bz#569661 - RHEL6.0 requires backport of upstream cpu model support..
Patch1296: cpu-model-config-4.patch
# For bz#561078 - "Cannot boot from non-existent NIC" when using virt-install --pxe
Patch1297: kvm-net-remove-NICInfo.bootable-field.patch
# For bz#561078 - "Cannot boot from non-existent NIC" when using virt-install --pxe
Patch1298: kvm-net-remove-broken-net_set_boot_mask-boot-device-vali.patch
# For bz#561078 - "Cannot boot from non-existent NIC" when using virt-install --pxe
Patch1299: kvm-boot-remove-unused-boot_devices_bitmap-variable.patch
# For bz#580109 - vhost net lacks upstream fixes
Patch1300: kvm-check-kvm-enabled.patch
# For bz#580109 - vhost net lacks upstream fixes
Patch1301: kvm-qemu-rename-notifier-event_notifier.patch
# For bz#580109 - vhost net lacks upstream fixes
Patch1302: kvm-virtio-API-name-cleanup.patch
# For bz#580109 - vhost net lacks upstream fixes
Patch1303: kvm-vhost-u_int64_t-uint64_t.patch
# For bz#580109 - vhost net lacks upstream fixes
Patch1304: kvm-virtio-pci-fix-coding-style.patch
# For bz#580109 - vhost net lacks upstream fixes
Patch1305: kvm-vhost-detect-lack-of-support-earlier-style.patch
# For bz#580109 - vhost net lacks upstream fixes
Patch1306: kvm-configure-vhost-related-fixes.patch
# For bz#580109 - vhost net lacks upstream fixes
Patch1307: kvm-vhost-fix-features-ack.patch
# For bz#580109 - vhost net lacks upstream fixes
Patch1308: kvm-vhost-net-disable-mergeable-buffers.patch
# For bz#579470 - QMP: device_add support
Patch1309: kvm-qemu-option-Make-qemu_opts_foreach-accumulate-return.patch
# For bz#579470 - QMP: device_add support
Patch1310: kvm-qdev-Fix-exit-code-for-device.patch
# For bz#579470 - QMP: device_add support
Patch1311: kvm-qdev-Add-help-for-device-properties.patch
# For bz#579470 - QMP: device_add support
Patch1312: kvm-qdev-update-help-on-device.patch
# For bz#579470 - QMP: device_add support
Patch1313: kvm-qdev-Add-rudimentary-help-for-property-value.patch
# For bz#579470 - QMP: device_add support
Patch1314: kvm-qdev-Free-opts-on-failed-do_device_add.patch
# For bz#579470 - QMP: device_add support
Patch1315: kvm-qdev-Improve-diagnostics-for-bad-property-values.patch
# For bz#579470 - QMP: device_add support
Patch1316: kvm-qdev-Catch-attempt-to-attach-more-than-one-device-to.patch
# For bz#579470 - QMP: device_add support
Patch1317: kvm-usb-Remove-disabled-monitor_printf-in-usb_read_file.patch
# For bz#579470 - QMP: device_add support
Patch1318: kvm-savevm-Fix-loadvm-to-report-errors-to-stderr-not-the.patch
# For bz#579470 - QMP: device_add support
Patch1319: kvm-pc-Fix-error-reporting-for-boot-once.patch
# For bz#579470 - QMP: device_add support
Patch1320: kvm-pc-Factor-common-code-out-of-pc_boot_set-and-cmos_in.patch
# For bz#579470 - QMP: device_add support
Patch1321: kvm-tools-Remove-unused-cur_mon-from-qemu-tool.c.patch
# For bz#579470 - QMP: device_add support
Patch1322: kvm-monitor-Separate-default-monitor-and-current-monitor.patch
# For bz#579470 - QMP: device_add support
Patch1323: kvm-block-Simplify-usb_msd_initfn-test-for-can-read-bdrv.patch
# For bz#579470 - QMP: device_add support
Patch1324: kvm-monitor-Factor-monitor_set_error-out-of-qemu_error_i.patch
# For bz#579470 - QMP: device_add support
Patch1325: kvm-error-Move-qemu_error-friends-from-monitor.c-to-own-.patch
# For bz#579470 - QMP: device_add support
Patch1326: kvm-error-Simplify-error-sink-setup.patch
# For bz#579470 - QMP: device_add support
Patch1327: kvm-error-Move-qemu_error-friends-into-their-own-header.patch
# For bz#579470 - QMP: device_add support
Patch1328: kvm-error-New-error_printf-and-error_vprintf.patch
# For bz#579470 - QMP: device_add support
Patch1329: kvm-error-Don-t-abuse-qemu_error-for-non-error-in-qdev_d.patch
# For bz#579470 - QMP: device_add support
Patch1330: kvm-error-Don-t-abuse-qemu_error-for-non-error-in-qbus_f.patch
# For bz#579470 - QMP: device_add support
Patch1331: kvm-error-Don-t-abuse-qemu_error-for-non-error-in-scsi_h.patch
# For bz#579470 - QMP: device_add support
Patch1332: kvm-error-Replace-qemu_error-by-error_report.patch
# For bz#579470 - QMP: device_add support
Patch1333: kvm-error-Rename-qemu_error_new-to-qerror_report.patch
# For bz#579470 - QMP: device_add support
Patch1334: kvm-error-Infrastructure-to-track-locations-for-error-re.patch
# For bz#579470 - QMP: device_add support
Patch1335: kvm-error-Include-the-program-name-in-error-messages-to-.patch
# For bz#579470 - QMP: device_add support
Patch1336: kvm-error-Track-locations-in-configuration-files.patch
# For bz#579470 - QMP: device_add support
Patch1337: kvm-QemuOpts-Fix-qemu_config_parse-to-catch-file-read-er.patch
# For bz#579470 - QMP: device_add support
Patch1338: kvm-error-Track-locations-on-command-line.patch
# For bz#579470 - QMP: device_add support
Patch1339: kvm-qdev-Fix-device-and-device_add-to-handle-unsuitable-.patch
# For bz#579470 - QMP: device_add support
Patch1340: kvm-qdev-Factor-qdev_create_from_info-out-of-qdev_create.patch
# For bz#579470 - QMP: device_add support
Patch1341: kvm-qdev-Hide-no_user-devices-from-users.patch
# For bz#579470 - QMP: device_add support
Patch1342: kvm-qdev-Hide-ptr-properties-from-users.patch
# For bz#579470 - QMP: device_add support
Patch1343: kvm-monitor-New-monitor_cur_is_qmp.patch
# For bz#579470 - QMP: device_add support
Patch1344: kvm-error-Let-converted-handlers-print-in-human-monitor.patch
# For bz#579470 - QMP: device_add support
Patch1345: kvm-error-Polish-human-readable-error-descriptions.patch
# For bz#579470 - QMP: device_add support
Patch1346: kvm-error-New-QERR_PROPERTY_NOT_FOUND.patch
# For bz#579470 - QMP: device_add support
Patch1347: kvm-error-New-QERR_PROPERTY_VALUE_BAD.patch
# For bz#579470 - QMP: device_add support
Patch1348: kvm-error-New-QERR_PROPERTY_VALUE_IN_USE.patch
# For bz#579470 - QMP: device_add support
Patch1349: kvm-error-New-QERR_PROPERTY_VALUE_NOT_FOUND.patch
# For bz#579470 - QMP: device_add support
Patch1350: kvm-qdev-convert-setting-device-properties-to-QError.patch
# For bz#579470 - QMP: device_add support
Patch1351: kvm-qdev-Relax-parsing-of-bus-option.patch
# For bz#579470 - QMP: device_add support
Patch1352: kvm-error-New-QERR_BUS_NOT_FOUND.patch
# For bz#579470 - QMP: device_add support
Patch1353: kvm-error-New-QERR_DEVICE_MULTIPLE_BUSSES.patch
# For bz#579470 - QMP: device_add support
Patch1354: kvm-error-New-QERR_DEVICE_NO_BUS.patch
# For bz#579470 - QMP: device_add support
Patch1355: kvm-qdev-Convert-qbus_find-to-QError.patch
# For bz#579470 - QMP: device_add support
Patch1356: kvm-error-New-error_printf_unless_qmp.patch
# For bz#579470 - QMP: device_add support
Patch1357: kvm-error-New-QERR_BAD_BUS_FOR_DEVICE.patch
# For bz#579470 - QMP: device_add support
Patch1358: kvm-error-New-QERR_BUS_NO_HOTPLUG.patch
# For bz#579470 - QMP: device_add support
Patch1359: kvm-error-New-QERR_DEVICE_INIT_FAILED.patch
# For bz#579470 - QMP: device_add support
Patch1360: kvm-error-New-QERR_NO_BUS_FOR_DEVICE.patch
# For bz#579470 - QMP: device_add support
Patch1361: kvm-Revert-qdev-Use-QError-for-device-not-found-error.patch
# For bz#579470 - QMP: device_add support
Patch1362: kvm-error-Convert-do_device_add-to-QError.patch
# For bz#579470 - QMP: device_add support
Patch1363: kvm-qemu-option-Functions-to-convert-to-from-QDict.patch
# For bz#579470 - QMP: device_add support
Patch1364: kvm-qemu-option-Move-the-implied-first-name-into-QemuOpt.patch
# For bz#579470 - QMP: device_add support
Patch1365: kvm-qemu-option-Rename-find_list-to-qemu_find_opts-exter.patch
# For bz#579470 - QMP: device_add support
Patch1366: kvm-monitor-New-argument-type-O.patch
# For bz#579470 - QMP: device_add support
Patch1367: kvm-monitor-Use-argument-type-O-for-device_add.patch
# For bz#579470 - QMP: device_add support
Patch1368: kvm-monitor-convert-do_device_add-to-QObject.patch
# For bz#579470 - QMP: device_add support
Patch1369: kvm-error-Trim-includes-after-Move-qemu_error-friends.patch
# For bz#579470 - QMP: device_add support
Patch1370: kvm-error-Trim-includes-in-qerror.c.patch
# For bz#579470 - QMP: device_add support
Patch1371: kvm-error-Trim-includes-after-Infrastructure-to-track-lo.patch
# For bz#579470 - QMP: device_add support
Patch1372: kvm-error-Make-use-of-error_set_progname-optional.patch
# For bz#579470 - QMP: device_add support
Patch1373: kvm-error-Link-qemu-img-qemu-nbd-qemu-io-with-qemu-error.patch
# For bz#579470 - QMP: device_add support
Patch1374: kvm-error-Move-qerror_report-from-qemu-error.-ch-to-qerr.patch
# For bz#576561 - spice: add more config options
Patch1375: kvm-spice-add-more-config-options-readd.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1376: kvm-Documentation-Add-monitor-commands-to-function-index.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1377: kvm-error-Put-error-definitions-back-in-alphabetical-ord.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1378: kvm-error-New-QERR_DUPLICATE_ID.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1379: kvm-error-Convert-qemu_opts_create-to-QError.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1380: kvm-error-New-QERR_INVALID_PARAMETER_VALUE.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1381: kvm-error-Convert-qemu_opts_set-to-QError.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1382: kvm-error-Drop-extra-messages-after-qemu_opts_set-and-qe.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1383: kvm-error-Use-QERR_INVALID_PARAMETER_VALUE-instead-of-QE.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1384: kvm-error-Convert-qemu_opts_validate-to-QError.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1385: kvm-error-Convert-net_client_init-to-QError.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1386: kvm-error-New-QERR_DEVICE_IN_USE.patch
# For bz#559670 - No 'netdev_add' command in monitor
Patch1387: kvm-monitor-New-commands-netdev_add-netdev_del.patch
# For bz#582325 - QMP: device_del support
Patch1388: kvm-qdev-Convert-qdev_unplug-to-QError.patch
# For bz#582325 - QMP: device_del support
Patch1389: kvm-monitor-convert-do_device_del-to-QObject-QError.patch
# For bz#582575 - Backport bdrv_aio_multiwrite fixes
Patch1390: kvm-block-Fix-error-code-in-multiwrite-for-immediate-fai.patch
# For bz#582575 - Backport bdrv_aio_multiwrite fixes
Patch1391: kvm-block-Fix-multiwrite-memory-leak-in-error-case.patch
# For bz#581540 - SPICE graphics event does not include auth details
Patch1392: kvm-spice-add-auth-info-to-monitor-events.patch
# For bz#569613 - backport qemu-kvm-0.12.3 fixes to RHEL6
Patch1393: kvm-Request-setting-of-nmi_pending-and-sipi_vector.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1394: kvm-virtio-serial-save-load-Ensure-target-has-enough-por.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1395: kvm-virtio-serial-save-load-Ensure-nr_ports-on-src-and-d.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1396: kvm-virtio-serial-save-load-Ensure-we-have-hot-plugged-p.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1397: kvm-virtio-serial-save-load-Send-target-host-connection-.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1398: kvm-virtio-serial-Use-control-messages-to-notify-guest-o.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1399: kvm-virtio-serial-whitespace-match-surrounding-code.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1400: kvm-virtio-serial-Remove-redundant-check-for-0-sized-wri.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1401: kvm-virtio-serial-Update-copyright-year-to-2010.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1402: kvm-virtio-serial-Propagate-errors-in-initialising-ports.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1403: kvm-virtio-serial-Send-out-guest-data-to-ports-only-if-p.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1404: kvm-iov-Introduce-a-new-file-for-helpers-around-iovs-add.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1405: kvm-iov-Add-iov_to_buf-and-iov_size-helpers.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1406: kvm-virtio-serial-Handle-scatter-gather-buffers-for-cont.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1407: kvm-virtio-serial-Handle-scatter-gather-input-from-the-g.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1408: kvm-virtio-serial-Apps-should-consume-all-data-that-gues.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1409: kvm-virtio-serial-Discard-data-that-guest-sends-us-when-.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1410: kvm-virtio-serial-Implement-flow-control-for-individual-.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1411: kvm-virtio-serial-Handle-output-from-guest-to-unintialis.patch
# For bz#574296 - Fix migration for virtio-serial after port hot-plug/hot-unplug operations
Patch1412: kvm-virtio-serial-bus-wake-up-iothread-upon-guest-read-n.patch
# For bz#587227 - Fix segfault when creating more vcpus than allowed.
Patch1413: kvm-Bail-out-when-VCPU_CREATE-fails.patch
# For bz#586572 - virtio-blk multiwrite merge memory leak
Patch1414: kvm-block-Free-iovec-arrays-allocated-by-multiwrite_merg.patch
# For bz#588828 - endless loop when parsing of command line with bare image argument
Patch1415: kvm-vl.c-fix-BZ-588828-endless-loop-caused-by-non-option.patch
# For bz#584902 - Cannot associate drive with a floppy device using -global
Patch1416: kvm-fdc-fix-drive-property-handling.patch
# For bz#585837 - After re-base snapshot, the file in the snapshot disappeared
Patch1417: kvm-qemu-img-use-the-heap-instead-of-the-huge-stack-arra.patch
# For bz#585837 - After re-base snapshot, the file in the snapshot disappeared
Patch1418: kvm-qemu-img-rebase-Fix-output-image-corruption.patch
# For bz#578448 - qemu-kvm segfault when nfs restart(without using werror&rerror)
Patch1419: kvm-virtio-blk-Fix-use-after-free-in-error-case.patch
# For bz#578448 - qemu-kvm segfault when nfs restart(without using werror&rerror)
Patch1420: kvm-block-Fix-multiwrite-error-handling.patch
# For bz#579692 - qemu-kvm "-boot once=drives" couldn't function properly
Patch1421: kvm-Fix-boot-once-option.patch
# For bz#573578 - Segfault when migrating via QMP command interface
Patch1422: kvm-QError-New-QERR_QMP_BAD_INPUT_OBJECT_MEMBER.patch
# For bz#573578 - Segfault when migrating via QMP command interface
Patch1423: kvm-QMP-Use-QERR_QMP_BAD_INPUT_OBJECT_MEMBER.patch
# For bz#573578 - Segfault when migrating via QMP command interface
Patch1424: kvm-QError-Improve-QERR_QMP_BAD_INPUT_OBJECT-desc.patch
# For bz#573578 - Segfault when migrating via QMP command interface
Patch1425: kvm-QMP-Check-arguments-member-s-type.patch
# For bz#590102 - QMP: Backport RESUME event
Patch1426: kvm-QMP-Introduce-RESUME-event.patch
# For bz#588133 - RHEL5.4 guest can lose virtio networking during migration
Patch1427: kvm-pci-irq_state-vmstate-breakage.patch
# For bz#588756 - blkdebug is missing
Patch1428: kvm-qemu-config-qemu_read_config_file-reads-the-normal-c.patch
# For bz#588756 - blkdebug is missing
Patch1429: kvm-qemu-config-Make-qemu_config_parse-more-generic.patch
# For bz#588756 - blkdebug is missing
Patch1430: kvm-blkdebug-Basic-request-passthrough.patch
# For bz#588756 - blkdebug is missing
Patch1431: kvm-blkdebug-Inject-errors.patch
# For bz#588756 - blkdebug is missing
Patch1432: kvm-Make-qemu-config-available-for-tools.patch
# For bz#588756 - blkdebug is missing
Patch1433: kvm-blkdebug-Add-events-and-rules.patch
# For bz#588756 - blkdebug is missing
Patch1434: kvm-qcow2-Trigger-blkdebug-events.patch
# For bz#588762 - Backport qcow2 fixes
Patch1435: kvm-qcow2-Fix-access-after-end-of-array.patch
# For bz#588762 - Backport qcow2 fixes
Patch1436: kvm-qcow2-rename-two-QCowAIOCB-members.patch
# For bz#588762 - Backport qcow2 fixes
Patch1437: kvm-qcow2-Don-t-ignore-immediate-read-write-failures.patch
# For bz#588762 - Backport qcow2 fixes
Patch1438: kvm-qcow2-Remove-request-from-in-flight-list-after-error.patch
# For bz#588762 - Backport qcow2 fixes
Patch1439: kvm-qcow2-Return-0-errno-in-write_l2_entries.patch
# For bz#588762 - Backport qcow2 fixes
Patch1440: kvm-qcow2-Fix-error-return-code-in-qcow2_alloc_cluster_l.patch
# For bz#588762 - Backport qcow2 fixes
Patch1441: kvm-qcow2-Return-0-errno-in-write_l1_entry.patch
# For bz#588762 - Backport qcow2 fixes
Patch1442: kvm-qcow2-Return-0-errno-in-l2_allocate.patch
# For bz#588762 - Backport qcow2 fixes
Patch1443: kvm-qcow2-Remove-abort-on-free_clusters-failure.patch
# For bz#591061 - make fails to build after make clean
Patch1444: kvm-Add-qemu-error.o-only-once-to-target-list.patch
# For bz#589439 - Qcow2 snapshot got corruption after commit using block device
Patch1445: kvm-block-Fix-bdrv_commit.patch
# For bz#578106 - call trace when boot guest with -cpu host
Patch1446: kvm-fix-80000001.EDX-supported-bit-filtering.patch
# For bz#591604 - cannot override cpu vendor from the command line
Patch1447: kvm-fix-CPUID-vendor-override.patch
# For bz#588884 - Rebooting a kernel with kvmclock enabled, into a kernel with kvmclock disabled, causes random crashes
Patch1448: kvm-turn-off-kvmclock-when-resetting-cpu.patch
# For bz#593369 - virtio-blk: Avoid zeroing every request structure
Patch1449: kvm-virtio-blk-Avoid-zeroing-every-request-structure.patch
# For bz#580363 - Error while creating raw image on block device
Patch1450: kvm-dmg-fix-open-failure.patch
# For bz#580363 - Error while creating raw image on block device
Patch1451: kvm-block-get-rid-of-the-BDRV_O_FILE-flag.patch
# For bz#580363 - Error while creating raw image on block device
Patch1452: kvm-block-Convert-first_drv-to-QLIST.patch
# For bz#580363 - Error while creating raw image on block device
Patch1453: kvm-block-separate-raw-images-from-the-file-protocol.patch
# For bz#580363 - Error while creating raw image on block device
Patch1454: kvm-block-Split-bdrv_open.patch
# For bz#580363 - Error while creating raw image on block device
Patch1455: kvm-block-Avoid-forward-declaration-of-bdrv_open_common.patch
# For bz#580363 - Error while creating raw image on block device
Patch1456: kvm-block-Open-the-underlying-image-file-in-generic-code.patch
# For bz#580363 - Error while creating raw image on block device
Patch1457: kvm-block-bdrv_has_zero_init.patch
# For bz#590998 - qcow2 high watermark
Patch1458: kvm-block-Do-not-export-bdrv_first.patch
# For bz#590998 - qcow2 high watermark
Patch1459: kvm-block-Convert-bdrv_first-to-QTAILQ.patch
# For bz#590998 - qcow2 high watermark
Patch1460: kvm-block-Add-wr_highest_sector-blockstat.patch
# For bz#582684 - Monitor: getfd command is broken
Patch1461: kvm-stash-away-SCM_RIGHTS-fd-until-a-getfd-command-arriv.patch
# For bz#582874 - Guest hangs during restart after hot unplug then hot plug physical NIC card
Patch1462: kvm-Fix-segfault-after-device-assignment-hot-remove.patch
# For bz#590884 - bogus 'info pci' state when hot-added assigned device fails to initialize
Patch1463: kvm-pci-cleanly-backout-of-pci_qdev_init.patch
# For bz#593287 - Failed asserting during ide_dma_cancel
Patch1464: kvm-ide-Fix-ide_dma_cancel.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1465: kvm-spice-vmc-add-copyright.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1466: kvm-spice-vmc-remove-debug-prints-and-defines.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1467: kvm-spice-vmc-add-braces-to-single-line-if-s.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1468: kvm-spice-vmc-s-SpiceVirtualChannel-SpiceVMChannel-g.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1469: kvm-spice-vmc-s-spice_virtual_channel-spice_vmc-g.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1470: kvm-spice-vmc-all-variables-of-type-SpiceVMChannel-renam.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1471: kvm-spice-vmc-remove-meaningless-cast-of-void.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1472: kvm-spice-vmc-add-spice_vmc_ring_t-fix-write-function.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1473: kvm-spice-vmc-don-t-touch-guest_out_ring-on-unplug.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1474: kvm-spice-vmc-VirtIOSerialPort-vars-renamed-to-vserport.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1475: kvm-spice-vmc-add-nr-property.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1476: kvm-spice-vmc-s-SPICE_VM_CHANNEL-SPICE_VMC-g.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1477: kvm-spice-vmc-add-vmstate.-saves-active_interface.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1478: kvm-spice-vmc-rename-guest-device-name-to-com.redhat.spi.patch
# For bz#576488 - Spice: virtio serial based device for guest-spice client communication
Patch1479: kvm-spice-vmc-remove-unused-property-name.patch
# For bz#566785 - virt block layer must not keep guest's logical_block_size fixed
Patch1480: kvm-block-add-logical_block_size-property.patch
# For bz#591176 - migration fails since virtio-serial-bus is using uninitialized memory
Patch1481: kvm-virtio-serial-bus-fix-ports_map-allocation.patch
# For bz#569661 - RHEL6.0 requires backport of upstream cpu model support..
Patch1482: kvm-Move-cpu-model-config-file-to-agree-with-rpm-build-B.patch
# For bz#590922 - backport qemu-kvm-0.12.4 fixes to RHEL6
Patch1483: kvm-fix-undefined-shifts-by-32.patch
# For bz#590922 - backport qemu-kvm-0.12.4 fixes to RHEL6
Patch1484: kvm-qemu-char.c-drop-debug-printfs-from-qemu_chr_parse_c.patch
# For bz#590922 - backport qemu-kvm-0.12.4 fixes to RHEL6
Patch1485: kvm-Fix-corner-case-in-chardev-udp-parameter.patch
# For bz#590922 - backport qemu-kvm-0.12.4 fixes to RHEL6
Patch1486: kvm-pci-passthrough-zap-option-rom-scanning.patch
# For bz#590922 - backport qemu-kvm-0.12.4 fixes to RHEL6
Patch1487: kvm-UHCI-spurious-interrupt-fix.patch
# For bz#590922 - backport qemu-kvm-0.12.4 fixes to RHEL6
Patch1488: kvm-Fix-SIGFPE-for-vnc-display-of-width-height-1.patch
# For bz#589670 - spice: Ensure ring data is save/restored on migration
Patch1489: kvm-spice-vmc-remove-ringbuffer.patch
# For bz#589670 - spice: Ensure ring data is save/restored on migration
Patch1490: kvm-spice-vmc-add-dprintfs.patch
# For bz#585940 - qemu-kvm crashes on reboot when vhost is enabled
Patch1491: kvm-qemu-kvm-fix-crash-on-reboot-with-vhost-net.patch
# For bz#577106 - Abort/Segfault when creating qcow2 format image with 512b cluster size
Patch1492: kvm-qcow2-Fix-creation-of-large-images.patch
# For bz#569767 - Caps Lock the key's appearance  of guest is not synchronous as host's --view kvm with vnc
Patch1493: kvm-vnc-sync-lock-modifier-state-on-connect.patch
# For bz#589952 - QMP breaks when issuing any command with a backslash
Patch1494: kvm-json-lexer-Initialize-x-and-y.patch
# For bz#589952 - QMP breaks when issuing any command with a backslash
Patch1495: kvm-json-lexer-Handle-missing-escapes.patch
# For bz#589952 - QMP breaks when issuing any command with a backslash
Patch1496: kvm-qjson-Handle-f.patch
# For bz#589952 - QMP breaks when issuing any command with a backslash
Patch1497: kvm-json-lexer-Drop-buf.patch
# For bz#589952 - QMP breaks when issuing any command with a backslash
Patch1498: kvm-json-streamer-Don-t-use-qdict_put_obj.patch
# For bz#596119 - Possible corruption after block request merge
Patch1499: kvm-block-fix-sector-comparism-in-multiwrite_req_compare.patch
# For bz#596119 - Possible corruption after block request merge
Patch1500: kvm-block-Fix-multiwrite-with-overlapping-requests.patch
# For bz#595495 - Fail to hotplug pci device to guest
Patch1501: kvm-device-assignment-use-stdint-types.patch
# For bz#595495 - Fail to hotplug pci device to guest
Patch1502: kvm-device-assignment-Don-t-use-libpci.patch
# For bz#595495 - Fail to hotplug pci device to guest
Patch1503: kvm-device-assignment-add-config-fd-qdev-property.patch
# For bz#595301 - QEMU terminates without warning with virtio-net and SMP enabled
Patch1504: kvm-qemu-address-todo-comment-in-exec.c.patch
# For bz#595813 - virtio-blk doesn't handle barriers correctly
Patch1505: kvm-virtio-blk-fix-barrier-support.patch
# changes for make-release with no resulting changes on binary
Patch1506: kvm-make-release-misc-fixes.patch
# For bz#595287 - virtio net/vhost net speed enhancements from upstream kernel
Patch1507: kvm-virtio-utilize-PUBLISH_USED_IDX-feature.patch
# For bz#595263 - virtio net lacks upstream fixes as of may 24
Patch1508: kvm-virtio-invoke-set_features-on-load.patch
# For bz#595263 - virtio net lacks upstream fixes as of may 24
Patch1509: kvm-virtio-net-return-with-value-in-void-function.patch
# For bz#585940 - qemu-kvm crashes on reboot when vhost is enabled
Patch1510: kvm-vhost-net-fix-reversed-logic-in-mask-notifiers.patch
# For bz#595130 - Disable hpet by default
Patch1511: kvm-hpet-Disable-for-Red-Hat-Enterprise-Linux.patch
# For bz#598896 - migration breaks networking with vhost-net
Patch1513: kvm-virtio-net-stop-vhost-backend-on-vmstop.patch
# For bz#598896 - migration breaks networking with vhost-net
Patch1514: kvm-msix-fix-msix_set-unset_mask_notifier.patch
# For bz#585310 - qemu-kvm does not exit when device assignment fails due to IRQ sharing
Patch1515: kvm-device-assignment-fix-failure-to-exit-on-shared-IRQ.patch
# For bz#588719 - Fix monitor command documentation
Patch1516: kvm-doc-Fix-host-forwarding-monitor-command-documentatio.patch
# For bz#588719 - Fix monitor command documentation
Patch1517: kvm-doc-Fix-acl-monitor-command-documentation.patch
# For bz#588719 - Fix monitor command documentation
Patch1518: kvm-doc-Heading-for-monitor-command-cpu-got-lost-restore.patch
# For bz#588719 - Fix monitor command documentation
Patch1519: kvm-doc-Clean-up-monitor-command-function-index.patch
# For bz#593769 - "info cpus" doesn't show halted state
Patch1520: kvm-fix-info-cpus-halted-state-reporting.patch
# For bz#559618 - QMP: Fix 'quit' to return success before exiting
Patch1521: kvm-sysemu-Export-no_shutdown.patch
# For bz#559618 - QMP: Fix 'quit' to return success before exiting
Patch1522: kvm-Monitor-Return-before-exiting-with-quit.patch
# For bz#566291 - QMP: Support vendor extensions
Patch1523: kvm-QMP-Add-Downstream-extension-of-QMP-to-spec.patch
# For bz#580365 - QMP: pci_add/pci_del conversion should be reverted
Patch1524: kvm-Revert-PCI-Convert-pci_device_hot_add-to-QObject.patch
# For bz#580365 - QMP: pci_add/pci_del conversion should be reverted
Patch1525: kvm-Revert-monitor-Convert-do_pci_device_hot_remove-to-Q.patch
# For bz#565609 - Unable to use werror/rerror with  -drive syntax using if=none
# For bz#593256 - Unable to set readonly flag for floppy disks
Patch1526: kvm-drive-allow-rerror-werror-and-readonly-for-if-none.patch
# For bz#596093 - 16bit integer qdev properties are not parsed correctly.
Patch1527: kvm-qdev-properties-Fix-u-intXX-parsers.patch
# For bz#590070 - QEMU misses DESKTOP-RESIZE event if it is triggered during client connection initialization
Patch1528: kvm-vnc-factor-out-vnc_desktop_resize.patch
# For bz#590070 - QEMU misses DESKTOP-RESIZE event if it is triggered during client connection initialization
Patch1529: kvm-vnc-send-desktopresize-event-as-reply-to-set-encodin.patch
# For bz#590070 - QEMU misses DESKTOP-RESIZE event if it is triggered during client connection initialization
Patch1530: kvm-vnc-keep-track-of-client-desktop-size.patch
# For bz#590070 - QEMU misses DESKTOP-RESIZE event if it is triggered during client connection initialization
Patch1531: kvm-vnc-don-t-send-invalid-screen-updates.patch
# For bz#590070 - QEMU misses DESKTOP-RESIZE event if it is triggered during client connection initialization
Patch1532: kvm-vnc-move-size-changed-check-into-the-vnc_desktop_res.patch
# For bz#591759 - Segmentation fault when using vnc to view guest without vga card
Patch1533: kvm-check-for-active_console-before-using-it.patch
# For bz#586349 - BLOCK_IO_ERROR event does not provide the errno that caused it.
Patch1534: kvm-Monitor-Make-RFQDN_REDHAT-public.patch
# For bz#586349 - BLOCK_IO_ERROR event does not provide the errno that caused it.
Patch1535: kvm-QMP-Add-error-reason-to-BLOCK_IO_ERROR-event.patch
# For bz#591494 - Virtio: Transfer file caused guest in same vlan abnormally quit
Patch1536: kvm-virtio-net-truncating-packet.patch
# For bz#600203 - vhost net new userspace on old kernel: 95: falling back on userspace virtio
Patch1537: kvm-vhost-net-check-PUBLISH_USED-in-backend.patch
# For bz#596315 - device assignment truncates MSIX table size
Patch1538: kvm-device-assignment-don-t-truncate-MSIX-capabilities-t.patch
# For bz#561433 - Segfault when keyboard is removed
Patch1539: kvm-If-a-USB-keyboard-is-unplugged-the-keyboard-eventhan.patch
# For bz#599460 - virtio nic is hotpluged when hotplug rtl8139 nic to guest
Patch1540: kvm-net-Fix-hotplug-with-pci_add.patch
# For bz#593758 - qemu fails to start with -cdrom /dev/sr0 if no media inserted
Patch1541: kvm-raw-posix-Detect-CDROM-via-ioctl-on-linux.patch
# For bz#593758 - qemu fails to start with -cdrom /dev/sr0 if no media inserted
Patch1542: kvm-block-Remove-special-case-for-vvfat.patch
# For bz#593758 - qemu fails to start with -cdrom /dev/sr0 if no media inserted
Patch1543: kvm-block-Make-find_image_format-return-raw-BlockDriver-.patch
# For bz#593758 - qemu fails to start with -cdrom /dev/sr0 if no media inserted
Patch1544: kvm-block-Add-missing-bdrv_delete-for-SG_IO-BlockDriver-.patch
# For bz#593758 - qemu fails to start with -cdrom /dev/sr0 if no media inserted
Patch1545: kvm-block-Assume-raw-for-drives-without-media.patch
# For bz#598407 - qcow2 corruption bug in refcount table growth
Patch1546: kvm-qcow2-Fix-corruption-after-refblock-allocation.patch
# For bz#598507 - Backport qcow2 error path fixes
Patch1547: kvm-qcow2-Fix-corruption-after-error-in-update_refcount.patch
# For bz#598507 - Backport qcow2 error path fixes
Patch1548: kvm-qcow2-Allow-qcow2_get_cluster_offset-to-return-error.patch
# For bz#598507 - Backport qcow2 error path fixes
Patch1549: kvm-qcow2-Change-l2_load-to-return-0-errno.patch
# For bz#598507 - Backport qcow2 error path fixes
Patch1550: kvm-qcow2-Return-right-error-code-in-write_refcount_bloc.patch
# For bz#598507 - Backport qcow2 error path fixes
Patch1551: kvm-qcow2-Clear-L2-table-cache-after-write-error.patch
# For bz#598507 - Backport qcow2 error path fixes
Patch1552: kvm-qcow2-Fix-error-handling-in-l2_allocate.patch
# For bz#598507 - Backport qcow2 error path fixes
Patch1553: kvm-qcow2-Restore-L1-entry-on-l2_allocate-failure.patch
# For bz#598507 - Backport qcow2 error path fixes
Patch1554: kvm-qcow2-Allow-get_refcount-to-return-errors.patch
# For bz#598507 - Backport qcow2 error path fixes
Patch1555: kvm-qcow2-Avoid-shadowing-variable-in-alloc_clusters_nor.patch
# For bz#598507 - Backport qcow2 error path fixes
Patch1556: kvm-qcow2-Allow-alloc_clusters_noref-to-return-errors.patch
# For bz#598507 - Backport qcow2 error path fixes
Patch1557: kvm-qcow2-Return-real-error-code-in-load_refcount_block.patch
Patch1558: kvm-make-release-make-mtime-owner-group-consistent.patch
# For bz#602724 - VNC disconnect segfault on KVM video consoles
Patch1559: kvm-fix-vnc-memory-corruption-with-width-1400.patch
# For bz#599460 - virtio nic is hotpluged when hotplug rtl8139 nic to guest
Patch1560: kvm-net-Fix-VM-start-with-net-none.patch
# For bz#602590 - Disable pci_add, pci_del, drive_add
Patch1561: kvm-monitor-Remove-pci_add-command-for-Red-Hat-Enterpris.patch
# For bz#602590 - Disable pci_add, pci_del, drive_add
Patch1562: kvm-monitor-Remove-pci_del-command-for-Red-Hat-Enterpris.patch
# For bz#602590 - Disable pci_add, pci_del, drive_add
Patch1563: kvm-monitor-Remove-drive_add-command-for-Red-Hat-Enterpr.patch
# For bz#602026 - Cannot change cdrom by "change device filename [format] " in (qemu) command line
Patch1564: kvm-block-read-only-open-cdrom-as-read-only-when-using-m.patch
# For bz#598022 - Hot-added device is not visible in guest after live-migration.
Patch1565: kvm-acpi_piix4-save-gpe-and-pci-hotplug-slot-status.patch
# For bz#596014 - hot add virtio-blk-pci via device_add lead to virtio network lost
Patch1566: kvm-Don-t-check-for-bus-master-for-old-guests.patch
# For bz#597147 - libvirt: kvm disk error after first stage install of Win2K or WinXP
Patch1567: kvm-Make-IDE-drives-defined-with-device-visible-to-cmos_.patch
# For bz#597147 - libvirt: kvm disk error after first stage install of Win2K or WinXP
Patch1568: kvm-Make-geometry-of-IDE-drives-defined-with-device-visi.patch
# For bz#602417 - Enable VIRTIO_RING_F_PUBLISHED bit for all virtio devices
Patch1569: kvm-virtio-Enable-the-PUBLISH_USED-feature-by-default-fo.patch
# For bz#595647 - Windows guest with qxl driver can't get into S3 state
Patch1570: kvm-do-not-enter-vcpu-again-if-it-was-stopped-during-IO.patch
# For bz#581789 - Cannot eject cd-rom when configured to host cd-rom
Patch1571: kvm-monitor-allow-device-to-be-ejected-if-no-disk-is-ins.patch
# For bz#596609 - Live migration failed when migration during boot
Patch1572: kvm-New-slots-need-dirty-tracking-enabled-when-migrating.patch
# For bz#596274 - QMP: netdev_del sometimes fails claiming the device is in use
Patch1573: kvm-Make-netdev_del-delete-the-netdev-even-when-it-s-in-.patch
# For bz#605359 - Fix MSIX regression from bz595495
Patch1574: kvm-device-assignment-msi-PBA-is-long.patch
# For bz#604210 - Segmentation fault when check  preallocated qcow2 image on lvm.
Patch1575: kvm-qcow2-Fix-qemu-img-check-segfault-on-corrupted-image.patch
# For bz#604210 - Segmentation fault when check  preallocated qcow2 image on lvm.
Patch1576: kvm-qcow2-Don-t-try-to-check-tables-that-couldn-t-be-loa.patch
# For bz#604210 - Segmentation fault when check  preallocated qcow2 image on lvm.
Patch1577: kvm-qcow2-Fix-error-handling-during-metadata-preallocati.patch
# For bz#607200 - qcow2 image corruption when using cache=writeback
Patch1578: kvm-block-Add-bdrv_-p-write_sync.patch
# For bz#607200 - qcow2 image corruption when using cache=writeback
Patch1579: kvm-qcow2-Use-bdrv_-p-write_sync-for-metadata-writes.patch
# For bz#607263 - Unable to launch QEMU with -M pc-0.12 and  virtio serial
Patch1580: kvm-virtio-serial-Fix-compat-property-name.patch
# For bz#606733 - Unable to set the driftfix parameter
Patch1581: kvm-rtc-Remove-TARGET_I386-from-qemu-config.c-enables-dr.patch
# For bz#585009 - QMP: input needs trailing  char
Patch1582: kvm-add-some-tests-for-invalid-JSON.patch
# For bz#585009 - QMP: input needs trailing  char
Patch1583: kvm-implement-optional-lookahead-in-json-lexer.patch
# For bz#585009 - QMP: input needs trailing  char
Patch1584: kvm-remove-unnecessary-lookaheads.patch
# For bz#605704 - qemu-kvm: set per-machine-type smbios strings
Patch1585: kvm-per-machine-type-smbios-Type-1-smbios-values.patch
# For bz#607688 - Excessive lseek() causes severe performance issues with vm disk images over NFS
Patch1586: kvm-raw-posix-Use-pread-pwrite-instead-of-lseek-read-wri.patch
# For bz#607688 - Excessive lseek() causes severe performance issues with vm disk images over NFS
Patch1587: kvm-block-Cache-total_sectors-to-reduce-bdrv_getlength-c.patch
# For bz#599122 - Unable to launch QEMU with a guest disk filename containing a ':'
Patch1588: kvm-block-allow-filenames-with-colons-again-for-host-dev.patch
# For bz#606084 - Allow control of kvm cpuid option via -cpu flag
Patch1589: kvm-Add-KVM-paravirt-cpuid-leaf.patch
# For bz#605638 - Remove unsupported monitor commands from qemu-kvm
Patch1590: kvm-Remove-usage-of-CONFIG_RED_HAT_DISABLED.patch
# For bz#605638 - Remove unsupported monitor commands from qemu-kvm
Patch1591: kvm-monitor-Remove-host_net_add-remove-for-Red-Hat-Enter.patch
# For bz#605638 - Remove unsupported monitor commands from qemu-kvm
Patch1592: kvm-monitor-Remove-usb_add-del-commands-for-Red-Hat-Ente.patch
# For bz#607244 - virtio-blk doesn't load list of pending requests correctly
Patch1593: kvm-virtio-blk-fix-the-list-operation-in-virtio_blk_load.patch
# For bz#596279 - QMP: does not report the real cause of PCI device assignment failure
Patch1594: kvm-QError-Introduce-QERR_DEVICE_INIT_FAILED_2.patch
# For bz#596279 - QMP: does not report the real cause of PCI device assignment failure
Patch1595: kvm-dev-assignment-Report-IRQ-assign-errors-in-QMP.patch
# For bz#603851 - QMP: Can't reuse same 'id' when netdev_add fails
Patch1596: kvm-net-delete-QemuOpts-when-net_client_init-fails.patch
# For bz#587382 - QMP: balloon command may not report an error
Patch1597: kvm-QMP-Fix-error-reporting-in-the-async-API.patch
# For bz#580648 - QMP: Bad package version in greeting message
Patch1598: kvm-QMP-Remove-leading-whitespace-in-package.patch
# For bz#601540 - qemu requires ability to verify location of cpu model definition file..
Patch1599: kvm-Add-optional-dump-of-default-config-file-paths-v2-BZ.patch
# For bz#597198 - qxl: 16bpp vga mode is broken.
Patch1600: kvm-qxl-drop-check-for-depths-32.patch
# For bz#597198 - qxl: 16bpp vga mode is broken.
# For bz#600205 - Live migration cause qemu-kvm Segmentation fault (core dumped)by using "-vga std"
Patch1601: kvm-spice-handle-16-bit-color-depth.patch
# For bz#597968 - Should not allow one physical NIC card to be assigned to one guest for many times
Patch1602: kvm-device-assignment-Don-t-deassign-when-the-assignment.patch
# For bz#566785 - virt block layer must not keep guest's logical_block_size fixed
Patch1603: kvm-block-fix-physical_block_size-calculation.patch
# For bz#601517 - x2apic needs to be present in all new Intel cpu models..
Patch1604: kvm-Add-x2apic-to-cpuid-feature-set-for-new-Intel-models.patch
# For bz#570174 - Restoring a qemu guest from a saved state file using -incoming sometimes fails and hangs
Patch1605: kvm-Exit-if-incoming-migration-fails.patch
# For bz#570174 - Restoring a qemu guest from a saved state file using -incoming sometimes fails and hangs
Patch1606: kvm-Factorize-common-migration-incoming-code.patch
# For bz#605361 - 82576 physical function device assignment doesn't work with win7
Patch1607: kvm-device-assignment-be-more-selective-in-interrupt-dis.patch
# For bz#572043 - Guest gets segfault when do multiple device hot-plug and hot-unplug
Patch1608: kvm-device-assignment-Avoid-munmapping-the-real-MSIX-are.patch
# For bz#572043 - Guest gets segfault when do multiple device hot-plug and hot-unplug
Patch1609: kvm-device-assignment-Cleanup-on-exit.patch
# For bz#582262 - QMP: Missing commands doc
Patch1610: kvm-doc-Update-monitor-info-subcommands.patch
# For bz#582262 - QMP: Missing commands doc
Patch1611: kvm-Fix-typo-in-balloon-help.patch
# For bz#582262 - QMP: Missing commands doc
Patch1612: kvm-monitor-Reorder-info-documentation.patch
# For bz#582262 - QMP: Missing commands doc
Patch1613: kvm-QMP-Introduce-commands-documentation.patch
# For bz#582262 - QMP: Missing commands doc
Patch1614: kvm-QMP-Sync-documentation-with-RHEL6-only-changes.patch
# For bz#582262 - QMP: Missing commands doc
Patch1615: kvm-Monitor-Drop-QMP-documentation-from-code.patch
# For bz#582262 - QMP: Missing commands doc
Patch1616: kvm-hxtool-Fix-line-number-reporting-on-SQMP-EQMP-errors.patch
# For bz#581963 - QMP: missing drive_add command in JSON mode
Patch1617: kvm-monitor-New-command-__com.redhat_drive_add.patch
# For bz#611229 - -rtc cmdline changes
Patch1618: kvm-Fix-driftfix-option.patch
Patch1619: kvm-make-release-fix-mtime-on-rhel6-beta.patch
# For bz#598836 - RHEL 6.0 RTC Alarm unusable in vm
Patch1620: kvm-make-rtc-alatm-work.patch
# For bz#612164 - [kvm] qemu image check returns cluster errors when using virtIO block (thinly provisioned) during e_no_space events (along with EIO errors)
Patch1621: kvm-qemu-img-check-Distinguish-different-kinds-of-errors.patch
# For bz#612164 - [kvm] qemu image check returns cluster errors when using virtIO block (thinly provisioned) during e_no_space events (along with EIO errors)
Patch1622: kvm-qcow2-vdi-Change-check-to-distinguish-error-cases.patch
# For bz#612481 - Enable migration subsections
Patch1623: kvm-Revert-ide-save-restore-pio-atapi-cmd-transfer-field.patch
# For bz#612481 - Enable migration subsections
Patch1624: kvm-vmstate-add-subsections-code.patch
# For bz#612481 - Enable migration subsections
Patch1625: kvm-ide-fix-migration-in-the-middle-of-pio-operation.patch
# For bz#612481 - Enable migration subsections
Patch1626: kvm-ide-fix-migration-in-the-middle-of-a-bmdma-transfer.patch
# For bz#612481 - Enable migration subsections
Patch1627: kvm-Initial-documentation-for-migration-Signed-off-by-Ju.patch
# For bz#607263 - Remove -M pc-0.12 support
Patch1628: kvm-Disable-non-rhel-machine-types-pc-0.12-pc-0.11-pc-0..patch
# For bz#610805 - Move CPU definitions to /usr/share/...
Patch1629: kvm-Move-CPU-definitions-to-usr-share-.-BZ-610805.patch
# For bz#609261 - Exec outgoing migration is too slow
Patch1630: kvm-QEMUFileBuffered-indicate-that-we-re-ready-when-the-.patch
# For bz#611715 - qemu-kvm gets no responsive  when do  hot-unplug pass-through device
Patch1631: kvm-device-assignment-Better-fd-tracking.patch
# For bz#613884 - x2apic needs to be present in all new AMD cpu models..
Patch1634: kvm-Add-x2apic-to-cpuid-feature-set-for-new-AMD-models.-.patch
# For bz#602209 - Core dumped during Guest installation
Patch1635: kvm-block-Fix-early-failure-in-multiwrite.patch
# For bz#602209 - Core dumped during Guest installation
Patch1636: kvm-block-Handle-multiwrite-errors-only-when-all-request.patch
# For bz#584372 - Fails to detect errors when using exec: based migration
Patch1637: kvm-migration-respect-exit-status-with-exec.patch
# For bz#584372 - Fails to detect errors when using exec: based migration
Patch1638: kvm-set-proper-migration-status-on-write-error-v3.patch
# For bz#614377 - Windows 7 requires re-activation when migrated from RHEL5 to RHEL6
Patch1639: kvm-Set-SMBIOS-vendor-to-QEMU-for-RHEL5-machine-types.patch
# For bz#611797 - qemu does not call unlink() on temp files in snapshot mode
Patch1640: kvm-Don-t-reset-bs-is_temporary-in-bdrv_open_common.patch
# For bz#614537 - Skype crashes on VM.
Patch1641: kvm-Change-default-CPU-model-qemu64-to-model-6.patch
# For bz#614537 - Skype crashes on VM.
Patch1642: kvm-set-model-6-on-Intel-CPUs-on-cpu-x86_64.conf.patch
# For bz#615228 - oom in vhost_dev_start
Patch1643: kvm-vhost-fix-miration-during-device-start.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1644: kvm-ram_blocks-Convert-to-a-QLIST.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1645: kvm-Remove-uses-of-ram.last_offset-aka-last_ram_offset.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1646: kvm-pc-Allocate-all-ram-in-a-single-qemu_ram_alloc.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1647: kvm-qdev-Add-a-get_dev_path-function-to-BusInfo.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1648: kvm-pci-Implement-BusInfo.get_dev_path.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1649: kvm-savevm-Add-DeviceState-param.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1650: kvm-savevm-Make-use-of-DeviceState.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1651: kvm-eepro100-Add-a-dev-field-to-eeprom-new-free-function.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1652: kvm-virtio-net-Incorporate-a-DeviceState-pointer-and-let.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1653: kvm-qemu_ram_alloc-Add-DeviceState-and-name-parameters.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1654: kvm-ramblocks-Make-use-of-DeviceState-pointer-and-BusInf.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1655: kvm-savevm-Migrate-RAM-based-on-name-offset.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1656: kvm-savevm-Use-RAM-blocks-for-basis-of-migration.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1657: kvm-savevm-Create-a-new-continue-flag-to-avoid-resending.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1658: kvm-qemu_ram_free-Implement-it.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1659: kvm-pci-Free-the-space-allocated-for-the-option-rom-on-r.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1660: kvm-ramblocks-No-more-being-lazy-about-duplicate-names.patch
# For bz#616525 - savevm needs to reset block info on each new save
Patch1661: kvm-savevm-Reset-last-block-info-at-beginning-of-each-sa.patch
# For bz#615152 - rhel 6 performance worse than rhel5.6 when committing 1G  changes recorded in  snapshot in its base image.
Patch1662: kvm-block-Change-bdrv_commit-to-handle-multiple-sectors-.patch
# For bz#616501 - publish used ABI incompatible with future guests
Patch1663: kvm-Revert-virtio-Enable-the-PUBLISH_USED-feature-by-def.patch
# For bz#616501 - publish used ABI incompatible with future guests
Patch1664: kvm-Revert-vhost-net-check-PUBLISH_USED-in-backend.patch
# For bz#616501 - publish used ABI incompatible with future guests
Patch1665: kvm-Revert-virtio-utilize-PUBLISH_USED_IDX-feature.patch
# For bz#596328 - [RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.
Patch1666: kvm-savevm-Fix-memory-leak-of-compat-struct.patch
# For bz#580010 - migration failed after pci_add and pci_del a virtio storage device
Patch1667: kvm-virtio-blk-Create-exit-function-to-unregister-savevm.patch
# For bz#596232 - Update docs to exclude unsupported options
Patch1668: kvm-Documentation-Add-a-warning-message-to-qemu-kvm-help.patch
# For bz#617534 - Disable SCSI and usb-storage
Patch1669: kvm-Disable-SCSI.patch
# For bz#612074 - core dumped while live migration with spice
Patch1670: kvm-spice-don-t-force-fullscreen-redraw-on-display-resiz.patch
# For bz#616188 - KVM_GET_SUPPORTED_CPUID doesn't return all host cpuid flags..
Patch1671: kvm-KVM_GET_SUPPORTED_CPUID-doesn-t-return-all-host-cpui.patch
# For bz#612696 - virsh attach-device crash kvm guest.
Patch1672: kvm-Do-not-try-loading-option-ROM-for-hotplug-PCI-device.patch
# For bz#591494 - Virtio: Transfer file caused guest in same vlan abnormally quit
Patch1673: kvm-virtio-net-correct-packet-length-checks.patch
# For bz#617414 - avoid canceling in flight ide dma
Patch1674: kvm-avoid-canceling-ide-dma-rediff.patch
# For bz#617463 - Coredump occorred when enable qxl
Patch1675: kvm-spice-Rename-conflicting-ramblock.patch
# For bz#617271 - RHEL6 qemu-kvm guest gets partitioned at sector 63
Patch1676: kvm-block-default-to-0-minimal-optimal-I-O-size.patch
# For bz#581555 - race between qemu monitor "cont" and incoming migration can cause failed restore/migration
Patch1677: kvm-migration-Accept-cont-only-after-successful-incoming.patch
# For bz#617085 - core dumped when add netdev to VM with vhost on
Patch1678: kvm-vhost_dev_unassign_memory-don-t-assert-if-removing-f.patch
# For bz#615214 - [VT-d] Booting RHEL6 guest with Intel 82541PI NIC assigned by libvirt cause qemu crash
Patch1679: kvm-device-assignment-Use-PCI-I-O-port-sysfs-resource-fi.patch
# For bz#558256 - rhel6 disk not detected first time in install
Patch1680: kvm-block-Change-bdrv_eject-not-to-drop-the-image.patch
# For bz#618788 - device-assignment hangs with kvm_run: Bad address
Patch1681: kvm-device-assignment-Leave-option-ROM-space-RW-KVM-does.patch
# For bz#616890 - "qemu-img convert" fails on block device
Patch1682: kvm-block-Fix-bdrv_has_zero_init.patch
# For bz#619414 - CVE-2010-2784 qemu: insufficient constraints checking in exec.c:subpage_register() [rhel-6.0]
Patch1683: kvm-Fix-segfault-in-mmio-subpage-handling-code.patch
# For bz#618601 - We need to reopen images after migration
Patch1684: kvm-Migration-reopen-block-devices-files.patch
# For bz#613892 - [SR-IOV]VF device can not start on 32bit Windows2008 SP2
# For bz#618332 - CPUID_EXT_POPCNT enabled in qemu64 and qemu32 built-in models.
Patch1685: kvm-Correct-cpuid-flags-and-model-fields-V2.patch
# For bz#618168 - Qemu-kvm in the src host core dump when do migration by using spice
Patch1686: kvm-Fix-migration-with-spice-enabled.patch
# For bz#607244 - virtio-blk doesn't load list of pending requests correctly
Patch1687: kvm-virtio-Factor-virtqueue_map_sg-out.patch
# For bz#607244 - virtio-blk doesn't load list of pending requests correctly
Patch1688: kvm-virtio-blk-Fix-migration-of-queued-requests.patch
# For bz#607611 - pci hotplug of e1000, rtl8139 nic device fails for all guests.
Patch1689: kvm-qdev-Reset-hotplugged-devices.patch
# For bz#621161 - qemu-kvm crashes with I/O Possible message
Patch1690: kvm-Block-I-O-signals-in-audio-helper-threads.patch
# For bz#622356 - Live migration failed during reboot due to vhost
Patch1691: kvm-vhost-Fix-size-of-dirty-log-sync-on-resize.patch
# For bz#624666 - qemu-img re-base broken on RHEL6
Patch1692: kvm-qemu-img-rebase-Open-new-backing-file-read-only.patch
# For bz#623903 - query-balloon commmand didn't return on pasued guest cause virt-manger hang
Patch1693: kvm-disable-guest-provided-stats-on-info-ballon-monitor-.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: SDL-devel zlib-devel which texi2html gnutls-devel cyrus-sasl-devel
BuildRequires: rsync dev86 iasl
BuildRequires: pciutils-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: ncurses-devel
BuildRequires: libaio-devel

# require spice-server API changes from bz#571286
BuildRequires: spice-server-devel >= 0.4.2-10.el6

Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service /sbin/chkconfig
Requires(postun): /sbin/service

Provides: kvm = 85
Obsoletes: kvm < 85
Requires: vgabios
Requires: vgabios-qxl
Requires: seabios
Requires: /usr/share/gpxe/e1000-0x100e.rom
Requires: /usr/share/gpxe/rtl8029.rom
Requires: /usr/share/gpxe/pcnet32.rom
Requires: /usr/share/gpxe/rtl8139.rom
Requires: /usr/share/gpxe/virtio-net.rom

# We don't provide vvfat anymore, that is used by older VDSM versions.
Conflicts: vdsm < 4.5

Requires: qemu-img = %{epoch}:%{version}-%{release}

%define qemudocdir %{_docdir}/%{name}-%{version}
%define cpumodeldir %{_datadir}/%{name}/cpu-model

%description
KVM (for Kernel-based Virtual Machine) is a full virtualization solution
for Linux on x86 hardware.

Using KVM, one can run multiple virtual machines running unmodified Linux
or Windows images. Each virtual machine has private virtualized hardware:
a network card, disk, graphics adapter, etc.

%package -n qemu-img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools
%description -n qemu-img
This package provides a command line tool for manipulating disk images

%package tools
Summary: KVM debugging and diagnostics tools
Group: Development/Tools

%description tools
This package contains some diagnostics and debugging tools for KVM,
such as kvm_stat.

%prep
%setup -q -n qemu-kvm-%{version}


%patch1000 -p1
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1
%patch1007 -p1
%patch1008 -p1
%patch1009 -p1
%patch1010 -p1
%patch1011 -p1
%patch1012 -p1
%patch1013 -p1
%patch1014 -p1
%patch1015 -p1
%patch1016 -p1
%patch1017 -p1
%patch1018 -p1
%patch1019 -p1
%patch1020 -p1
%patch1021 -p1
%patch1022 -p1
%patch1023 -p1
%patch1024 -p1
%patch1025 -p1
%patch1026 -p1
%patch1027 -p1
%patch1028 -p1
%patch1029 -p1
%patch1030 -p1
%patch1031 -p1
%patch1032 -p1
%patch1033 -p1
%patch1034 -p1
%patch1035 -p1
%patch1036 -p1
%patch1037 -p1
%patch1038 -p1
%patch1039 -p1
%patch1040 -p1
%patch1041 -p1
%patch1042 -p1
%patch1043 -p1
%patch1044 -p1
%patch1045 -p1
%patch1046 -p1
%patch1047 -p1
%patch1048 -p1
%patch1049 -p1
%patch1050 -p1
%patch1051 -p1
%patch1052 -p1
%patch1053 -p1
%patch1054 -p1
%patch1055 -p1
%patch1056 -p1
%patch1057 -p1
%patch1058 -p1
%patch1059 -p1
%patch1060 -p1
%patch1061 -p1
%patch1062 -p1
%patch1063 -p1
%patch1064 -p1
%patch1065 -p1
%patch1066 -p1
%patch1067 -p1
%patch1068 -p1
%patch1069 -p1
%patch1070 -p1
%patch1071 -p1
%patch1072 -p1
%patch1073 -p1
%patch1074 -p1
%patch1075 -p1
%patch1076 -p1
%patch1077 -p1
%patch1078 -p1
%patch1079 -p1
%patch1080 -p1
%patch1081 -p1
%patch1082 -p1
%patch1083 -p1
%patch1084 -p1
%patch1085 -p1
%patch1086 -p1
%patch1087 -p1
%patch1088 -p1
%patch1089 -p1
%patch1090 -p1
%patch1091 -p1
%patch1092 -p1
%patch1093 -p1
%patch1094 -p1
%patch1095 -p1
%patch1096 -p1
%patch1097 -p1
%patch1098 -p1
%patch1099 -p1
%patch1100 -p1
%patch1101 -p1
%patch1102 -p1
%patch1103 -p1
%patch1104 -p1
%patch1105 -p1
%patch1106 -p1
%patch1107 -p1
%patch1108 -p1
%patch1109 -p1
%patch1110 -p1
%patch1111 -p1
%patch1112 -p1
%patch1113 -p1
%patch1114 -p1
%patch1115 -p1
%patch1116 -p1
%patch1117 -p1
%patch1118 -p1
%patch1119 -p1
%patch1120 -p1
%patch1121 -p1
%patch1122 -p1
%patch1123 -p1
%patch1124 -p1
%patch1125 -p1
%patch1126 -p1
%patch1127 -p1
%patch1128 -p1
%patch1129 -p1
%patch1130 -p1
%patch1131 -p1
%patch1132 -p1
%patch1133 -p1
%patch1134 -p1
%patch1135 -p1
%patch1136 -p1
%patch1137 -p1
%patch1138 -p1
%patch1139 -p1
%patch1140 -p1
%patch1141 -p1
%patch1142 -p1
%patch1143 -p1
%patch1144 -p1
%patch1145 -p1
%patch1146 -p1
%patch1147 -p1
%patch1148 -p1
%patch1149 -p1
%patch1150 -p1
%patch1151 -p1
%patch1152 -p1
%patch1153 -p1
%patch1154 -p1
%patch1155 -p1
%patch1156 -p1
%patch1157 -p1
%patch1158 -p1
%patch1159 -p1
%patch1160 -p1
%patch1161 -p1
%patch1162 -p1
%patch1163 -p1
%patch1164 -p1
%patch1165 -p1
%patch1166 -p1
%patch1167 -p1
%patch1168 -p1
%patch1169 -p1
%patch1170 -p1
%patch1171 -p1
%patch1172 -p1
%patch1173 -p1
%patch1174 -p1
%patch1175 -p1
%patch1176 -p1
%patch1177 -p1
%patch1178 -p1
%patch1179 -p1
%patch1180 -p1
%patch1181 -p1
%patch1182 -p1
%patch1183 -p1
%patch1184 -p1
%patch1185 -p1
%patch1186 -p1
%patch1187 -p1
%patch1188 -p1
%patch1189 -p1
%patch1190 -p1
%patch1191 -p1
%patch1192 -p1
%patch1193 -p1
%patch1194 -p1
%patch1195 -p1
%patch1196 -p1
%patch1197 -p1
%patch1198 -p1
%patch1199 -p1
%patch1200 -p1
%patch1201 -p1
%patch1202 -p1
%patch1203 -p1
%patch1204 -p1
%patch1205 -p1
%patch1206 -p1
%patch1207 -p1
%patch1208 -p1
%patch1209 -p1
%patch1210 -p1
%patch1211 -p1
%patch1212 -p1
%patch1213 -p1
%patch1214 -p1
%patch1215 -p1
%patch1216 -p1
%patch1217 -p1
%patch1218 -p1
%patch1219 -p1
%patch1220 -p1
%patch1221 -p1
%patch1222 -p1
%patch1223 -p1
%patch1224 -p1
%patch1225 -p1
%patch1226 -p1
%patch1227 -p1
%patch1228 -p1
%patch1229 -p1
%patch1230 -p1
%patch1231 -p1
%patch1232 -p1
%patch1233 -p1
%patch1234 -p1
%patch1235 -p1
%patch1236 -p1
%patch1237 -p1
%patch1238 -p1
%patch1239 -p1
%patch1240 -p1
%patch1241 -p1
%patch1242 -p1
%patch1243 -p1
%patch1244 -p1
%patch1245 -p1
%patch1246 -p1
%patch1247 -p1
%patch1248 -p1
%patch1249 -p1
%patch1250 -p1
%patch1251 -p1
%patch1252 -p1
%patch1253 -p1
%patch1254 -p1
%patch1255 -p1
%patch1256 -p1
%patch1257 -p1
%patch1258 -p1
%patch1259 -p1
%patch1260 -p1
%patch1261 -p1
%patch1262 -p1
%patch1263 -p1
%patch1264 -p1
%patch1265 -p1
%patch1266 -p1
%patch1267 -p1
%patch1268 -p1
%patch1269 -p1
%patch1270 -p1
%patch1271 -p1
%patch1272 -p1
%patch1273 -p1
%patch1274 -p1
%patch1275 -p1
%patch1276 -p1
%patch1277 -p1
%patch1278 -p1
%patch1279 -p1
%patch1280 -p1
%patch1281 -p1
%patch1282 -p1
%patch1283 -p1
%patch1284 -p1
%patch1285 -p1
%patch1286 -p1
%patch1287 -p1
%patch1288 -p1
%patch1289 -p1
%patch1290 -p1
%patch1291 -p1
%patch1292 -p1
%patch1293 -p1
%patch1294 -p1
%patch1295 -p1
%patch1296 -p1
%patch1297 -p1
%patch1298 -p1
%patch1299 -p1
%patch1300 -p1
%patch1301 -p1
%patch1302 -p1
%patch1303 -p1
%patch1304 -p1
%patch1305 -p1
%patch1306 -p1
%patch1307 -p1
%patch1308 -p1
%patch1309 -p1
%patch1310 -p1
%patch1311 -p1
%patch1312 -p1
%patch1313 -p1
%patch1314 -p1
%patch1315 -p1
%patch1316 -p1
%patch1317 -p1
%patch1318 -p1
%patch1319 -p1
%patch1320 -p1
%patch1321 -p1
%patch1322 -p1
%patch1323 -p1
%patch1324 -p1
%patch1325 -p1
%patch1326 -p1
%patch1327 -p1
%patch1328 -p1
%patch1329 -p1
%patch1330 -p1
%patch1331 -p1
%patch1332 -p1
%patch1333 -p1
%patch1334 -p1
%patch1335 -p1
%patch1336 -p1
%patch1337 -p1
%patch1338 -p1
%patch1339 -p1
%patch1340 -p1
%patch1341 -p1
%patch1342 -p1
%patch1343 -p1
%patch1344 -p1
%patch1345 -p1
%patch1346 -p1
%patch1347 -p1
%patch1348 -p1
%patch1349 -p1
%patch1350 -p1
%patch1351 -p1
%patch1352 -p1
%patch1353 -p1
%patch1354 -p1
%patch1355 -p1
%patch1356 -p1
%patch1357 -p1
%patch1358 -p1
%patch1359 -p1
%patch1360 -p1
%patch1361 -p1
%patch1362 -p1
%patch1363 -p1
%patch1364 -p1
%patch1365 -p1
%patch1366 -p1
%patch1367 -p1
%patch1368 -p1
%patch1369 -p1
%patch1370 -p1
%patch1371 -p1
%patch1372 -p1
%patch1373 -p1
%patch1374 -p1
%patch1375 -p1
%patch1376 -p1
%patch1377 -p1
%patch1378 -p1
%patch1379 -p1
%patch1380 -p1
%patch1381 -p1
%patch1382 -p1
%patch1383 -p1
%patch1384 -p1
%patch1385 -p1
%patch1386 -p1
%patch1387 -p1
%patch1388 -p1
%patch1389 -p1
%patch1390 -p1
%patch1391 -p1
%patch1392 -p1
%patch1393 -p1
%patch1394 -p1
%patch1395 -p1
%patch1396 -p1
%patch1397 -p1
%patch1398 -p1
%patch1399 -p1
%patch1400 -p1
%patch1401 -p1
%patch1402 -p1
%patch1403 -p1
%patch1404 -p1
%patch1405 -p1
%patch1406 -p1
%patch1407 -p1
%patch1408 -p1
%patch1409 -p1
%patch1410 -p1
%patch1411 -p1
%patch1412 -p1
%patch1413 -p1
%patch1414 -p1
%patch1415 -p1
%patch1416 -p1
%patch1417 -p1
%patch1418 -p1
%patch1419 -p1
%patch1420 -p1
%patch1421 -p1
%patch1422 -p1
%patch1423 -p1
%patch1424 -p1
%patch1425 -p1
%patch1426 -p1
%patch1427 -p1
%patch1428 -p1
%patch1429 -p1
%patch1430 -p1
%patch1431 -p1
%patch1432 -p1
%patch1433 -p1
%patch1434 -p1
%patch1435 -p1
%patch1436 -p1
%patch1437 -p1
%patch1438 -p1
%patch1439 -p1
%patch1440 -p1
%patch1441 -p1
%patch1442 -p1
%patch1443 -p1
%patch1444 -p1
%patch1445 -p1
%patch1446 -p1
%patch1447 -p1
%patch1448 -p1
%patch1449 -p1
%patch1450 -p1
%patch1451 -p1
%patch1452 -p1
%patch1453 -p1
%patch1454 -p1
%patch1455 -p1
%patch1456 -p1
%patch1457 -p1
%patch1458 -p1
%patch1459 -p1
%patch1460 -p1
%patch1461 -p1
%patch1462 -p1
%patch1463 -p1
%patch1464 -p1
%patch1465 -p1
%patch1466 -p1
%patch1467 -p1
%patch1468 -p1
%patch1469 -p1
%patch1470 -p1
%patch1471 -p1
%patch1472 -p1
%patch1473 -p1
%patch1474 -p1
%patch1475 -p1
%patch1476 -p1
%patch1477 -p1
%patch1478 -p1
%patch1479 -p1
%patch1480 -p1
%patch1481 -p1
%patch1482 -p1
%patch1483 -p1
%patch1484 -p1
%patch1485 -p1
%patch1486 -p1
%patch1487 -p1
%patch1488 -p1
%patch1489 -p1
%patch1490 -p1
%patch1491 -p1
%patch1492 -p1
%patch1493 -p1
%patch1494 -p1
%patch1495 -p1
%patch1496 -p1
%patch1497 -p1
%patch1498 -p1
%patch1499 -p1
%patch1500 -p1
%patch1501 -p1
%patch1502 -p1
%patch1503 -p1
%patch1504 -p1
%patch1505 -p1
%patch1506 -p1
%patch1507 -p1
%patch1508 -p1
%patch1509 -p1
%patch1510 -p1
%patch1511 -p1
%patch1513 -p1
%patch1514 -p1
%patch1515 -p1
%patch1516 -p1
%patch1517 -p1
%patch1518 -p1
%patch1519 -p1
%patch1520 -p1
%patch1521 -p1
%patch1522 -p1
%patch1523 -p1
%patch1524 -p1
%patch1525 -p1
%patch1526 -p1
%patch1527 -p1
%patch1528 -p1
%patch1529 -p1
%patch1530 -p1
%patch1531 -p1
%patch1532 -p1
%patch1533 -p1
%patch1534 -p1
%patch1535 -p1
%patch1536 -p1
%patch1537 -p1
%patch1538 -p1
%patch1539 -p1
%patch1540 -p1
%patch1541 -p1
%patch1542 -p1
%patch1543 -p1
%patch1544 -p1
%patch1545 -p1
%patch1546 -p1
%patch1547 -p1
%patch1548 -p1
%patch1549 -p1
%patch1550 -p1
%patch1551 -p1
%patch1552 -p1
%patch1553 -p1
%patch1554 -p1
%patch1555 -p1
%patch1556 -p1
%patch1557 -p1
%patch1558 -p1
%patch1559 -p1
%patch1560 -p1
%patch1561 -p1
%patch1562 -p1
%patch1563 -p1
%patch1564 -p1
%patch1565 -p1
%patch1566 -p1
%patch1567 -p1
%patch1568 -p1
%patch1569 -p1
%patch1570 -p1
%patch1571 -p1
%patch1572 -p1
%patch1573 -p1
%patch1574 -p1
%patch1575 -p1
%patch1576 -p1
%patch1577 -p1
%patch1578 -p1
%patch1579 -p1
%patch1580 -p1
%patch1581 -p1
%patch1582 -p1
%patch1583 -p1
%patch1584 -p1
%patch1585 -p1
%patch1586 -p1
%patch1587 -p1
%patch1588 -p1
%patch1589 -p1
%patch1590 -p1
%patch1591 -p1
%patch1592 -p1
%patch1593 -p1
%patch1594 -p1
%patch1595 -p1
%patch1596 -p1
%patch1597 -p1
%patch1598 -p1
%patch1599 -p1
%patch1600 -p1
%patch1601 -p1
%patch1602 -p1
%patch1603 -p1
%patch1604 -p1
%patch1605 -p1
%patch1606 -p1
%patch1607 -p1
%patch1608 -p1
%patch1609 -p1
%patch1610 -p1
%patch1611 -p1
%patch1612 -p1
%patch1613 -p1
%patch1614 -p1
%patch1615 -p1
%patch1616 -p1
%patch1617 -p1
%patch1618 -p1
%patch1619 -p1
%patch1620 -p1
%patch1621 -p1
%patch1622 -p1
%patch1623 -p1
%patch1624 -p1
%patch1625 -p1
%patch1626 -p1
%patch1627 -p1
%patch1628 -p1
%patch1629 -p1
%patch1630 -p1
%patch1631 -p1
%patch1634 -p1
%patch1635 -p1
%patch1636 -p1
%patch1637 -p1
%patch1638 -p1
%patch1639 -p1
%patch1640 -p1
%patch1641 -p1
%patch1642 -p1
%patch1643 -p1
%patch1644 -p1
%patch1645 -p1
%patch1646 -p1
%patch1647 -p1
%patch1648 -p1
%patch1649 -p1
%patch1650 -p1
%patch1651 -p1
%patch1652 -p1
%patch1653 -p1
%patch1654 -p1
%patch1655 -p1
%patch1656 -p1
%patch1657 -p1
%patch1658 -p1
%patch1659 -p1
%patch1660 -p1
%patch1661 -p1
%patch1662 -p1
%patch1663 -p1
%patch1664 -p1
%patch1665 -p1
%patch1666 -p1
%patch1667 -p1
%patch1668 -p1
%patch1669 -p1
%patch1670 -p1
%patch1671 -p1
%patch1672 -p1
%patch1673 -p1
%patch1674 -p1
%patch1675 -p1
%patch1676 -p1
%patch1677 -p1
%patch1678 -p1
%patch1679 -p1
%patch1680 -p1
%patch1681 -p1
%patch1682 -p1
%patch1683 -p1
%patch1684 -p1
%patch1685 -p1
%patch1686 -p1
%patch1687 -p1
%patch1688 -p1
%patch1689 -p1
%patch1690 -p1
%patch1691 -p1
%patch1692 -p1
%patch1693 -p1

%build
# --build-id option is used fedora 8 onwards for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# sdl outputs to alsa or pulseaudio depending on system config, but it's broken (#495964)
# alsa works, but causes huge CPU load due to bugs
# oss works, but is very problematic because it grabs exclusive control of the device causing other apps to go haywire
./configure --target-list=x86_64-softmmu \
            --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
            --cpuconfdir=%{cpumodeldir} \
            --audio-drv-list=pa,alsa \
            --audio-card-list=ac97,es1370 \
            --disable-strip \
            --extra-ldflags=$extraldflags \
            --extra-cflags="$RPM_OPT_FLAGS" \
            --disable-xen \
            --block-drv-whitelist=qcow2,raw,file,host_device,host_cdrom \
            --disable-debug-tcg \
            --disable-sparse \
            --enable-werror \
            --disable-sdl \
            --disable-curses \
            --disable-curl \
            --disable-check-utests \
            --enable-vnc-tls \
            --enable-vnc-sasl \
            --disable-brlapi \
            --disable-bluez \
            --enable-docs \
            --disable-vde \
            --enable-linux-aio \
            --enable-kvm \
            --enable-spice \
            --enable-kvm-cap-pit \
            --enable-kvm-cap-device-assignment

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

make V=1 %{?_smp_mflags} $buildldflags

%install
rm -rf $RPM_BUILD_ROOT

install -D -p -m 0755 %{SOURCE4} $RPM_BUILD_ROOT%{_initddir}/ksm
install -D -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm

install -D -p -m 0755 %{SOURCE6} $RPM_BUILD_ROOT%{_initddir}/ksmtuned
install -D -p -m 0755 %{SOURCE7} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d

install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/blacklist-kvm.conf

make prefix="${RPM_BUILD_ROOT}%{_prefix}" \
     bindir="${RPM_BUILD_ROOT}%{_bindir}" \
     sharedir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" \
     mandir="${RPM_BUILD_ROOT}%{_mandir}" \
     docdir="${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}" \
     datadir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" \
     cpuconfdir="${RPM_BUILD_ROOT}%{cpumodeldir}" \
     sysconfdir="${RPM_BUILD_ROOT}%{_sysconfdir}" install

mv ${RPM_BUILD_ROOT}%{_bindir}/qemu-system-x86_64 ${RPM_BUILD_ROOT}%{_libexecdir}/qemu-kvm

rm -rf ${RPM_BUILD_ROOT}%{_bindir}/qemu-nbd
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man8/qemu-nbd.8*

chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
install -D -p -m 0644 -t ${RPM_BUILD_ROOT}%{qemudocdir} Changelog README TODO COPYING COPYING.LIB LICENSE

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu-kvm.conf

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/pxe*bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vgabios*bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bios.bin
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-ppc
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc32
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc64
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/petalogix-s3adsp1800.dtb
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/video.x
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bamboo.dtb
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/ppc_rom.bin

# the pxe gpxe images will be symlinks to the images on
# /usr/share/gpxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
  ln -s ../gpxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.bin
}

pxe_link e1000 e1000-0x100e
pxe_link ne2k_pci rtl8029
pxe_link pcnet pcnet32
pxe_link rtl8139 rtl8139
pxe_link virtio virtio-net
ln -s ../vgabios/VGABIOS-lgpl-latest.bin  %{buildroot}/%{_datadir}/%{name}/vgabios.bin
ln -s ../vgabios/VGABIOS-lgpl-latest.cirrus.bin %{buildroot}/%{_datadir}/%{name}/vgabios-cirrus.bin
ln -s ../vgabios/VGABIOS-lgpl-latest.qxl.bin %{buildroot}/%{_datadir}/%{name}/vgabios-qxl.bin
ln -s ../seabios/bios.bin %{buildroot}/%{_datadir}/%{name}/bios.bin

%clean
rm -rf $RPM_BUILD_ROOT

%post
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu

/sbin/chkconfig --add ksm
/sbin/chkconfig --add ksmtuned

# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
sh %{_sysconfdir}/sysconfig/modules/kvm.modules

%preun
if [ $1 -eq 0 ]; then
    /sbin/service ksmtuned stop &>/dev/null || :
    /sbin/chkconfig --del ksmtuned
    /sbin/service ksm stop &>/dev/null || :
    /sbin/chkconfig --del ksm
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service ksm condrestart &>/dev/null || :
    /sbin/service ksmtuned condrestart &>/dev/null || :
fi

%files
%defattr(-,root,root)
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/TODO
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/qemu-tech.html
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/keymaps/
%{_mandir}/man1/qemu-kvm.1*
%config(noreplace) %{_sysconfdir}/sasl2/qemu-kvm.conf
%{_initddir}/ksm
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_initddir}/ksmtuned
%{_sbindir}/ksmtuned
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/vapic.bin
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/pxe-e1000.bin
%{_datadir}/%{name}/pxe-virtio.bin
%{_datadir}/%{name}/pxe-pcnet.bin
%{_datadir}/%{name}/pxe-rtl8139.bin
%{_datadir}/%{name}/pxe-ne2k_pci.bin
%{_datadir}/%{name}/extboot.bin
%{_libexecdir}/qemu-kvm
%{_sysconfdir}/sysconfig/modules/kvm.modules
%{_sysconfdir}/udev/rules.d/80-kvm.rules
%{cpumodeldir}/cpu-x86_64.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/blacklist-kvm.conf

%files tools
%defattr(-,root,root,-)
%{_bindir}/kvm_stat

%files -n qemu-img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_mandir}/man1/qemu-img.1*

%changelog
* Tue Aug 24 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.113.el6
- kvm-disable-guest-provided-stats-on-info-ballon-monitor-.patch [bz#623903]
- Resolves: bz#623903
  (query-balloon commmand didn't return on pasued guest cause virt-manger hang)

* Wed Aug 18 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.112.el6
- kvm-qemu-img-rebase-Open-new-backing-file-read-only.patch [bz#624666]
- Resolves: bz#624666
  (qemu-img re-base broken on RHEL6)

* Tue Aug 17 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.111.el6
- blacklist vhost_net [bz#624769]
- Resolves: bz#624769
  (Blacklist vhost_net)

* Mon Aug 16 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.110.el6
- kvm-vhost-Fix-size-of-dirty-log-sync-on-resize.patch [bz#622356]
- Resolves: bz#622356
  (Live migration failed during reboot due to vhost)

* Mon Aug 09 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.109.el6
- kvm-qdev-Reset-hotplugged-devices.patch [bz#607611]
- kvm-Block-I-O-signals-in-audio-helper-threads.patch [bz#621161]
- Resolves: bz#607611
  (pci hotplug of e1000, rtl8139 nic device fails for all guests.)
- Resolves: bz#621161
  (qemu-kvm crashes with I/O Possible message)

* Wed Aug 04 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.108.el6
- kvm-Fix-migration-with-spice-enabled.patch [bz#618168]
- kvm-virtio-Factor-virtqueue_map_sg-out.patch [bz#607244]
- kvm-virtio-blk-Fix-migration-of-queued-requests.patch [bz#607244]
- Resolves: bz#607244
  (virtio-blk doesn't load list of pending requests correctly)
- Resolves: bz#618168
  (Qemu-kvm in the src host core dump when do migration by using spice)

* Tue Aug 03 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.107.el6
- kvm-Correct-cpuid-flags-and-model-fields-V2.patch [bz#613892 bz#618332]
- Resolves: bz#613892
  ([SR-IOV]VF device can not start on 32bit Windows2008 SP2)
- Resolves: bz#618332
  (CPUID_EXT_POPCNT enabled in qemu64 and qemu32 built-in models.)

* Fri Jul 30 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.106.el6
- kvm-device-assignment-Leave-option-ROM-space-RW-KVM-does.patch [bz#618788]
- kvm-block-Fix-bdrv_has_zero_init.patch [bz#616890]
- kvm-Fix-segfault-in-mmio-subpage-handling-code.patch [bz#619414]
- kvm-Migration-reopen-block-devices-files.patch [bz#618601]
- Resolves: bz#616890
  ("qemu-img convert" fails on block device)
- Resolves: bz#618601
  (We need to reopen images after migration)
- Resolves: bz#618788
  (device-assignment hangs with kvm_run: Bad address)
- Resolves: bz#619414
  (CVE-2010-2784 qemu: insufficient constraints checking in exec.c:subpage_register() [rhel-6.0])

* Wed Jul 28 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.105.el6
- kvm-device-assignment-Use-PCI-I-O-port-sysfs-resource-fi.patch [bz#615214]
- kvm-block-Change-bdrv_eject-not-to-drop-the-image.patch [bz#558256]
- Resolves: bz#558256
  (rhel6 disk not detected first time in install)
- Resolves: bz#615214
  ([VT-d] Booting RHEL6 guest with Intel 82541PI NIC assigned by libvirt cause qemu crash)

* Tue Jul 27 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.104.el6
- kvm-vhost_dev_unassign_memory-don-t-assert-if-removing-f.patch [bz#617085]
- Resolves: bz#617085
  (core dumped when add netdev to VM with vhost on)

* Tue Jul 27 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.103.el6
- kvm-migration-Accept-cont-only-after-successful-incoming.patch [bz#581555]
- Resolves: bz#581555
  (race between qemu monitor "cont" and incoming migration can cause failed restore/migration)

* Tue Jul 27 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.102.el6
- kvm-spice-Rename-conflicting-ramblock.patch [bz#617463]
- kvm-block-default-to-0-minimal-optimal-I-O-size.patch [bz#617271]
- Resolves: bz#617271
  (RHEL6 qemu-kvm guest gets partitioned at sector 63)
- Resolves: bz#617463
  (Coredump occorred when enable qxl)

* Tue Jul 27 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.101.el6
- kvm-virtio-net-correct-packet-length-checks.patch [bz#591494]
- kvm-avoid-canceling-ide-dma-rediff.patch [bz#617414]
- Resolves: bz#591494
  (Virtio: Transfer file caused guest in same vlan abnormally quit)
- Resolves: bz#617414
  (avoid canceling in flight ide dma)

* Mon Jul 26 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.100.el6
- kvm-Disable-SCSI.patch [bz#617534]
- kvm-spice-don-t-force-fullscreen-redraw-on-display-resiz.patch [bz#612074]
- kvm-KVM_GET_SUPPORTED_CPUID-doesn-t-return-all-host-cpui.patch [bz#616188]
- kvm-Do-not-try-loading-option-ROM-for-hotplug-PCI-device.patch [bz#612696]
- Resolves: bz#612074
  (core dumped while live migration with spice)
- Resolves: bz#612696
  (virsh attach-device crash kvm guest.)
- Resolves: bz#616188
  (KVM_GET_SUPPORTED_CPUID doesn't return all host cpuid flags..)
- Resolves: bz#617534
  (Disable SCSI and usb-storage)

* Thu Jul 22 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.99.el6
- kvm-Documentation-Add-a-warning-message-to-qemu-kvm-help.patch [bz#596232]
- Resolves: bz#596232
  (Update docs to exclude unsupported options)

* Thu Jul 22 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.98.el6
- kvm-ram_blocks-Convert-to-a-QLIST.patch [bz#596328]
- kvm-Remove-uses-of-ram.last_offset-aka-last_ram_offset.patch [bz#596328]
- kvm-pc-Allocate-all-ram-in-a-single-qemu_ram_alloc.patch [bz#596328]
- kvm-qdev-Add-a-get_dev_path-function-to-BusInfo.patch [bz#596328]
- kvm-pci-Implement-BusInfo.get_dev_path.patch [bz#596328]
- kvm-savevm-Add-DeviceState-param.patch [bz#596328]
- kvm-savevm-Make-use-of-DeviceState.patch [bz#596328]
- kvm-eepro100-Add-a-dev-field-to-eeprom-new-free-function.patch [bz#596328]
- kvm-virtio-net-Incorporate-a-DeviceState-pointer-and-let.patch [bz#596328]
- kvm-qemu_ram_alloc-Add-DeviceState-and-name-parameters.patch [bz#596328]
- kvm-ramblocks-Make-use-of-DeviceState-pointer-and-BusInf.patch [bz#596328]
- kvm-savevm-Migrate-RAM-based-on-name-offset.patch [bz#596328]
- kvm-savevm-Use-RAM-blocks-for-basis-of-migration.patch [bz#596328]
- kvm-savevm-Create-a-new-continue-flag-to-avoid-resending.patch [bz#596328]
- kvm-qemu_ram_free-Implement-it.patch [bz#596328]
- kvm-pci-Free-the-space-allocated-for-the-option-rom-on-r.patch [bz#596328]
- kvm-ramblocks-No-more-being-lazy-about-duplicate-names.patch [bz#596328]
- kvm-savevm-Reset-last-block-info-at-beginning-of-each-sa.patch [bz#616525]
- kvm-block-Change-bdrv_commit-to-handle-multiple-sectors-.patch [bz#615152]
- kvm-Revert-virtio-Enable-the-PUBLISH_USED-feature-by-def.patch [bz#616501]
- kvm-Revert-vhost-net-check-PUBLISH_USED-in-backend.patch [bz#616501]
- kvm-Revert-virtio-utilize-PUBLISH_USED_IDX-feature.patch [bz#616501]
- kvm-savevm-Fix-memory-leak-of-compat-struct.patch [bz#596328]
- kvm-virtio-blk-Create-exit-function-to-unregister-savevm.patch [bz#580010]
- Resolves: bz#580010
  (migration failed after pci_add and pci_del a virtio storage device)
- Resolves: bz#596328
  ([RHEL6 Beta1] : KVM guest remote migration fails with pci device hotplug.)
- Resolves: bz#615152
  (rhel 6 performance worse than rhel5.6 when committing 1G  changes recorded in  snapshot in its base image.)
- Resolves: bz#616501
  (publish used ABI incompatible with future guests)
- Resolves: bz#616525
  (savevm needs to reset block info on each new save)

* Tue Jul 20 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.97.el6
- kvm-block-Fix-early-failure-in-multiwrite.patch [bz#602209]
- kvm-block-Handle-multiwrite-errors-only-when-all-request.patch [bz#602209]
- kvm-migration-respect-exit-status-with-exec.patch [bz#584372]
- kvm-set-proper-migration-status-on-write-error-v3.patch [bz#584372]
- kvm-Set-SMBIOS-vendor-to-QEMU-for-RHEL5-machine-types.patch [bz#614377]
- kvm-Don-t-reset-bs-is_temporary-in-bdrv_open_common.patch [bz#611797]
- kvm-Change-default-CPU-model-qemu64-to-model-6.patch [bz#614537]
- kvm-set-model-6-on-Intel-CPUs-on-cpu-x86_64.conf.patch [bz#614537]
- kvm-vhost-fix-miration-during-device-start.patch [bz#615228]
- Resolves: bz#584372
  (Fails to detect errors when using exec: based migration)
- Resolves: bz#602209
  (Core dumped during Guest installation)
- Resolves: bz#611797
  (qemu does not call unlink() on temp files in snapshot mode)
- Resolves: bz#614377
  (Windows 7 requires re-activation when migrated from RHEL5 to RHEL6)
- Resolves: bz#614537
  (Skype crashes on VM.)
- Resolves: bz#615228
  (oom in vhost_dev_start)

* Thu Jul 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.96.el6
- fix some errors in ksmd.init [bz#570467]
- fix some errors in ksmtuned.init [bz#579883]
- kvm-Add-x2apic-to-cpuid-feature-set-for-new-AMD-models.-.patch [bz#613884]
- Resolves: bz#570467
  ([RHEL 6] Initscripts improvement for ksm and ksmtuned)
- Resolves: bz#579883
  (init script doesn't stop ksmd)
- Resolves: bz#613884
  (x2apic needs to be present in all new AMD cpu models..)

* Wed Jul 14 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.95.el6
- kvm-Move-CPU-definitions-to-usr-share-.-BZ-610805.patch [bz#610805]
- kvm-QEMUFileBuffered-indicate-that-we-re-ready-when-the-.patch [bz#609261]
- kvm-device-assignment-Better-fd-tracking.patch [bz#611715]
- Resolves: bz#609261
  (Exec outgoing migration is too slow)
- Resolves: bz#610805
  (Move CPU definitions to /usr/share/...)
- Resolves: bz#611715
  (qemu-kvm gets no responsive  when do  hot-unplug pass-through device)

* Tue Jul 13 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.94.el6
- kvm-Revert-ide-save-restore-pio-atapi-cmd-transfer-field.patch [bz#612481]
- kvm-vmstate-add-subsections-code.patch [bz#612481]
- kvm-ide-fix-migration-in-the-middle-of-pio-operation.patch [bz#612481]
- kvm-ide-fix-migration-in-the-middle-of-a-bmdma-transfer.patch [bz#612481]
- kvm-Initial-documentation-for-migration-Signed-off-by-Ju.patch [bz#612481]
- kvm-Disable-non-rhel-machine-types-pc-0.12-pc-0.11-pc-0..patch [bz#607263]
- Resolves: bz#607263
  (Remove -M pc-0.12 support)
- Resolves: bz#612481
  (Enable migration subsections)

* Fri Jul 09 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.93.el6
- kvm-make-rtc-alatm-work.patch [bz#598836]
- kvm-qemu-img-check-Distinguish-different-kinds-of-errors.patch [bz#612164]
- kvm-qcow2-vdi-Change-check-to-distinguish-error-cases.patch [bz#612164]
- Resolves: bz#598836
  (RHEL 6.0 RTC Alarm unusable in vm)
- Resolves: bz#612164
  ([kvm] qemu image check returns cluster errors when using virtIO block (thinly provisioned) during e_no_space events (along with EIO errors))

* Wed Jul 07 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.92.el6
- build-time-only fix: fix the tarball-generation make-release script for newer git versions
  (kvm-make-release-fix-mtime-on-rhel6-beta.patch)
- Related: bz#581963 bz#582262 bz#611229

* Wed Jul 07 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.91.el6
- kvm-doc-Update-monitor-info-subcommands.patch [bz#582262]
- kvm-Fix-typo-in-balloon-help.patch [bz#582262]
- kvm-monitor-Reorder-info-documentation.patch [bz#582262]
- kvm-QMP-Introduce-commands-documentation.patch [bz#582262]
- kvm-QMP-Sync-documentation-with-RHEL6-only-changes.patch [bz#582262]
- kvm-Monitor-Drop-QMP-documentation-from-code.patch [bz#582262]
- kvm-hxtool-Fix-line-number-reporting-on-SQMP-EQMP-errors.patch [bz#582262]
- kvm-monitor-New-command-__com.redhat_drive_add.patch [bz#581963]
- kvm-Fix-driftfix-option.patch [bz#611229]
- Resolves: bz#581963
  (QMP: missing drive_add command in JSON mode)
- Resolves: bz#582262
  (QMP: Missing commands doc)
- Resolves: bz#611229
  (-rtc cmdline changes)

* Tue Jun 29 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.90.el6
- kvm-device-assignment-Avoid-munmapping-the-real-MSIX-are.patch [bz#572043]
- kvm-device-assignment-Cleanup-on-exit.patch [bz#572043]
- Resolves: bz#572043
  (Guest gets segfault when do multiple device hot-plug and hot-unplug)

* Tue Jun 29 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.89.el6
- kvm-device-assignment-be-more-selective-in-interrupt-dis.patch [bz#605361]
- Resolves: bz#605361
  (82576 physical function device assignment doesn't work with win7)

* Tue Jun 29 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.88.el6
- kvm-Exit-if-incoming-migration-fails.patch [bz#570174]
- kvm-Factorize-common-migration-incoming-code.patch [bz#570174]
- Resolves: bz#570174
  (Restoring a qemu guest from a saved state file using -incoming sometimes fails and hangs)

* Tue Jun 29 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.87.el6
- kvm-qxl-drop-check-for-depths-32.patch [bz#597198]
- kvm-spice-handle-16-bit-color-depth.patch [bz#597198 bz#600205]
- kvm-device-assignment-Don-t-deassign-when-the-assignment.patch [bz#597968]
- kvm-block-fix-physical_block_size-calculation.patch [bz#566785]
- kvm-Add-x2apic-to-cpuid-feature-set-for-new-Intel-models.patch [bz#601517]
- Resolves: bz#566785
  (virt block layer must not keep guest's logical_block_size fixed)
- Resolves: bz#597198
  (qxl: 16bpp vga mode is broken.)
- Resolves: bz#597968
  (Should not allow one physical NIC card to be assigned to one guest for many times)
- Resolves: bz#600205
  (Live migration cause qemu-kvm Segmentation fault (core dumped)by using "-vga std")
- Resolves: bz#601517
  (x2apic needs to be present in all new Intel cpu models..)

* Mon Jun 28 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.86.el6
- kvm-net-delete-QemuOpts-when-net_client_init-fails.patch [bz#603851]
- kvm-QMP-Fix-error-reporting-in-the-async-API.patch [bz#587382]
- kvm-QMP-Remove-leading-whitespace-in-package.patch [bz#580648]
- kvm-Add-optional-dump-of-default-config-file-paths-v2-BZ.patch [bz#601540]
- Resolves: bz#580648
  (QMP: Bad package version in greeting message)
- Resolves: bz#587382
  (QMP: balloon command may not report an error)
- Resolves: bz#601540
  (qemu requires ability to verify location of cpu model definition file..)
- Resolves: bz#603851
  (QMP: Can't reuse same 'id' when netdev_add fails)

* Mon Jun 28 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.85.el6
- kvm-Remove-usage-of-CONFIG_RED_HAT_DISABLED.patch [bz#605638]
- kvm-monitor-Remove-host_net_add-remove-for-Red-Hat-Enter.patch [bz#605638]
- kvm-monitor-Remove-usb_add-del-commands-for-Red-Hat-Ente.patch [bz#605638]
- kvm-virtio-blk-fix-the-list-operation-in-virtio_blk_load.patch [bz#607244]
- kvm-QError-Introduce-QERR_DEVICE_INIT_FAILED_2.patch [bz#596279]
- kvm-dev-assignment-Report-IRQ-assign-errors-in-QMP.patch [bz#596279]
- Resolves: bz#596279
  (QMP: does not report the real cause of PCI device assignment failure)
- Resolves: bz#605638
  (Remove unsupported monitor commands from qemu-kvm)
- Resolves: bz#607244
  (virtio-blk doesn't load list of pending requests correctly)

* Mon Jun 28 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.84.el6
- kvm-Add-KVM-paravirt-cpuid-leaf.patch [bz#606084]
- Resolves: bz#606084
  (Allow control of kvm cpuid option via -cpu flag)

* Mon Jun 28 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.83.el6
- kvm-add-some-tests-for-invalid-JSON.patch [bz#585009]
- kvm-implement-optional-lookahead-in-json-lexer.patch [bz#585009]
- kvm-remove-unnecessary-lookaheads.patch [bz#585009]
- kvm-per-machine-type-smbios-Type-1-smbios-values.patch [bz#605704]
- kvm-raw-posix-Use-pread-pwrite-instead-of-lseek-read-wri.patch [bz#607688]
- kvm-block-Cache-total_sectors-to-reduce-bdrv_getlength-c.patch [bz#607688]
- kvm-block-allow-filenames-with-colons-again-for-host-dev.patch [bz#599122]
- Resolves: bz#585009
  (QMP: input needs trailing  char)
- Resolves: bz#599122
  (Unable to launch QEMU with a guest disk filename containing a ':')
- Resolves: bz#605704
  (qemu-kvm: set per-machine-type smbios strings)
- Resolves: bz#607688
  (Excessive lseek() causes severe performance issues with vm disk images over NFS)

* Fri Jun 25 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.82.el6
- kvm-monitor-allow-device-to-be-ejected-if-no-disk-is-ins.patch [bz#581789]
- kvm-New-slots-need-dirty-tracking-enabled-when-migrating.patch [bz#596609]
- kvm-Make-netdev_del-delete-the-netdev-even-when-it-s-in-.patch [bz#596274]
- kvm-device-assignment-msi-PBA-is-long.patch [bz#605359]
- kvm-qcow2-Fix-qemu-img-check-segfault-on-corrupted-image.patch [bz#604210]
- kvm-qcow2-Don-t-try-to-check-tables-that-couldn-t-be-loa.patch [bz#604210]
- kvm-qcow2-Fix-error-handling-during-metadata-preallocati.patch [bz#604210]
- kvm-block-Add-bdrv_-p-write_sync.patch [bz#607200]
- kvm-qcow2-Use-bdrv_-p-write_sync-for-metadata-writes.patch [bz#607200]
- kvm-virtio-serial-Fix-compat-property-name.patch [bz#607263]
- kvm-rtc-Remove-TARGET_I386-from-qemu-config.c-enables-dr.patch [bz#606733]
- Resolves: bz#581789
  (Cannot eject cd-rom when configured to host cd-rom)
- Resolves: bz#596274
  (QMP: netdev_del sometimes fails claiming the device is in use)
- Resolves: bz#596609
  (Live migration failed when migration during boot)
- Resolves: bz#604210
  (Segmentation fault when check  preallocated qcow2 image on lvm.)
- Resolves: bz#605359
  (Fix MSIX regression from bz595495)
- Resolves: bz#606733
  (Unable to set the driftfix parameter)
- Resolves: bz#607200
  (qcow2 image corruption when using cache=writeback)
- Resolves: bz#607263
  (Unable to launch QEMU with -M pc-0.12 and  virtio serial)

* Thu Jun 24 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.81.el6
- kvm-virtio-Enable-the-PUBLISH_USED-feature-by-default-fo.patch [bz#602417]
- kvm-do-not-enter-vcpu-again-if-it-was-stopped-during-IO.patch [bz#595647]
- Resolves: bz#595647
  (Windows guest with qxl driver can't get into S3 state)
- Resolves: bz#602417
  (Enable VIRTIO_RING_F_PUBLISHED bit for all virtio devices)

* Wed Jun 23 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.80.el6
- don't package kvmtrace anymore
- Resolves: bz#605426
  (obsolete kvmtrace binary is still being packaged)

* Tue Jun 22 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.79.el6
- kvm-Make-geometry-of-IDE-drives-defined-with-device-visi.patch [bz#597147]
- Resolves: bz#597147
  (libvirt: kvm disk error after first stage install of Win2K or WinXP)

* Mon Jun 21 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.78.el6
- kvm-block-read-only-open-cdrom-as-read-only-when-using-m.patch [bz#602026]
- kvm-acpi_piix4-save-gpe-and-pci-hotplug-slot-status.patch [bz#598022]
- kvm-Don-t-check-for-bus-master-for-old-guests.patch [bz#596014]
- kvm-Make-IDE-drives-defined-with-device-visible-to-cmos_.patch [bz#597147]
- Resolves: bz#596014
  (hot add virtio-blk-pci via device_add lead to virtio network lost)
- Resolves: bz#597147
  (libvirt: kvm disk error after first stage install of Win2K or WinXP)
- Resolves: bz#598022
  (Hot-added device is not visible in guest after live-migration.)
- Resolves: bz#602026
  (Cannot change cdrom by "change device filename [format] " in (qemu) command line)

* Wed Jun 16 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.77.el6
- kvm.modules: autoload vhost-net module too [bz#596891]
- Resolves: bz#596891
  (vhost-net module should be loaded automatically)

* Wed Jun 16 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.76.el6
- kvm-fix-vnc-memory-corruption-with-width-1400.patch [bz#602724]
- kvm-net-Fix-VM-start-with-net-none.patch [bz#599460]
- kvm-monitor-Remove-pci_add-command-for-Red-Hat-Enterpris.patch [bz#602590]
- kvm-monitor-Remove-pci_del-command-for-Red-Hat-Enterpris.patch [bz#602590]
- kvm-monitor-Remove-drive_add-command-for-Red-Hat-Enterpr.patch [bz#602590]
- Resolves: bz#599460
  (virtio nic is hotpluged when hotplug rtl8139 nic to guest)
- Resolves: bz#602590
  (Disable pci_add, pci_del, drive_add)
- Resolves: bz#602724
  (VNC disconnect segfault on KVM video consoles)

* Tue Jun 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.75.el6
- kvm-qcow2-Fix-corruption-after-refblock-allocation.patch [bz#598407]
- kvm-qcow2-Fix-corruption-after-error-in-update_refcount.patch [bz#598507]
- kvm-qcow2-Allow-qcow2_get_cluster_offset-to-return-error.patch [bz#598507]
- kvm-qcow2-Change-l2_load-to-return-0-errno.patch [bz#598507]
- kvm-qcow2-Return-right-error-code-in-write_refcount_bloc.patch [bz#598507]
- kvm-qcow2-Clear-L2-table-cache-after-write-error.patch [bz#598507]
- kvm-qcow2-Fix-error-handling-in-l2_allocate.patch [bz#598507]
- kvm-qcow2-Restore-L1-entry-on-l2_allocate-failure.patch [bz#598507]
- kvm-qcow2-Allow-get_refcount-to-return-errors.patch [bz#598507]
- kvm-qcow2-Avoid-shadowing-variable-in-alloc_clusters_nor.patch [bz#598507]
- kvm-qcow2-Allow-alloc_clusters_noref-to-return-errors.patch [bz#598507]
- kvm-qcow2-Return-real-error-code-in-load_refcount_block.patch [bz#598507]
- kvm-make-release-make-mtime-owner-group-consistent.patch
- Resolves: bz#598407
  (qcow2 corruption bug in refcount table growth)
- Resolves: bz#598507
  (Backport qcow2 error path fixes)

* Mon Jun 14 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.74.el6
- kvm-raw-posix-Detect-CDROM-via-ioctl-on-linux.patch [bz#593758]
- kvm-block-Remove-special-case-for-vvfat.patch [bz#593758]
- kvm-block-Make-find_image_format-return-raw-BlockDriver-.patch [bz#593758]
- kvm-block-Add-missing-bdrv_delete-for-SG_IO-BlockDriver-.patch [bz#593758]
- kvm-block-Assume-raw-for-drives-without-media.patch [bz#593758]
- Resolves: bz#593758
  (qemu fails to start with -cdrom /dev/sr0 if no media inserted)

* Fri Jun 11 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.73.el6
- kvm-net-Fix-hotplug-with-pci_add.patch [bz#599460]
- Resolves: bz#599460
  (virtio nic is hotpluged when hotplug rtl8139 nic to guest)

* Wed Jun 09 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.72.el6
- kvm-Monitor-Make-RFQDN_REDHAT-public.patch [bz#586349]
- kvm-QMP-Add-error-reason-to-BLOCK_IO_ERROR-event.patch [bz#586349]
- kvm-virtio-net-truncating-packet.patch [bz#591494]
- kvm-vhost-net-check-PUBLISH_USED-in-backend.patch [bz#600203]
- kvm-device-assignment-don-t-truncate-MSIX-capabilities-t.patch [bz#596315]
- kvm-If-a-USB-keyboard-is-unplugged-the-keyboard-eventhan.patch [bz#561433]
- Resolves: bz#561433
  (Segfault when keyboard is removed)
- Resolves: bz#586349
  (BLOCK_IO_ERROR event does not provide the errno that caused it.)
- Resolves: bz#591494
  (Virtio: Transfer file caused guest in same vlan abnormally quit)
- Resolves: bz#596315
  (device assignment truncates MSIX table size)
- Resolves: bz#600203
  (vhost net new userspace on old kernel: 95: falling back on userspace virtio)

* Mon Jun 07 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.71.el6
- kvm-device-assignment-fix-failure-to-exit-on-shared-IRQ.patch [bz#585310]
- kvm-doc-Fix-host-forwarding-monitor-command-documentatio.patch [bz#588719]
- kvm-doc-Fix-acl-monitor-command-documentation.patch [bz#588719]
- kvm-doc-Heading-for-monitor-command-cpu-got-lost-restore.patch [bz#588719]
- kvm-doc-Clean-up-monitor-command-function-index.patch [bz#588719]
- kvm-fix-info-cpus-halted-state-reporting.patch [bz#593769]
- kvm-sysemu-Export-no_shutdown.patch [bz#559618]
- kvm-Monitor-Return-before-exiting-with-quit.patch [bz#559618]
- kvm-QMP-Add-Downstream-extension-of-QMP-to-spec.patch [bz#566291]
- kvm-Revert-PCI-Convert-pci_device_hot_add-to-QObject.patch [bz#580365]
- kvm-Revert-monitor-Convert-do_pci_device_hot_remove-to-Q.patch [bz#580365]
- kvm-drive-allow-rerror-werror-and-readonly-for-if-none.patch [bz#565609 bz#593256]
- kvm-qdev-properties-Fix-u-intXX-parsers.patch [bz#596093]
- kvm-vnc-factor-out-vnc_desktop_resize.patch [bz#590070]
- kvm-vnc-send-desktopresize-event-as-reply-to-set-encodin.patch [bz#590070]
- kvm-vnc-keep-track-of-client-desktop-size.patch [bz#590070]
- kvm-vnc-don-t-send-invalid-screen-updates.patch [bz#590070]
- kvm-vnc-move-size-changed-check-into-the-vnc_desktop_res.patch [bz#590070]
- kvm-check-for-active_console-before-using-it.patch [bz#591759]
- Resolves: bz#559618
  (QMP: Fix 'quit' to return success before exiting)
- Resolves: bz#565609
  (Unable to use werror/rerror with  -drive syntax using if=none)
- Resolves: bz#566291
  (QMP: Support vendor extensions)
- Resolves: bz#580365
  (QMP: pci_add/pci_del conversion should be reverted)
- Resolves: bz#585310
  (qemu-kvm does not exit when device assignment fails due to IRQ sharing)
- Resolves: bz#588719
  (Fix monitor command documentation)
- Resolves: bz#590070
  (QEMU misses DESKTOP-RESIZE event if it is triggered during client connection initialization)
- Resolves: bz#591759
  (Segmentation fault when using vnc to view guest without vga card)
- Resolves: bz#593256
  (Unable to set readonly flag for floppy disks)
- Resolves: bz#593769
  ("info cpus" doesn't show halted state)
- Resolves: bz#596093
  (16bit integer qdev properties are not parsed correctly.)

* Mon Jun 07 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.70.el6
- kvm-virtio-invoke-set_features-on-load.patch [bz#595263]
- kvm-virtio-net-return-with-value-in-void-function.patch [bz#595263]
- kvm-vhost-net-fix-reversed-logic-in-mask-notifiers.patch [bz#585940]
- kvm-hpet-Disable-for-Red-Hat-Enterprise-Linux.patch [bz#595130]
- ksmtuned: typo MemCached -> Cached [bz#597005]
- kvm-virtio-net-stop-vhost-backend-on-vmstop.patch [bz#598896]
- kvm-msix-fix-msix_set-unset_mask_notifier.patch [bz#598896]
- Resolves: bz#585940
  (qemu-kvm crashes on reboot when vhost is enabled)
- Resolves: bz#595130
  (Disable hpet by default)
- Resolves: bz#595263
  (virtio net lacks upstream fixes as of may 24)
- Resolves: bz#597005
  (ksmtune: typo: MemCached -> Cached)
- Resolves: bz#598896
  (migration breaks networking with vhost-net)

* Tue Jun 01 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.69.el6
- Changes to make-release script with no resulting changes on binary package
- kvm-virtio-utilize-PUBLISH_USED_IDX-feature.patch [bz#595287]
- Resolves: bz#595287
  (virtio net/vhost net speed enhancements from upstream kernel)

* Wed May 26 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.68.el6
- kvm-virtio-blk-fix-barrier-support.patch [bz#595813]
- Resolves: bz#595813
  (virtio-blk doesn't handle barriers correctly)

* Wed May 26 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.67.el6
- kvm-qemu-address-todo-comment-in-exec.c.patch [bz#595301]
- Resolves: bz#595301
  (QEMU terminates without warning with virtio-net and SMP enabled)

* Wed May 26 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.66.el6
- kvm-device-assignment-use-stdint-types.patch [bz#595495]
- kvm-device-assignment-Don-t-use-libpci.patch [bz#595495]
- kvm-device-assignment-add-config-fd-qdev-property.patch [bz#595495]
- Resolves: bz#595495
  (Fail to hotplug pci device to guest)

* Wed May 26 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.65.el6
- kvm-qcow2-Fix-creation-of-large-images.patch [bz#577106]
- kvm-vnc-sync-lock-modifier-state-on-connect.patch [bz#569767]
- kvm-json-lexer-Initialize-x-and-y.patch [bz#589952]
- kvm-json-lexer-Handle-missing-escapes.patch [bz#589952]
- kvm-qjson-Handle-f.patch [bz#589952]
- kvm-json-lexer-Drop-buf.patch [bz#589952]
- kvm-json-streamer-Don-t-use-qdict_put_obj.patch [bz#589952]
- kvm-block-fix-sector-comparism-in-multiwrite_req_compare.patch [bz#596119]
- kvm-block-Fix-multiwrite-with-overlapping-requests.patch [bz#596119]
- Resolves: bz#569767
  (Caps Lock the key's appearance  of guest is not synchronous as host's --view kvm with vnc)
- Resolves: bz#577106
  (Abort/Segfault when creating qcow2 format image with 512b cluster size)
- Resolves: bz#589952
  (QMP breaks when issuing any command with a backslash)
- Resolves: bz#596119
  (Possible corruption after block request merge)

* Tue May 25 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.64.el6
- kvm-qemu-kvm-fix-crash-on-reboot-with-vhost-net.patch [bz#585940]
- Related: bz#585940
  (qemu-kvm crashes on reboot when vhost is enabled)

* Tue May 25 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.63.el6
- kvm-fix-undefined-shifts-by-32.patch [bz#590922]
- kvm-qemu-char.c-drop-debug-printfs-from-qemu_chr_parse_c.patch [bz#590922]
- kvm-Fix-corner-case-in-chardev-udp-parameter.patch [bz#590922]
- kvm-pci-passthrough-zap-option-rom-scanning.patch [bz#590922]
- kvm-UHCI-spurious-interrupt-fix.patch [bz#590922]
- kvm-Fix-SIGFPE-for-vnc-display-of-width-height-1.patch [bz#590922]
- kvm-spice-vmc-remove-ringbuffer.patch [bz#589670]
- kvm-spice-vmc-add-dprintfs.patch [bz#589670]
- Resolves: bz#589670
  (spice: Ensure ring data is save/restored on migration)
- Related: bz#590922
  (backport qemu-kvm-0.12.4 fixes to RHEL6)

* Mon May 24 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.62.el6
- kvm-block-add-logical_block_size-property.patch [bz#566785]
- kvm-virtio-serial-bus-fix-ports_map-allocation.patch [bz#591176]
- kvm-Move-cpu-model-config-file-to-agree-with-rpm-build-B.patch [bz#569661]
- Resolves: bz#566785
  (virt block layer must not keep guest's logical_block_size fixed)
- Resolves: bz#569661
  (RHEL6.0 requires backport of upstream cpu model support..)
- Resolves: bz#591176
  (migration fails since virtio-serial-bus is using uninitialized memory)

* Mon May 24 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.61.el6
- Add "file" format to bdrv whitelist
- Resolves: bz#593909
  (VM can not start by using qemu-kvm-0.12.1.2-2.56.el6)

* Thu May 20 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.60.el6
- kvm-spice-vmc-add-copyright.patch [bz#576488]
- kvm-spice-vmc-remove-debug-prints-and-defines.patch [bz#576488]
- kvm-spice-vmc-add-braces-to-single-line-if-s.patch [bz#576488]
- kvm-spice-vmc-s-SpiceVirtualChannel-SpiceVMChannel-g.patch [bz#576488]
- kvm-spice-vmc-s-spice_virtual_channel-spice_vmc-g.patch [bz#576488]
- kvm-spice-vmc-all-variables-of-type-SpiceVMChannel-renam.patch [bz#576488]
- kvm-spice-vmc-remove-meaningless-cast-of-void.patch [bz#576488]
- kvm-spice-vmc-add-spice_vmc_ring_t-fix-write-function.patch [bz#576488]
- kvm-spice-vmc-don-t-touch-guest_out_ring-on-unplug.patch [bz#576488]
- kvm-spice-vmc-VirtIOSerialPort-vars-renamed-to-vserport.patch [bz#576488]
- kvm-spice-vmc-add-nr-property.patch [bz#576488]
- kvm-spice-vmc-s-SPICE_VM_CHANNEL-SPICE_VMC-g.patch [bz#576488]
- kvm-spice-vmc-add-vmstate.-saves-active_interface.patch [bz#576488]
- kvm-spice-vmc-rename-guest-device-name-to-com.redhat.spi.patch [bz#576488]
- kvm-spice-vmc-remove-unused-property-name.patch [bz#576488]
- Resolves: bz#576488
  (Spice: virtio serial based device for guest-spice client communication)

* Wed May 19 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.59.el6
- kvm-pci-cleanly-backout-of-pci_qdev_init.patch [bz#590884]
- kvm-ide-Fix-ide_dma_cancel.patch [bz#593287]
- Resolves: bz#590884
  (bogus 'info pci' state when hot-added assigned device fails to initialize)
- Resolves: bz#593287
  (Failed asserting during ide_dma_cancel)

* Wed May 19 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.58.el6
- kvm-Fix-segfault-after-device-assignment-hot-remove.patch [bz#582874]
- Resolves: bz#582874
  (Guest hangs during restart after hot unplug then hot plug physical NIC card)

* Wed May 19 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.57.el6
- kvm-stash-away-SCM_RIGHTS-fd-until-a-getfd-command-arriv.patch [bz#582684]
- Resolves: bz#582684
  (Monitor: getfd command is broken)

* Wed May 19 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.56.el6
- kvm-dmg-fix-open-failure.patch [bz#580363]
- kvm-block-get-rid-of-the-BDRV_O_FILE-flag.patch [bz#580363]
- kvm-block-Convert-first_drv-to-QLIST.patch [bz#580363]
- kvm-block-separate-raw-images-from-the-file-protocol.patch [bz#580363]
- kvm-block-Split-bdrv_open.patch [bz#580363]
- kvm-block-Avoid-forward-declaration-of-bdrv_open_common.patch [bz#580363]
- kvm-block-Open-the-underlying-image-file-in-generic-code.patch [bz#580363]
- kvm-block-bdrv_has_zero_init.patch [bz#580363]
- kvm-block-Do-not-export-bdrv_first.patch [bz#590998]
- kvm-block-Convert-bdrv_first-to-QTAILQ.patch [bz#590998]
- kvm-block-Add-wr_highest_sector-blockstat.patch [bz#590998]
- Resolves: bz#580363
  (Error while creating raw image on block device)
- Resolves: bz#590998
  (qcow2 high watermark)

* Wed May 19 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.55.el6
- kvm-turn-off-kvmclock-when-resetting-cpu.patch [bz#588884]
- kvm-virtio-blk-Avoid-zeroing-every-request-structure.patch [bz#593369]
- Resolves: bz#588884
  (Rebooting a kernel with kvmclock enabled, into a kernel with kvmclock disabled, causes random crashes)
- Resolves: bz#593369
  (virtio-blk: Avoid zeroing every request structure)

* Mon May 17 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.54.el6
- kvm-qemu-config-qemu_read_config_file-reads-the-normal-c.patch [bz#588756]
- kvm-qemu-config-Make-qemu_config_parse-more-generic.patch [bz#588756]
- kvm-blkdebug-Basic-request-passthrough.patch [bz#588756]
- kvm-blkdebug-Inject-errors.patch [bz#588756]
- kvm-Make-qemu-config-available-for-tools.patch [bz#588756]
- kvm-blkdebug-Add-events-and-rules.patch [bz#588756]
- kvm-qcow2-Trigger-blkdebug-events.patch [bz#588756]
- kvm-qcow2-Fix-access-after-end-of-array.patch [bz#588762]
- kvm-qcow2-rename-two-QCowAIOCB-members.patch [bz#588762]
- kvm-qcow2-Don-t-ignore-immediate-read-write-failures.patch [bz#588762]
- kvm-qcow2-Remove-request-from-in-flight-list-after-error.patch [bz#588762]
- kvm-qcow2-Return-0-errno-in-write_l2_entries.patch [bz#588762]
- kvm-qcow2-Fix-error-return-code-in-qcow2_alloc_cluster_l.patch [bz#588762]
- kvm-qcow2-Return-0-errno-in-write_l1_entry.patch [bz#588762]
- kvm-qcow2-Return-0-errno-in-l2_allocate.patch [bz#588762]
- kvm-qcow2-Remove-abort-on-free_clusters-failure.patch [bz#588762]
- kvm-Add-qemu-error.o-only-once-to-target-list.patch [bz#591061]
- kvm-block-Fix-bdrv_commit.patch [bz#589439]
- kvm-fix-80000001.EDX-supported-bit-filtering.patch [bz#578106]
- kvm-fix-CPUID-vendor-override.patch [bz#591604]
- Resolves: bz#578106
  (call trace when boot guest with -cpu host)
- Resolves: bz#588756
  (blkdebug is missing)
- Resolves: bz#588762
  (Backport qcow2 fixes)
- Resolves: bz#589439
  (Qcow2 snapshot got corruption after commit using block device)
- Resolves: bz#591061
  (make fails to build after make clean)
- Resolves: bz#591604
  (cannot override cpu vendor from the command line)

* Wed May 12 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.53.el6
- kvm-virtio-blk-Fix-use-after-free-in-error-case.patch [bz#578448]
- kvm-block-Fix-multiwrite-error-handling.patch [bz#578448]
- kvm-Fix-boot-once-option.patch [bz#579692]
- kvm-QError-New-QERR_QMP_BAD_INPUT_OBJECT_MEMBER.patch [bz#573578]
- kvm-QMP-Use-QERR_QMP_BAD_INPUT_OBJECT_MEMBER.patch [bz#573578]
- kvm-QError-Improve-QERR_QMP_BAD_INPUT_OBJECT-desc.patch [bz#573578]
- kvm-QMP-Check-arguments-member-s-type.patch [bz#573578]
- kvm-QMP-Introduce-RESUME-event.patch [bz#590102]
- kvm-pci-irq_state-vmstate-breakage.patch [bz#588133]
- Resolves: bz#573578
  (Segfault when migrating via QMP command interface)
- Resolves: bz#578448
  (qemu-kvm segfault when nfs restart(without using werror&rerror))
- Resolves: bz#579692
  (qemu-kvm "-boot once=drives" couldn't function properly)
- Resolves: bz#588133
  (RHEL5.4 guest can lose virtio networking during migration)
- Resolves: bz#590102
  (QMP: Backport RESUME event)

* Mon May 10 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.52.el6
- kvm-qemu-img-use-the-heap-instead-of-the-huge-stack-arra.patch [bz#585837]
- kvm-qemu-img-rebase-Fix-output-image-corruption.patch [bz#585837]
- Resolves: bz#585837
  (After re-base snapshot, the file in the snapshot disappeared)

* Fri May 07 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.51.el6
- kvm-fdc-fix-drive-property-handling.patch [bz#584902]
- Resolves: bz#584902
  (Cannot associate drive with a floppy device using -global)

* Wed May 05 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.50.el6
- kvm-vl.c-fix-BZ-588828-endless-loop-caused-by-non-option.patch [bz#588828]
- Resolves: bz#588828
  (endless loop when parsing of command line with bare image argument)

* Tue May 04 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.49.el6
- kvm-block-Free-iovec-arrays-allocated-by-multiwrite_merg.patch [bz#586572]
- Resolves: bz#586572
  (virtio-blk multiwrite merge memory leak)
- Force spice to be enabled and fix BuildRequires to use spice-server-devel
- Resolves: bz#588904
  (qemu-kvm builds without spice support)

* Thu Apr 29 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.48.el6
- kvm-virtio-serial-save-load-Ensure-target-has-enough-por.patch [bz#574296]
- kvm-virtio-serial-save-load-Ensure-nr_ports-on-src-and-d.patch [bz#574296]
- kvm-virtio-serial-save-load-Ensure-we-have-hot-plugged-p.patch [bz#574296]
- kvm-virtio-serial-save-load-Send-target-host-connection-.patch [bz#574296]
- kvm-virtio-serial-Use-control-messages-to-notify-guest-o.patch [bz#574296]
- kvm-virtio-serial-whitespace-match-surrounding-code.patch [bz#574296]
- kvm-virtio-serial-Remove-redundant-check-for-0-sized-wri.patch [bz#574296]
- kvm-virtio-serial-Update-copyright-year-to-2010.patch [bz#574296]
- kvm-virtio-serial-Propagate-errors-in-initialising-ports.patch [bz#574296]
- kvm-virtio-serial-Send-out-guest-data-to-ports-only-if-p.patch [bz#574296]
- kvm-iov-Introduce-a-new-file-for-helpers-around-iovs-add.patch [bz#574296]
- kvm-iov-Add-iov_to_buf-and-iov_size-helpers.patch [bz#574296]
- kvm-virtio-serial-Handle-scatter-gather-buffers-for-cont.patch [bz#574296]
- kvm-virtio-serial-Handle-scatter-gather-input-from-the-g.patch [bz#574296]
- kvm-virtio-serial-Apps-should-consume-all-data-that-gues.patch [bz#574296]
- kvm-virtio-serial-Discard-data-that-guest-sends-us-when-.patch [bz#574296]
- kvm-virtio-serial-Implement-flow-control-for-individual-.patch [bz#574296]
- kvm-virtio-serial-Handle-output-from-guest-to-unintialis.patch [bz#574296]
- kvm-virtio-serial-bus-wake-up-iothread-upon-guest-read-n.patch [bz#574296]
- kvm-Bail-out-when-VCPU_CREATE-fails.patch [bz#587227]
- Resolves: bz#574296
  (Fix migration for virtio-serial after port hot-plug/hot-unplug operations)
- Resolves: bz#587227
  (Fix segfault when creating more vcpus than allowed.)

* Wed Apr 28 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.47.el6
- kvm-Request-setting-of-nmi_pending-and-sipi_vector.patch [bz#569613]
- Resolves: bz#569613
  (backport qemu-kvm-0.12.3 fixes to RHEL6)

* Tue Apr 27 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.46.el6
- kvm-spice-add-auth-info-to-monitor-events.patch [bz#581540]
- Resolves: bz#581540
  (SPICE graphics event does not include auth details)

* Mon Apr 26 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.45.el6
- kvm-Documentation-Add-monitor-commands-to-function-index.patch [bz#559670]
- kvm-error-Put-error-definitions-back-in-alphabetical-ord.patch [bz#559670]
- kvm-error-New-QERR_DUPLICATE_ID.patch [bz#559670]
- kvm-error-Convert-qemu_opts_create-to-QError.patch [bz#559670]
- kvm-error-New-QERR_INVALID_PARAMETER_VALUE.patch [bz#559670]
- kvm-error-Convert-qemu_opts_set-to-QError.patch [bz#559670]
- kvm-error-Drop-extra-messages-after-qemu_opts_set-and-qe.patch [bz#559670]
- kvm-error-Use-QERR_INVALID_PARAMETER_VALUE-instead-of-QE.patch [bz#559670]
- kvm-error-Convert-qemu_opts_validate-to-QError.patch [bz#559670]
- kvm-error-Convert-net_client_init-to-QError.patch [bz#559670]
- kvm-error-New-QERR_DEVICE_IN_USE.patch [bz#559670]
- kvm-monitor-New-commands-netdev_add-netdev_del.patch [bz#559670]
- kvm-qdev-Convert-qdev_unplug-to-QError.patch [bz#582325]
- kvm-monitor-convert-do_device_del-to-QObject-QError.patch [bz#582325]
- kvm-block-Fix-error-code-in-multiwrite-for-immediate-fai.patch [bz#582575]
- kvm-block-Fix-multiwrite-memory-leak-in-error-case.patch [bz#582575]
- Resolves: bz#559670
  (No 'netdev_add' command in monitor)
- Resolves: bz#582325
  (QMP: device_del support)
- Resolves: bz#582575
  (Backport bdrv_aio_multiwrite fixes)

* Mon Apr 26 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.44.el6
- kvm-spice-add-more-config-options-readd.patch [bz#576561]
- BuildRequires spice-server-devel >= 0.4.2-10.el6 because of API changes
- Resolves: bz#576561
  (spice: add more config options)

* Mon Apr 26 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.43.el6
- kvm-qemu-option-Make-qemu_opts_foreach-accumulate-return.patch [bz#579470]
- kvm-qdev-Fix-exit-code-for-device.patch [bz#579470]
- kvm-qdev-Add-help-for-device-properties.patch [bz#579470]
- kvm-qdev-update-help-on-device.patch [bz#579470]
- kvm-qdev-Add-rudimentary-help-for-property-value.patch [bz#579470]
- kvm-qdev-Free-opts-on-failed-do_device_add.patch [bz#579470]
- kvm-qdev-Improve-diagnostics-for-bad-property-values.patch [bz#579470]
- kvm-qdev-Catch-attempt-to-attach-more-than-one-device-to.patch [bz#579470]
- kvm-usb-Remove-disabled-monitor_printf-in-usb_read_file.patch [bz#579470]
- kvm-savevm-Fix-loadvm-to-report-errors-to-stderr-not-the.patch [bz#579470]
- kvm-pc-Fix-error-reporting-for-boot-once.patch [bz#579470]
- kvm-pc-Factor-common-code-out-of-pc_boot_set-and-cmos_in.patch [bz#579470]
- kvm-tools-Remove-unused-cur_mon-from-qemu-tool.c.patch [bz#579470]
- kvm-monitor-Separate-default-monitor-and-current-monitor.patch [bz#579470]
- kvm-block-Simplify-usb_msd_initfn-test-for-can-read-bdrv.patch [bz#579470]
- kvm-monitor-Factor-monitor_set_error-out-of-qemu_error_i.patch [bz#579470]
- kvm-error-Move-qemu_error-friends-from-monitor.c-to-own-.patch [bz#579470]
- kvm-error-Simplify-error-sink-setup.patch [bz#579470]
- kvm-error-Move-qemu_error-friends-into-their-own-header.patch [bz#579470]
- kvm-error-New-error_printf-and-error_vprintf.patch [bz#579470]
- kvm-error-Don-t-abuse-qemu_error-for-non-error-in-qdev_d.patch [bz#579470]
- kvm-error-Don-t-abuse-qemu_error-for-non-error-in-qbus_f.patch [bz#579470]
- kvm-error-Don-t-abuse-qemu_error-for-non-error-in-scsi_h.patch [bz#579470]
- kvm-error-Replace-qemu_error-by-error_report.patch [bz#579470]
- kvm-error-Rename-qemu_error_new-to-qerror_report.patch [bz#579470]
- kvm-error-Infrastructure-to-track-locations-for-error-re.patch [bz#579470]
- kvm-error-Include-the-program-name-in-error-messages-to-.patch [bz#579470]
- kvm-error-Track-locations-in-configuration-files.patch [bz#579470]
- kvm-QemuOpts-Fix-qemu_config_parse-to-catch-file-read-er.patch [bz#579470]
- kvm-error-Track-locations-on-command-line.patch [bz#579470]
- kvm-qdev-Fix-device-and-device_add-to-handle-unsuitable-.patch [bz#579470]
- kvm-qdev-Factor-qdev_create_from_info-out-of-qdev_create.patch [bz#579470]
- kvm-qdev-Hide-no_user-devices-from-users.patch [bz#579470]
- kvm-qdev-Hide-ptr-properties-from-users.patch [bz#579470]
- kvm-monitor-New-monitor_cur_is_qmp.patch [bz#579470]
- kvm-error-Let-converted-handlers-print-in-human-monitor.patch [bz#579470]
- kvm-error-Polish-human-readable-error-descriptions.patch [bz#579470]
- kvm-error-New-QERR_PROPERTY_NOT_FOUND.patch [bz#579470]
- kvm-error-New-QERR_PROPERTY_VALUE_BAD.patch [bz#579470]
- kvm-error-New-QERR_PROPERTY_VALUE_IN_USE.patch [bz#579470]
- kvm-error-New-QERR_PROPERTY_VALUE_NOT_FOUND.patch [bz#579470]
- kvm-qdev-convert-setting-device-properties-to-QError.patch [bz#579470]
- kvm-qdev-Relax-parsing-of-bus-option.patch [bz#579470]
- kvm-error-New-QERR_BUS_NOT_FOUND.patch [bz#579470]
- kvm-error-New-QERR_DEVICE_MULTIPLE_BUSSES.patch [bz#579470]
- kvm-error-New-QERR_DEVICE_NO_BUS.patch [bz#579470]
- kvm-qdev-Convert-qbus_find-to-QError.patch [bz#579470]
- kvm-error-New-error_printf_unless_qmp.patch [bz#579470]
- kvm-error-New-QERR_BAD_BUS_FOR_DEVICE.patch [bz#579470]
- kvm-error-New-QERR_BUS_NO_HOTPLUG.patch [bz#579470]
- kvm-error-New-QERR_DEVICE_INIT_FAILED.patch [bz#579470]
- kvm-error-New-QERR_NO_BUS_FOR_DEVICE.patch [bz#579470]
- kvm-Revert-qdev-Use-QError-for-device-not-found-error.patch [bz#579470]
- kvm-error-Convert-do_device_add-to-QError.patch [bz#579470]
- kvm-qemu-option-Functions-to-convert-to-from-QDict.patch [bz#579470]
- kvm-qemu-option-Move-the-implied-first-name-into-QemuOpt.patch [bz#579470]
- kvm-qemu-option-Rename-find_list-to-qemu_find_opts-exter.patch [bz#579470]
- kvm-monitor-New-argument-type-O.patch [bz#579470]
- kvm-monitor-Use-argument-type-O-for-device_add.patch [bz#579470]
- kvm-monitor-convert-do_device_add-to-QObject.patch [bz#579470]
- kvm-error-Trim-includes-after-Move-qemu_error-friends.patch [bz#579470]
- kvm-error-Trim-includes-in-qerror.c.patch [bz#579470]
- kvm-error-Trim-includes-after-Infrastructure-to-track-lo.patch [bz#579470]
- kvm-error-Make-use-of-error_set_progname-optional.patch [bz#579470]
- kvm-error-Link-qemu-img-qemu-nbd-qemu-io-with-qemu-error.patch [bz#579470]
- kvm-error-Move-qerror_report-from-qemu-error.-ch-to-qerr.patch [bz#579470]
- Resolves: bz#579470
  (QMP: device_add support)

* Fri Apr 23 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.42.el6
- kvm-net-remove-NICInfo.bootable-field.patch [bz#561078]
- kvm-net-remove-broken-net_set_boot_mask-boot-device-vali.patch [bz#561078]
- kvm-boot-remove-unused-boot_devices_bitmap-variable.patch [bz#561078]
- kvm-check-kvm-enabled.patch [bz#580109]
- kvm-qemu-rename-notifier-event_notifier.patch [bz#580109]
- kvm-virtio-API-name-cleanup.patch [bz#580109]
- kvm-vhost-u_int64_t-uint64_t.patch [bz#580109]
- kvm-virtio-pci-fix-coding-style.patch [bz#580109]
- kvm-vhost-detect-lack-of-support-earlier-style.patch [bz#580109]
- kvm-configure-vhost-related-fixes.patch [bz#580109]
- kvm-vhost-fix-features-ack.patch [bz#580109]
- kvm-vhost-net-disable-mergeable-buffers.patch [bz#580109]
- Resolves: bz#561078
  ("Cannot boot from non-existent NIC" when using virt-install --pxe)
- Resolves: bz#580109
  (vhost net lacks upstream fixes)

* Thu Apr 22 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.41.el6
- Build fix: pass sysconfdir to 'make install'
- Related: bz#569661

* Tue Apr 20 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.40.el6
- cpu-model-config-1.patch [bz#569661]
- cpu-model-config-2.patch [bz#569661]
- cpu-model-config-3.patch [bz#569661]
- cpu-model-config-4.patch [bz#569661]
- Resolves: bz#569661
  (RHEL6.0 requires backport of upstream cpu model support..)

* Mon Apr 19 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.39.el6
- kvm-virtio-blk-revert-serial-number-support.patch [bz#564101]
- kvm-block-add-topology-qdev-properties.patch [bz#564101]
- kvm-virtio-blk-add-topology-support.patch [bz#564101]
- kvm-scsi-add-topology-support.patch [bz#564101]
- kvm-ide-add-topology-support.patch [bz#564101]
- kvm-pcnet-make-subsystem-vendor-id-match-hardware.patch [bz#580140]
- Resolves: bz#564101
  ([RFE] topology support in the virt block layer)
- Resolves: bz#580140
  (emulated pcnet nic in qemu-kvm has wrong PCI subsystem ID for Windows XP driver)

* Tue Apr 13 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.38.el6
- kvm-read-only-Make-CDROM-a-read-only-drive.patch [bz#537164]
- kvm-read-only-BDRV_O_FLAGS-cleanup.patch [bz#537164]
- kvm-read-only-Added-drives-readonly-option.patch [bz#537164]
- kvm-read-only-Disable-fall-back-to-read-only.patch [bz#537164]
- kvm-read-only-No-need-anymoe-for-bdrv_set_read_only.patch [bz#537164]
- kvm-read_only-Ask-for-read-write-permissions-when-openin.patch [bz#537164]
- kvm-read-only-Read-only-device-changed-to-opens-it-s-fil.patch [bz#537164]
- kvm-read-only-qemu-img-Fix-qemu-img-can-t-create-qcow-im.patch [bz#537164]
- kvm-block-clean-up-bdrv_open2-structure-a-bit.patch [bz#537164]
- kvm-block-saner-flags-filtering-in-bdrv_open2.patch [bz#537164]
- kvm-block-flush-backing_hd-in-the-right-place.patch [bz#537164]
- kvm-block-fix-cache-flushing-in-bdrv_commit.patch [bz#537164]
- kvm-block-more-read-only-changes-related-to-backing-file.patch [bz#537164]
- kvm-read-only-minor-cleanup.patch [bz#537164]
- kvm-read-only-Another-minor-cleanup.patch [bz#537164]
- kvm-read-only-allow-read-only-CDROM-with-any-interface.patch [bz#537164]
- kvm-qemu-img-rebase-Add-f-option.patch [bz#580028]
- kvm-qemu-io-Fix-return-value-handling-of-bdrv_open.patch [bz#579974]
- kvm-qemu-nbd-Fix-return-value-handling-of-bdrv_open.patch [bz#579974]
- kvm-qemu-img-Fix-error-message.patch [bz#579974]
- kvm-Replace-calls-of-old-bdrv_open.patch [bz#579974]
- Resolves: bz#537164
  (-drive arg has no way to request a read only disk)
- Resolves: bz#579974
  (Get segmentation fault when creating qcow2 format image on block device with "preallocation=metadata")
- Resolves: bz#580028
  ('qemu-img re-base' broken on block devices)

* Mon Apr 12 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.37.el6
- kvm-balloon-Fix-overflow-when-reporting-actual-memory-si.patch [bz#578912]
- kvm-json-parser-Output-the-content-of-invalid-keyword.patch [bz#576544]
- Resolves: bz#576544
  (Error message doesn't contain the content of invalid keyword)
- Resolves: bz#578912
  (Monitor: Overflow in 'info balloon')

* Wed Apr 07 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.36.el6
- kvm-char-Remove-redundant-qemu_chr_generic_open-call.patch [bz#558236]
- kvm-add-close-callback-for-tty-based-char-device.patch [bz#558236]
- kvm-Restore-terminal-attributes-for-tty-based-monitor.patch [bz#558236]
- kvm-Restore-terminal-monitor-attributes-addition.patch [bz#558236]
- Resolves: bz#558236
  (qemu-kvm monitor corrupts tty on exit)

* Tue Apr 06 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.35.el6
- kvm-QError-New-QERR_DEVICE_NOT_ENCRYPTED.patch [bz#563641]
- kvm-Wrong-error-message-in-block_passwd-command.patch [bz#563641]
- kvm-Monitor-Introduce-RFQDN_REDHAT-and-use-it.patch [bz#578493]
- kvm-QMP-Fix-Spice-event-names.patch [bz#578493]
- Resolves: bz#563641
  (QMP: Wrong error message in block_passwd command)
- Resolves: bz#578493
  (QMP: Fix spice event names)
- ksm.init: touch max_kernel_pages only if it exists [bz#561907]
- Resolves: bz#561907
- ksmtuned: add debug information [bz#576789]
- Resolves: bz#576789

* Tue Mar 30 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.34.el6
- kvm-Monitor-Introduce-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-simple-handlers-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-do_cont-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-do_eject-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-do_cpu_set-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-do_block_set_passwd-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-do_getfd-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-do_closefd-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-pci_device_hot_add-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-pci_device_hot_remove-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-do_migrate-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-do_memory_save-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-do_physical_memory_save-to-cmd_new_r.patch [bz#563491]
- kvm-Monitor-Convert-do_info-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-do_change-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-to-mon_set_password-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Convert-mon_spice_migrate-to-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Rename-cmd_new_ret.patch [bz#563491]
- kvm-Monitor-Debugging-support.patch [bz#563491]
- kvm-Monitor-Drop-the-print-disabling-mechanism.patch [bz#563491]
- kvm-Monitor-Audit-handler-return.patch [bz#563491]
- kvm-Monitor-Debug-stray-prints-the-right-way.patch [bz#563491]
- kvm-Monitor-Report-more-than-one-error-in-handlers.patch [bz#563491]
- Resolves: bz#563491
  (QMP: New internal error handling mechanism)

* Mon Mar 29 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.33.el6
- kvm-Fix-kvm_load_mpstate-for-vcpu-hot-add.patch [bz#569613]
- kvm-qemu-kvm-enable-get-set-vcpu-events-on-reset-and-mig.patch [bz#569613]
- kvm-Synchronize-kvm-headers.patch [bz#569613]
- kvm-Increase-VNC_MAX_WIDTH.patch [bz#569613]
- kvm-device-assignment-default-requires-IOMMU.patch [bz#569613]
- kvm-Do-not-allow-vcpu-stop-with-in-progress-PIO.patch [bz#569613]
- kvm-fix-savevm-command-without-id-or-tag.patch [bz#569613]
- kvm-Do-not-ignore-error-if-open-file-failed-serial-dev-t.patch [bz#569613]
- kvm-segfault-due-to-buffer-overrun-in-usb-serial.patch [bz#569613]
- kvm-fix-inet_parse-typo.patch [bz#569613]
- kvm-virtio-net-fix-network-stall-under-load.patch [bz#569613]
- kvm-don-t-dereference-NULL-after-failed-strdup.patch [bz#569613]
- kvm-net-Remove-unused-net_client_uninit.patch [bz#569613]
- kvm-net-net_check_clients-runs-too-early-to-see-device-f.patch [bz#569613]
- kvm-net-Fix-bogus-Warning-vlan-0-with-no-nics-with-devic.patch [bz#569613]
- kvm-net-net_check_clients-checks-only-VLAN-clients-fix.patch [bz#569613]
- kvm-net-info-network-shows-only-VLAN-clients-fix.patch [bz#569613]
- kvm-net-Monitor-command-set_link-finds-only-VLAN-clients.patch [bz#569613]
- kvm-ide-save-restore-pio-atapi-cmd-transfer-fields-and-i.patch [bz#569613]
- kvm-cirrus-Properly-re-register-cirrus_linear_io_addr-on.patch [bz#569613]
- Related: bz#569613
  (backport qemu-kvm-0.12.3 fixes to RHEL6)

* Fri Mar 26 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.32.el6
- kvm-Revert-spice-add-more-config-options.patch [bz#576561]
  (need to wait for spice patches to be included on spice-server)
- Related: bz#576561
  (spice: add more config options)

* Fri Mar 26 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.31.el6
- kvm-Transparent-Hugepage-Support-3.patch [bz#574525]
- kvm-monitor-Don-t-check-for-mon_get_cpu-failure.patch [bz#574642]
- kvm-QError-New-QERR_OPEN_FILE_FAILED.patch [bz#574642]
- kvm-monitor-convert-do_memory_save-to-QError.patch [bz#574642]
- kvm-monitor-convert-do_physical_memory_save-to-QError.patch [bz#574642]
- kvm-QError-New-QERR_INVALID_CPU_INDEX.patch [bz#574642]
- kvm-monitor-convert-do_cpu_set-to-QObject-QError.patch [bz#574642]
- kvm-monitor-Use-QERR_INVALID_PARAMETER-instead-of-QERR_I.patch [bz#575800]
- kvm-Revert-QError-New-QERR_INVALID_CPU_INDEX.patch [bz#575800]
- kvm-json-parser-Fix-segfault-on-malformed-input.patch [bz#575800]
- kvm-fix-i-format-handling-in-memory-dump.patch [bz#575800]
- kvm-Don-t-set-default-monitor-when-there-is-a-mux-ed-one.patch [bz#575800]
- kvm-monitor-Document-argument-type-M.patch [bz#575821]
- kvm-QDict-New-qdict_get_double.patch [bz#575821]
- kvm-monitor-New-argument-type-b.patch [bz#575821]
- kvm-monitor-Use-argument-type-b-for-migrate_set_speed.patch [bz#575821]
- kvm-monitor-convert-do_migrate_set_speed-to-QObject.patch [bz#575821]
- kvm-monitor-New-argument-type-T.patch [bz#575821]
- kvm-monitor-Use-argument-type-T-for-migrate_set_downtime.patch [bz#575821]
- kvm-monitor-convert-do_migrate_set_downtime-to-QObject.patch [bz#575821]
- kvm-block-Emit-BLOCK_IO_ERROR-before-vm_stop-call.patch [bz#575912]
- kvm-QMP-Move-STOP-event-into-do_vm_stop.patch [bz#575912]
- kvm-QMP-Move-RESET-event-into-qemu_system_reset.patch [bz#575912]
- kvm-QMP-Sync-with-upstream-event-changes.patch [bz#575912]
- kvm-QMP-Drop-DEBUG-event.patch [bz#575912]
- kvm-QMP-Revamp-the-qmp-events.txt-file.patch [bz#575912]
- kvm-QMP-Introduce-RTC_CHANGE-event.patch [bz#547534]
- kvm-QMP-Introduce-WATCHDOG-event.patch [bz#557083]
- kvm-spice-add-more-config-options.patch [bz#576561]
- Resolves: bz#547534
  (RFE: a QMP event notification for RTC clock changes)
- Resolves: bz#557083
  (QMP events for watchdog events)
- Resolves: bz#574525
  (Align qemu-kvm guest memory for transparent hugepage support)
- Resolves: bz#574642
  (QMP: Convert do_cpu_set() to QObject)
- Resolves: bz#575800
  (Monitor: Backport a collection of fixes)
- Resolves: bz#575821
  (QMP: Convert migrate_set_speed, migrate_set_downtime to QObject)
- Resolves: bz#575912
  (QMP: Backport event related fixes)
- Resolves: bz#576561
  (spice: add more config options)

* Thu Mar 25 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.30.el6
- kvm-New-API-for-asynchronous-monitor-commands.patch [bz#574939]
- kvm-Revert-QMP-Fix-query-balloon-key-change.patch [bz#574939]
- kvm-virtio-Add-memory-statistics-reporting-to-the-balloo.patch [bz#574939]
- Resolves: bz#574939
  (Memory statistics support)

* Wed Mar 24 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.29.el6
- kvm-scsi-device-version-property.patch [bz#558835]
- kvm-scsi-disk-fix-buffer-overflow.patch [bz#558835]
- Resolves: bz#558835
  (ide/scsi drive versions)

* Wed Mar 24 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.28.el6
- kvm-qcow2-Factor-next_refcount_table_size-out.patch [bz#567940]
- kvm-qcow2-Rewrite-alloc_refcount_block-grow_refcount_tab.patch [bz#567940]
- kvm-qcow2-More-checks-for-qemu-img-check.patch [bz#567940]
- kvm-spice-virtual-machine-channel-replacement-for-remove.patch [bz#576488]
- Resolves: bz#567940
  (qcow2 corruption with I/O error during refcount block allocation)
- Resolves: bz#576488
  (Spice: virtio serial based device for guest-spice client communication)

* Wed Mar 24 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.27.el6
- kvm-spice-add-tablet.patch [bz#574211]
- kvm-spice-simple-display-wake-spice-server-only-when-idl.patch [bz#574212]
- kvm-spice-qxl-switch-back-to-vga-mode-on-register-access.patch [bz#574214]
- kvm-spice-qxl-ring-access-security-fix.patch [bz#568820]
- kvm-vnc-support-password-expire.patch [bz#525935]
- kvm-spice-vnc-add-__com.redhat_set_password-monitor-comm.patch [bz#525935]
- kvm-spice-add-audio-support.patch [bz#574222]
- kvm-spice-make-image-compression-configurable.patch [bz#574225]
- kvm-spice-configure-channel-security.patch [bz#574225]
- kvm-spice-configure-renderer.patch [bz#574225]
- kvm-spice-send-connect-disconnect-monitor-events.patch [bz#558957]
- kvm-spice-qxl-update-vga-help-text-indicating-qxl-is-the.patch [bz#574853]
- kvm-spice-notifying-spice-when-migration-starts-and-ends.patch [bz#574849]
- kvm-spice-add-__com.redhat_spice_migrate_info-monitor-co.patch [bz#574849]
- Resolves: bz#525935
  (RFE: expire vnc password)
- Resolves: bz#558957
  (A QMP event notification on SPICE client connect/disconnect events)
- Resolves: bz#568820
  (EMBARGOED CVE-2010-0431 qemu: Insufficient guest provided pointers validation [rhel-6.0])
- Resolves: bz#574211
  (spice: add tablet support)
- Resolves: bz#574212
  (spice:wake spice server only when idle)
- Resolves: bz#574214
  (qxl: switch qxl from native into vga mode on vga register access)
- Resolves: bz#574222
  (spice: add audio support)
- Resolves: bz#574225
  (spice: add config options)
- Resolves: bz#574849
  (spice: client migration support)
- Resolves: bz#574853
  (spice/qxl: add qxl to -vga help text)

* Thu Mar 18 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.26.el6
- kvm-add-spice-into-the-configure-file.patch [bz#549757]
- kvm-spice-core-bits.patch [bz#549757]
- kvm-spice-add-keyboard.patch [bz#549757]
- kvm-spice-add-mouse.patch [bz#549757]
- kvm-spice-simple-display.patch [bz#549757]
- kvm-move-x509-file-name-defines-to-qemu-x509.h.patch [bz#549757]
- kvm-spice-tls-support.patch [bz#549757]
- kvm-spice-configure-listening-addr.patch [bz#549757]
- kvm-spice-add-qxl-device.patch [bz#549757]
- Resolves: bz#549757
  (Provide SPICE support  / -spice command line argument)

* Wed Mar 17 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.25.el6
- kvm-qemu-memory-notifiers.patch [bz#562958]
- kvm-tap-add-interface-to-get-device-fd.patch [bz#562958]
- kvm-add-API-to-set-ioeventfd.patch [bz#562958]
- kvm-notifier-event-notifier-implementation.patch [bz#562958]
- kvm-virtio-add-notifier-support.patch [bz#562958]
- kvm-virtio-add-APIs-for-queue-fields.patch [bz#562958]
- kvm-virtio-add-set_status-callback.patch [bz#562958]
- kvm-virtio-move-typedef-to-qemu-common.patch [bz#562958]
- kvm-virtio-pci-fill-in-notifier-support.patch [bz#562958]
- kvm-vhost-vhost-net-support.patch [bz#562958]
- kvm-tap-add-vhost-vhostfd-options.patch [bz#562958]
- kvm-tap-add-API-to-retrieve-vhost-net-header.patch [bz#562958]
- kvm-virtio-net-vhost-net-support.patch [bz#562958]
- kvm-qemu-kvm-add-vhost.h-header.patch [bz#562958]
- kvm-irqfd-support.patch [bz#562958]
- kvm-msix-add-mask-unmask-notifiers.patch [bz#562958]
- kvm-virtio-pci-irqfd-support.patch [bz#562958]
- Resolves: bz#562958
  (RFE: Support vhost net mode)

* Fri Mar 12 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.24.el6
- kvm-path.c-fix-warning-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-hw-pc.c-fix-warnings-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-slirp-misc.c-fix-warning-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-savevm.c-fix-warning-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-block-bochs.c-fix-warning-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-block.c-fix-warning-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-Introduce-qemu_write_full.patch [bz#567099]
- kvm-force-to-test-result-for-qemu_write_full.patch [bz#567099]
- kvm-block-cow.c-fix-warnings-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-block-qcow.c-fix-warnings-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-block-vmdk.o-fix-warnings-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-block-vvfat.c-fix-warnings-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-block-qcow2.c-fix-warnings-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-net-slirp.c-fix-warning-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-usb-linux.c-fix-warning-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-vl.c-fix-warning-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-monitor.c-fix-warnings-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-linux-user-mmap.c-fix-warnings-with-_FORTIFY_SOURCE.patch [bz#567099]
- kvm-check-pipe-return-value.patch [bz#567099]
- kvm-fix-qemu-kvm-_FORTIFY_SOURCE-compilation.patch [bz#567099]
- kvm-Enable-_FORTIFY_SOURCE-2.patch [bz#567099]
- kvm-qcow2-Fix-image-creation-regression.patch [bz#567099]
- kvm-cow-return-errno-instead-of-1.patch [bz#567099]
- kvm-slirp-check-system-success.patch [bz#567099]
- kvm-qcow2-return-errno-instead-of-1.patch [bz#567099]
- kvm-qcow-return-errno-instead-of-1.patch [bz#567099]
- kvm-vmdk-return-errno-instead-of-1.patch [bz#567099]
- kvm-vmdk-make-vmdk_snapshot_create-return-errno.patch [bz#567099]
- kvm-vmdk-fix-double-free.patch [bz#567099]
- kvm-vmdk-share-cleanup-code.patch [bz#567099]
- kvm-block-print-errno-on-error.patch [bz#567099]
- kvm-documentation-qemu_write_full-don-t-work-with-non-bl.patch [bz#567099]
- kvm-virtio-serial-pci-Allow-MSI-to-be-disabled.patch [bz#567035]
- kvm-pc-Add-backward-compatibility-options-for-virtio-ser.patch [bz#567035]
- kvm-virtio-serial-don-t-set-MULTIPORT-for-1-port-dev.patch [bz#567035]
- kvm-qdev-Add-a-DEV_NVECTORS_UNSPECIFIED-enum-for-unspeci.patch [bz#567035]
- kvm-virtio-pci-Use-DEV_NVECTORS_UNSPECIFIED-instead-of-1.patch [bz#567035]
- kvm-kbd-leds-infrastructure.patch [bz#569767]
- kvm-kbd-leds-ps-2-kbd.patch [bz#569767]
- kvm-kbd-leds-usb-kbd.patch [bz#569767]
- kvm-kbd-keds-vnc.patch [bz#569767]
- kvm-migration-Clear-fd-also-in-error-cases.patch [bz#570174]
- Resolves: bz#567035
  (Backport changes for virtio-serial from upstream: disabling MSI, backward compat.)
- Resolves: bz#567099
  (Allow _FORTIFY_SOURCE=2 & --enable-warning)
- Resolves: bz#569767
  (Caps Lock the key's appearance  of guest is not synchronous as host's --view kvm with vnc)
- Resolves: bz#570174
  (Restoring a qemu guest from a saved state file using -incoming sometimes fails and hangs)

* Tue Mar 02 2010 Glauber Costa <glommer@redhat.com> - qemu-kvm-0.12.1.2-2.23.el6
- kvm-ide-device-version-property.patch [bz#558835]
- kvm-pc-add-driver-version-compat-properties.patch [bz#558835]
- kvm-qemu-img-Fix-segfault-during-rebase.patch [bz#567602]
- Resolves: bz#558835
  (ide/scsi drive versions)
- Resolves: bz#567602
  (qemu-img rebase subcommand got Segmentation fault)

* Mon Mar 01 2010 Glauber Costa <glommer@redhat.com> - qemu-kvm-0.12.1.2-2.22.el6
- kvm-QMP-BLOCK_IO_ERROR-event-handling.patch [bz#547501]
- kvm-block-BLOCK_IO_ERROR-QMP-event.patch [bz#547501]
- kvm-ide-Generate-BLOCK_IO_ERROR-QMP-event.patch [bz#547501]
- kvm-scsi-Generate-BLOCK_IO_ERROR-QMP-event.patch [bz#547501]
- kvm-virtio-blk-Generate-BLOCK_IO_ERROR-QMP-event.patch [bz#547501]
- kvm-add-rhel-machine-types.patch [bz#558838]
- kvm-QMP-Fix-query-balloon-key-change.patch [bz#568739]
- Resolves: bz#547501
  (RFE: a QMP event notification for disk  I/O errors with werror/rerror flags)
- Resolves: bz#558838
  (add rhel machine types)
- Resolves: bz#568739
  (QMP: Fix 'query-balloon' key)

* Fri Feb 26 2010 Glauber Costa <glommer@redhat.com> - qemu-kvm-0.12.1.2-2.21.el6
- kvm-net-add-API-to-disable-enable-polling.patch [bz#562958]
- kvm-virtio-rename-features-guest_features.patch [bz#562958]
- kvm-qdev-add-bit-property-type.patch [bz#562958]
- kvm-qdev-fix-thinko-leading-to-guest-crashes.patch [bz#562958]
- kvm-virtio-add-features-as-qdev-properties-fixup.patch [bz#562958]
- Resolves: bz#562958
  (RFE: Support vhost net mode)

* Fri Feb 26 2010 Glauber Costa <glommer@redhat.com> - qemu-kvm-0.12.1.2-2.20.el6
- kvm-QMP-Add-QEMU-s-version-to-the-greeting-message.patch [bz#557930]
- kvm-QMP-Introduce-the-qmp_capabilities-command.patch [bz#557930]
- kvm-QMP-Enforce-capability-negotiation-rules.patch [bz#557930]
- kvm-QMP-spec-Capability-negotiation-updates.patch [bz#557930]
- kvm-json-escape-u0000-.-u001F-when-outputting-json.patch [bz#559667]
- kvm-json-fix-PRId64-on-Win32.patch [bz#563878]
- kvm-qjson-Improve-debugging.patch [bz#563875]
- kvm-Monitor-remove-unneeded-checks.patch [bz#563876]
- kvm-QError-Don-t-abort-on-multiple-faults.patch [bz#559635]
- kvm-QMP-Don-t-leak-on-connection-close.patch [bz#559645]
- kvm-QMP-Emit-Basic-events.patch [bz#558623]
- Resolves: bz#557930
  (QMP: Feature Negotiation support)
- Resolves: bz#558623
  (QMP: Basic async events are not emitted)
- Resolves: bz#559635
  (QMP: assertion on multiple faults)
- Resolves: bz#559645
  (QMP: leak when a QMP connection is closed)
- Resolves: bz#559667
  (QMP: JSON parser doesn't escape some control chars)
- Resolves: bz#563875
  (QJSON: Improve debugging)
- Resolves: bz#563876
  (Monitor: remove unneeded checks)
- Resolves: bz#563878
  (QJSON: Fix PRId64 handling)

* Fri Feb 19 2010 Glauber Costa <glommer@redhat.com> - qemu-kvm-0.12.1.2-2.19.el6
- kvm-virtio_blk-Factor-virtio_blk_handle_request-out.patch [bz#560942]
- kvm-virtio-blk-Fix-restart-after-read-error.patch [bz#560942]
- kvm-virtio-blk-Fix-error-cases-which-ignored-rerror-werr.patch [bz#560942]
- Resolves: bz#560942
  (virtio-blk error handling doesn't work reliably)

* Thu Feb 11 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.18.el6
- kvm-roms-minor-fixes-and-cleanups.patch [bz#558818]
- kvm-fw_cfg-rom-loader-tweaks.patch [bz#558818]
- kvm-roms-rework-rom-loading-via-fw.patch [bz#558818]
- kvm-pci-allow-loading-roms-via-fw_cfg.patch [bz#558818]
- kvm-pc-add-rombar-to-compat-properties-for-pc-0.10-and-p.patch [bz#558818]
- Resolves: bz#558818
  (rom loading)

* Wed Feb 10 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.17.el6
- kvm-Fix-QEMU_WARN_UNUSED_RESULT.patch [bz#560623]
- kvm-qcow2-Fix-error-handling-in-qcow2_grow_l1_table.patch [bz#560623]
- kvm-qcow2-Fix-error-handling-in-qcow_save_vmstate.patch [bz#560623]
- kvm-qcow2-Return-0-errno-in-get_cluster_table.patch [bz#560623]
- kvm-qcow2-Return-0-errno-in-qcow2_alloc_cluster_offset.patch [bz#560623]
- kvm-block-Return-original-error-codes-in-bdrv_pread-writ.patch [bz#560623]
- kvm-qcow2-Fix-error-handling-in-grow_refcount_table.patch [bz#560623]
- kvm-qcow2-Improve-error-handling-in-update_refcount.patch [bz#560623]
- kvm-qcow2-Allow-updating-no-refcounts.patch [bz#560623]
- kvm-qcow2-Don-t-ignore-update_refcount-return-value.patch [bz#560623]
- kvm-qcow2-Don-t-ignore-qcow2_alloc_clusters-return-value.patch [bz#560623]
- kvm-net-Make-inet_strfamily-public.patch [bz#562181]
- kvm-net-inet_strfamily-Better-unknown-family-report.patch [bz#562181]
- kvm-vnc-Use-inet_strfamily.patch [bz#562181]
- Resolves: bz#560623
  (error codes aren't always propagated up through the block layer (e.g. -ENOSPC))
- Resolves: bz#562181
  (Small VNC related cleanup)

* Mon Feb 08 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.16.el6
- Move /usr/bin/qemu-kvm to /usr/libexec/qemu-kvm
- Resolves: bz#560651

* Wed Feb 03 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.15.el6
- kvm-VNC-Use-enabled-key-instead-of-status.patch [bz#549759]
- kvm-VNC-Make-auth-key-mandatory.patch [bz#549759]
- kvm-VNC-Rename-client-s-username-key.patch [bz#549759]
- kvm-VNC-Add-family-key.patch [bz#549759]
- kvm-VNC-Cache-client-info-at-connection-time.patch [bz#549759]
- kvm-QMP-Introduce-VNC_CONNECTED-event.patch [bz#549759]
- kvm-QMP-Introduce-VNC_DISCONNECTED-event.patch [bz#549759]
- kvm-QMP-Introduce-VNC_INITIALIZED-event.patch [bz#549759]
- kvm-block-avoid-creating-too-large-iovecs-in-multiwrite_.patch [bz#558730]
- Resolves: bz#549759
  (A QMP event notification on VNC client connect/disconnect events)
- Resolves: bz#558730
  (qemu may create too large iovecs for the kernel)

* Thu Jan 28 2010 Glauber Costa <glommer@redhat.com> - qemu-kvm-0.12.1.2-2.14.el6
- kvm-MCE-Fix-bug-of-IA32_MCG_STATUS-after-system-reset.patch [bz#558416]
- kvm-Fix-CPU-topology-initialization.patch [bz#558432]
- kvm-loader-more-ignores-for-rom-intended-to-be-loaded-by.patch [bz#558467]
- kvm-pc-add-machine-type-for-0.12.patch [bz#558470]
- kvm-virtio-console-Rename-virtio-serial.c-back-to-virtio.patch [bz#559089]
- kvm-virtio-serial-bus-Fix-bus-initialisation-and-allow-f.patch [bz#559503]
- Resolves: bz#558416
  (Machine check exception injected into qemu reinjected after every reset)
- Resolves: bz#558432
  (CPU topology not taking effect)
- Resolves: bz#558467
  (roms potentially loaded twice)
- Resolves: bz#558470
  (Incorrect machine types)
- Resolves: bz#559089
  (Rename virtio-serial.c to virtio-console.c as is upstream.)
- Resolves: bz#559503
  (virtio-serial: fix multiple devices intialisation)

* Wed Jan 27 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.13.el6
- kvm-reduce-number-of-reinjects-on-ACK.patch [bz#557435]
- kvm-Add-missing-newline-at-the-end-of-options-list.patch [bz#558412]
- kvm-vnc-Fix-artifacts-in-hextile-decoding.patch [bz#558414]
- kvm-QMP-Drop-wrong-assert.patch [bz#558415]
- kvm-vmware_vga-Check-cursor-dimensions-passed-from-guest.patch [bz#558435]
- kvm-virtio-pci-thinko-fix.patch [bz#558438]
- kvm-QMP-Don-t-free-async-event-s-data.patch [bz#558465]
- kvm-vnc_refresh-return-if-vd-timer-is-NULL.patch [bz#558466]
- kvm-osdep.c-Fix-accept4-fallback.patch [bz#558477]
- kvm-QMP-Emit-asynchronous-events-on-all-QMP-monitors.patch [bz#558619]
- kvm-vnc_refresh-calling-vnc_update_client-might-free-vs.patch [bz#558846]
- Resolves: bz#557435
  (KVM: WIN7-32bit blue screen (IMAGE_NAME:  ntkrnlmp.exe).)
- Resolves: bz#558412
  (-help output not terminated by newline)
- Resolves: bz#558414
  (Artifacts in hextile decoding)
- Resolves: bz#558415
  (Assert triggers on qmp commands returning lists)
- Resolves: bz#558435
  (vmware-svga buffer overflow copying cursor data)
- Resolves: bz#558438
  (virtio status bits corrupted if guest deasserts bus mastering bit)
- Resolves: bz#558465
  (Double-free of qmp async messages)
- Resolves: bz#558466
  (Possible segfault on vnc client disconnect)
- Resolves: bz#558477
  (Incorrect handling of EINVAL from accept4())
- Resolves: bz#558619
  (QMP: Emit asynchronous events on all QMP monitors)
- Resolves: bz#558846
  (fix use-after-free in vnc code)

* Fri Jan 22 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.12.el6
- kvm-virtio-serial-bus-Remove-guest-buffer-caching-and-th.patch [bz#543825]
- kvm-virtio-serial-Make-sure-we-don-t-crash-when-host-por.patch [bz#543825]
- kvm-virtio-serial-Use-MSI-vectors-for-port-virtqueues.patch [bz#543825]
- kvm-virtio-serial-bus-Match-upstream-whitespace.patch [bz#543825]
- Resolves: bz#543825
  ([RFE] Backport virtio-serial device to qemu)

* Mon Jan 18 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.11.el6
- kvm-block-Introduce-BDRV_O_NO_BACKING.patch [bz#556459]
- kvm-block-Add-bdrv_change_backing_file.patch [bz#556459]
- kvm-qemu-img-rebase.patch [bz#556459]
- Resolves: bz#556459
  (RFE - In-place backing file format change)

* Mon Jan 18 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.10.el6
- Conflicts with older vdsm version, that needs vvfat support
- Related: bz#555336

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.9.el6
- Disable -Werror again, as there are still warnings on the build
- Related: bz#555336
  (Remove unneeded features)

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.8.el6
- Require libaio-devel for build
- Related: bz#555336
  (Remove unneeded features)

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.7.el6
- Disable vvfat support
- Resolves: bz#555336
  (Remove unneeded features)

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.6.el6
- Fix misapply of virtio patches
- Related: bz#543825

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.5.el6
- Remove unneeded/unsupported features: [bz#555336]
  - make default options explicit
  - remove sdl support
  - remove sb16 emulation
  - remove oss support
  - remove curses support
  - disable curl support
  - disable bluez support
  - enable -Werror
  - limit block drivers support
  - add host_cdrom block device
- Resolves: bz#555336
  (Remove unneeded features)

* Fri Jan 15 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.4.el6
- kvm-virtio-Remove-duplicate-macro-definition-for-max.-vi.patch [bz#543825]
- kvm-virtio-console-qdev-conversion-new-virtio-serial-bus.patch [bz#543825]
- kvm-virtio-serial-bus-Maintain-guest-and-host-port-open-.patch [bz#543825]
- kvm-virtio-serial-bus-Add-a-port-name-property-for-port-.patch [bz#543825]
- kvm-virtio-serial-bus-Add-support-for-buffering-guest-ou.patch [bz#543825]
- kvm-virtio-serial-bus-Add-ability-to-hot-unplug-ports.patch [bz#543825]
- kvm-virtio-serial-Add-a-virtserialport-device-for-generi.patch [bz#543825]
- kvm-Move-virtio-serial-to-Makefile.hw.patch [bz#543825]
- Resolves: bz#543825
  ([RFE] Backport virtio-serial device to qemu)

* Tue Jan 12 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.3.el6
- Use seabios instead of bochs-bios
- Resolves: bz#553732

* Tue Jan 12 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.2.el6
- Build only on x86_64
- Resolves: bz#538039

* Thu Jan 07 2010 Eduardo Habkost <ehabkost@redhat.com> - qemu-kvm-0.12.1.2-2.1.el6
- Rebasing to 0.12.1.2-2.fc13
- Resolves: bz#553271

* Tue Dec 08 2009 Dennis Gregorovic <dgregor@redhat.com> - 2:0.11.0-7.1
- Rebuilt for RHEL 6

* Mon Oct 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-7.el6
- Initial RHEL6 qemu-kvm package
