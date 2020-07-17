#include "qemu/osdep.h"
#include "qemu.h"
#include "aio.h"

static GHashTable *iocb_list_hashtable(bool create)
{
    static GHashTable *iocb_list;

    if (create && !iocb_list) {
        iocb_list = g_hash_table_new(g_int64_hash, g_int64_equal);
    }

    return iocb_list;
}
struct iocb *target_find_host_iocb(abi_long target_iocb)
{
    GHashTable *iocb_list = iocb_list_hashtable(false);

    if (!iocb_list) {
        return NULL;
    }

    return g_hash_table_lookup(iocb_list, &target_iocb);
}

static void host_iocb_free(struct iocb *iocb)
{
    GHashTable *iocb_list = iocb_list_hashtable(false);

    if (iocb_list) {
        struct qemu_internal_io_data *data;
        data = (struct qemu_internal_io_data *)iocb->aio_data;
        g_hash_table_remove(iocb_list, &data->orig_obj);
    }
    g_free((void *)iocb->aio_data);
    g_free(iocb);
}

struct iocb *host_to_target_io_event(struct target_io_event *target_event,
                                     struct io_event *host_event)
{
    struct qemu_internal_io_data *data;
    struct iocb *obj;

    obj = (struct iocb *)host_event->obj;
    data = (struct qemu_internal_io_data *)host_event->data;

    __put_user(data->orig_data, &target_event->data);
    __put_user(data->orig_obj, &target_event->obj);
    __put_user(host_event->res, &target_event->res);
    __put_user(host_event->res2, &target_event->res2);

    unlock_user((void *)obj->aio_buf, data->orig_buf, obj->aio_nbytes);

    return obj;
}

void host_to_target_io_events(struct target_io_event *target_result,
                              struct io_event *host_result, long nr)
{
    int i;
    struct iocb *iocb;

    for (i = 0; i < nr; i++) {
        iocb = host_to_target_io_event(&target_result[i], &host_result[i]);
        host_iocb_free(iocb);
    }
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

    g_hash_table_add(iocb_list_hashtable(true), &data->orig_obj);

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
