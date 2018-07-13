#ifndef QGRAPH_E1000E
#define QGRAPH_E1000E

#include "qgraph.h"
#include "pci.h"

#define E1000E_RX0_MSG_ID           (0)
#define E1000E_TX0_MSG_ID           (1)
#define E1000E_OTHER_MSG_ID         (2)

#define E1000E_TDLEN    (0x3808)
#define E1000E_TDT      (0x3818)
#define E1000E_RDLEN    (0x2808)
#define E1000E_RDT      (0x2818)

typedef struct QE1000E QE1000E;
typedef struct QE1000E_PCI QE1000E_PCI;

struct QE1000E {
    uint32_t (*readl)(QE1000E *d, uint32_t reg);
    void (*writel)(QE1000E *d, uint32_t reg, uint32_t val);
    void (*wait_isr)(QE1000E *d, uint16_t msg_id);
    uint64_t tx_ring;
    uint64_t rx_ring;
};

struct QE1000E_PCI {
    QOSGraphObject obj;
    QPCIDevice pci_dev;
    QPCIBar mac_regs;
    QE1000E e1000e;
};

#endif