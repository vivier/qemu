# Default configuration for aarch64-softmmu

# We support all the 32 bit boards so need all their config
include arm-softmmu.mak

CONFIG_XLNX_ZYNQMP=y
CONFIG_PL061=y
CONFIG_GPIO_KEY=y
