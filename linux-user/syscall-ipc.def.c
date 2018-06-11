#ifdef TARGET_NR_msgctl
SYSCALL_DEF(msgctl, ARG_DEC, ARG_DEC, ARG_PTR);
#endif
#ifdef TARGET_NR_msgget
SYSCALL_DEF(msgget, ARG_DEC, ARG_DEC);
#endif
#ifdef TARGET_NR_msgrcv
SYSCALL_DEF(msgrcv, ARG_DEC, ARG_PTR, ARG_DEC, ARG_DEC, ARG_HEX);
#endif
#ifdef TARGET_NR_msgsnd
SYSCALL_DEF(msgsnd, ARG_DEC, ARG_PTR, ARG_DEC, ARG_HEX);
#endif
#ifdef TARGET_NR_semctl
SYSCALL_DEF(semctl, ARG_DEC, ARG_DEC, ARG_DEC, ARG_HEX);
#endif
#ifdef TARGET_NR_semget
SYSCALL_DEF(semget, ARG_DEC, ARG_DEC, ARG_HEX);
#endif
#ifdef TARGET_NR_semop
SYSCALL_DEF(semop, ARG_DEC, ARG_PTR, ARG_DEC);
#endif
#ifdef TARGET_NR_shmget
SYSCALL_DEF(shmget, ARG_DEC, ARG_DEC, ARG_HEX);
#endif
#ifdef TARGET_NR_shmctl
SYSCALL_DEF(shmctl, ARG_DEC, ARG_DEC, ARG_PTR);
#endif
#ifdef TARGET_NR_shmat
SYSCALL_DECL(shmat, NULL, impl_shmat, NULL, print_syscall_ptr_ret, ARG_DEC, ARG_PTR, ARG_HEX);
#endif
#ifdef TARGET_NR_shmdt
SYSCALL_DEF(shmdt, ARG_PTR);
#endif
#ifdef TARGET_NR_ipc
SYSCALL_DEF_ARGS(ipc, ARG_HEX, ARG_DEC, ARG_DEC, ARG_HEX, ARG_PTR, ARG_HEX);
#endif
