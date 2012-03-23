/*
 * Human Monitor Interface
 *
 * Copyright IBM, Corp. 2011
 *
 * Authors:
 *  Anthony Liguori   <aliguori@us.ibm.com>
 *
 * This work is licensed under the terms of the GNU GPL, version 2.  See
 * the COPYING file in the top-level directory.
 *
 */

#include "hmp.h"
#include "qmp-commands.h"

#ifdef CONFIG_LIVE_SNAPSHOTS
static void hmp_handle_error(Monitor *mon, Error **errp)
{
    if (error_is_set(errp)) {
        monitor_printf(mon, "%s\n", error_get_pretty(*errp));
        error_free(*errp);
    }
}

void hmp_snapshot_blkdev(Monitor *mon, const QDict *qdict)
{
    const char *device = qdict_get_str(qdict, "device");
    const char *filename = qdict_get_try_str(qdict, "snapshot-file");
    const char *format = qdict_get_try_str(qdict, "format");
    Error *errp = NULL;

    if (!filename) {
        /* In the future, if 'snapshot-file' is not specified, the snapshot
           will be taken internally. Today it's actually required. */
        error_set(&errp, QERR_MISSING_PARAMETER, "snapshot-file");
        hmp_handle_error(mon, &errp);
        return;
    }

    qmp_blockdev_snapshot_sync(device, filename, !!format, format, &errp);
    hmp_handle_error(mon, &errp);
}
#endif
