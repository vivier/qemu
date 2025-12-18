#include "qemu/osdep.h"
#include "qapi/qapi-commands-machine.h"
#include "qemu/uuid.h"

UuidInfo *qmp_query_uuid(Error **errp)
{
    UuidInfo *info = g_new0(UuidInfo, 1);

    info->UUID = g_strdup(UUID_NONE);
    return info;
}

