Summary: Userspace component of KVM
Name: qemu-kvm
Version: 0.12.1.2
Release: 2.52%{?dist}
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
such as kvmtrace and kvm_stat.

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

%build
# --build-id option is used fedora 8 onwards for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# sdl outputs to alsa or pulseaudio depending on system config, but it's broken (#495964)
# alsa works, but causes huge CPU load due to bugs
# oss works, but is very problematic because it grabs exclusive control of the device causing other apps to go haywire
./configure --target-list=x86_64-softmmu \
            --prefix=%{_prefix} \
            --audio-drv-list=pa,alsa \
            --audio-card-list=ac97,es1370 \
            --disable-strip \
            --extra-ldflags=$extraldflags \
            --extra-cflags="$RPM_OPT_FLAGS" \
            --disable-xen \
            --block-drv-whitelist=qcow2,raw,host_device,host_cdrom \
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

cd kvm/user
./configure --prefix=%{_prefix} --kerneldir=$(pwd)/../kernel/
make kvmtrace
cd ../../

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

install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/kvm.modules
install -m 0755 kvm/user/kvmtrace $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 kvm/user/kvmtrace_format $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d

make prefix="${RPM_BUILD_ROOT}%{_prefix}" \
     bindir="${RPM_BUILD_ROOT}%{_bindir}" \
     sharedir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" \
     mandir="${RPM_BUILD_ROOT}%{_mandir}" \
     docdir="${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}" \
     datadir="${RPM_BUILD_ROOT}%{_datadir}/%{name}" \
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
%{_sysconfdir}/qemu/target-x86_64.conf

%files tools
%defattr(-,root,root,-)
%{_bindir}/kvmtrace
%{_bindir}/kvmtrace_format
%{_bindir}/kvm_stat

%files -n qemu-img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_mandir}/man1/qemu-img.1*

%changelog
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
