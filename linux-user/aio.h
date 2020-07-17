#ifndef LINUX_USER_AIO_H
#define LINUX_USER_AIO_H

#include <linux/aio_abi.h>

struct target_io_event {
    uint64_t data;
    uint64_t obj;
    int64_t  res;
    int64_t  res2;
};

struct qemu_internal_io_data {
    uint64_t orig_data;
    uint64_t orig_obj;
    uint64_t orig_buf;
};

struct target_iocb {
    uint64_t   aio_data;
#if defined(TARGET_WORDS_BIGENDIAN)
    abi_int    aio_rw_flags;
    uint32_t   aio_key;
#else
    uint32_t   aio_key;
    abi_int    aio_rw_flags;
#endif
    uint16_t   aio_lio_opcode;
    int16_t    aio_reqprio;
    uint32_t   aio_fildes;
    uint64_t   aio_buf;
    uint64_t   aio_nbytes;
    int64_t    aio_offset;
    uint64_t   aio_reserved2;
    uint32_t   aio_flags;
    uint32_t   aio_resfd;
};

struct iocb *target_find_host_iocb(abi_long target_iocb);
int target_to_host_iocb_array(struct iocb **iocbpp, abi_long *target_addr,
                              abi_long nr);
struct iocb *host_to_target_io_event(struct target_io_event *target_event,
                                     struct io_event *host_event);
void host_to_target_io_events(struct target_io_event *target_result,
                              struct io_event *host_result, long nr);
#endif /* LINUX_USER_AIO_H */
