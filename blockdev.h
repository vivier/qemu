/*
 * QEMU host block devices
 *
 * Copyright (c) 2003-2008 Fabrice Bellard
 *
 * This work is licensed under the terms of the GNU GPL, version 2 or
 * later.  See the COPYING file in the top-level directory.
 */

#ifndef BLOCKDEV_H
#define BLOCKDEV_H

#include "block.h"
#include "qemu-queue.h"

void blockdev_mark_auto_del(BlockDriverState *bs);
void blockdev_auto_del(BlockDriverState *bs);

#define BLOCK_SERIAL_STRLEN 20

typedef enum {
    IF_NONE,
    IF_IDE, IF_SCSI, IF_FLOPPY, IF_PFLASH, IF_MTD, IF_SD, IF_VIRTIO, IF_XEN,
    IF_COUNT
} BlockInterfaceType;

typedef struct DriveInfo {
    BlockDriverState *bdrv;
    char *id;
    const char *devaddr;
    BlockInterfaceType type;
    int bus;
    int unit;
    int auto_del;               /* see blockdev_mark_auto_del() */
    QemuOpts *opts;
    char serial[BLOCK_SERIAL_STRLEN + 1];
    QTAILQ_ENTRY(DriveInfo) next;
    int opened;
    int bdrv_flags;
    char *file;
    BlockDriver *drv;
} DriveInfo;

#define MAX_IDE_DEVS	2
#define MAX_SCSI_DEVS	7

extern QTAILQ_HEAD(drivelist, DriveInfo) drives;
extern QTAILQ_HEAD(driveoptlist, DriveOpt) driveopts;
extern DriveInfo *extboot_drive;

extern DriveInfo *drive_get(BlockInterfaceType type, int bus, int unit);
extern DriveInfo *drive_get_by_id(const char *id);
extern int drive_get_max_bus(BlockInterfaceType type);
extern void drive_uninit(DriveInfo *dinfo);
extern DriveInfo *drive_get_by_blockdev(BlockDriverState *bs);
extern const char *drive_get_serial(BlockDriverState *bdrv);

extern QemuOpts *drive_add(const char *file, const char *fmt, ...);
extern DriveInfo *drive_init(QemuOpts *arg, int default_to_scsi,
                             int *fatal_error);

extern int drives_reopen(void);

/* device-hotplug */

DriveInfo *add_init_drive(const char *opts);

void do_commit(Monitor *mon, const QDict *qdict);
int do_eject(Monitor *mon, const QDict *qdict, QObject **ret_data);
int do_block_set_passwd(Monitor *mon, const QDict *qdict, QObject **ret_data);
int do_change_block(Monitor *mon, const char *device,
                    const char *filename, const char *fmt);
int simple_drive_add(Monitor *mon, const QDict *qdict, QObject **ret_data);
int do_drive_del(Monitor *mon, const QDict *qdict, QObject **ret_data);

#endif
