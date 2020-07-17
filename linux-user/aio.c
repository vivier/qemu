#include "qemu/osdep.h"
#include "qemu.h"
#include "aio.h"

static void host_iocb_free(struct iocb *iocb)
{
    g_free((void *)iocb->aio_data);
    g_free(iocb);
}

static int target_to_host_iocb(struct iocb *host_iocb, abi_long target_addr)
{
    struct qemu_internal_io_data *data;
    struct target_iocb *target_iocb;

    if (!lock_user_struct(VERIFY_WRITE, target_iocb, target_addr, 1)) {
        return -TARGET_EFAULT;
    }

    data = g_new(struct qemu_internal_io_data, 1);
    data->orig_obj = target_addr;
    __get_user(data->orig_data, &target_iocb->aio_data);
    __get_user(data->orig_buf, &target_iocb->aio_buf);

    host_iocb->aio_data = (uint64_t)data;

    __get_user(host_iocb->aio_nbytes, &target_iocb->aio_nbytes);
    __get_user(host_iocb->aio_key , &target_iocb->aio_key);
    __get_user(host_iocb->aio_rw_flags, &target_iocb->aio_rw_flags);
    __get_user(host_iocb->aio_lio_opcode, &target_iocb->aio_lio_opcode);
    __get_user(host_iocb->aio_reqprio, &target_iocb->aio_reqprio);
    __get_user(host_iocb->aio_fildes, &target_iocb->aio_fildes);
    __get_user(host_iocb->aio_buf, &target_iocb->aio_buf);
    __get_user(host_iocb->aio_offset, &target_iocb->aio_offset);
    __get_user(host_iocb->aio_reserved2, &target_iocb->aio_reserved2);
    __get_user(host_iocb->aio_flags, &target_iocb->aio_flags);
    __get_user(host_iocb->aio_resfd, &target_iocb->aio_resfd);

    host_iocb->aio_buf = (uint64_t)lock_user(VERIFY_READ,
                                             data->orig_buf,
                                             host_iocb->aio_nbytes, 1);

    unlock_user_struct(target_iocb, target_addr, 0);

    return 0;
}

int target_to_host_iocb_array(struct iocb **iocbpp, abi_long *target_addr_array,
                              abi_long nr)
{
    int i, ret;
    abi_long target_addr;

    for (i = 0; i < nr; i++) {
        iocbpp[i] = g_new(struct iocb, 1);
        __get_user(target_addr, &target_addr_array[i]);
        ret = target_to_host_iocb(iocbpp[i], target_addr);
        if (is_error(ret)) {
            while (--i >= 0) {
                host_iocb_free(iocbpp[i]);
            }
            return ret;
        }
    }
    return 0;
}
