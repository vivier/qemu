/*
 * QEMU dump
 *
 * Copyright Fujitsu, Corp. 2011, 2012
 *
 * Authors:
 *     Wen Congyang <wency@cn.fujitsu.com>
 *
 * This work is licensed under the terms of the GNU GPL, version 2. See
 * the COPYING file in the top-level directory.
 *
 */

#ifndef DUMP_H
#define DUMP_H

#define MAKEDUMPFILE_SIGNATURE      "makedumpfile"
#define MAX_SIZE_MDF_HEADER         (4096) /* max size of makedumpfile_header */
#define TYPE_FLAT_HEADER            (1)    /* type of flattened format */
#define VERSION_FLAT_HEADER         (1)    /* version of flattened format */
#define END_FLAG_FLAT_HEADER        (-1)

typedef struct ArchDumpInfo {
    int d_machine;  /* Architecture */
    int d_endian;   /* ELFDATA2LSB or ELFDATA2MSB */
    int d_class;    /* ELFCLASS32 or ELFCLASS64 */
} ArchDumpInfo;

typedef struct QEMU_PACKED MakedumpfileHeader {
    char signature[16];     /* = "makedumpfile" */
    int64_t type;
    int64_t version;
} MakedumpfileHeader;

typedef struct QEMU_PACKED MakedumpfileDataHeader {
    int64_t offset;
    int64_t buf_size;
} MakedumpfileDataHeader;

#endif
