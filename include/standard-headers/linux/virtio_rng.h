#ifndef _LINUX_VIRTIO_RNG_H
#define _LINUX_VIRTIO_RNG_H
/* This header is BSD licensed so anyone can use the definitions to implement
 * compatible drivers/servers. */
#include "standard-headers/linux/virtio_ids.h"
#include "standard-headers/linux/virtio_config.h"

/* The features bitmap for virtuio rng */
#define VIRTIO_RNG_F_CTRL_VQ		0	/* Device has control queue */

struct virtio_rng_ctrl_hdr {
	uint8_t cmd;
} QEMU_PACKED;

#define VIRTIO_RNG_CMD_FLUSH 0

typedef uint8_t virtio_rng_ctrl_ack;

#define VIRTIO_RNG_OK	0
#define VIRTIO_RNG_ERR	1

#endif /* _LINUX_VIRTIO_RNG_H */
