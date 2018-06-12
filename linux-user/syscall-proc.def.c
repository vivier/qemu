SYSCALL_DEF_ARGS(clone, ARG_CLONEFLAG, ARG_PTR, ARG_PTR, ARG_PTR, ARG_PTR);
#ifdef TARGET_NR_fork
SYSCALL_DEF(fork);
#endif
#ifdef TARGET_NR_vfork
SYSCALL_DEF(vfork);
#endif
#ifdef TARGET_NR_getegid
SYSCALL_DEF(getegid);
#endif
#ifdef TARGET_NR_getegid32
SYSCALL_DEF(getegid32);
#endif
#ifdef TARGET_NR_geteuid
SYSCALL_DEF(geteuid);
#endif
#ifdef TARGET_NR_geteuid32
SYSCALL_DEF(geteuid32);
#endif
#ifdef TARGET_NR_getgid
SYSCALL_DEF(getgid);
#endif
#ifdef TARGET_NR_getgid32
SYSCALL_DEF(getgid32);
#endif
SYSCALL_DEF(getgroups, ARG_DEC, ARG_PTR);
#ifdef TARGET_NR_getgroups32
SYSCALL_DEF(getgroups32, ARG_DEC, ARG_PTR);
#endif
#ifdef TARGET_NR_getresgid
SYSCALL_DEF(getresgid, ARG_PTR, ARG_PTR, ARG_PTR);
#endif
#ifdef TARGET_NR_getresgid32
SYSCALL_DEF(getresgid32, ARG_PTR, ARG_PTR, ARG_PTR);
#endif
#ifdef TARGET_NR_getresuid
SYSCALL_DEF(getresuid, ARG_PTR, ARG_PTR, ARG_PTR);
#endif
#ifdef TARGET_NR_getresuid32
SYSCALL_DEF(getresuid32, ARG_PTR, ARG_PTR, ARG_PTR);
#endif
#ifdef TARGET_NR_getpgrp
SYSCALL_DEF(getpgrp);
#endif
#ifdef TARGET_NR_getpid
SYSCALL_DEF(getpid);
#endif
#ifdef TARGET_NR_getppid
SYSCALL_DEF(getppid);
#endif
SYSCALL_DEF(gettid);
#ifdef TARGET_NR_getuid
SYSCALL_DEF(getuid);
#endif
#ifdef TARGET_NR_getuid32
SYSCALL_DEF(getuid32);
#endif
#ifdef TARGET_NR_getxgid
SYSCALL_DEF(getxgid);
#endif
#ifdef TARGET_NR_getxpid
SYSCALL_DEF(getxpid);
#endif
#ifdef TARGET_NR_getxuid
SYSCALL_DEF(getxuid);
#endif
SYSCALL_DEF(setfsgid, ARG_DEC);
#ifdef TARGET_NR_setfsgid32
SYSCALL_DEF(setfsgid32, ARG_DEC);
#endif
SYSCALL_DEF(setfsuid, ARG_DEC);
#ifdef TARGET_NR_setfsuid32
SYSCALL_DEF(setfsuid32, ARG_DEC);
#endif
SYSCALL_DEF(setgid, ARG_DEC);
#ifdef TARGET_NR_setgid32
SYSCALL_DEF(setgid32, ARG_DEC);
#endif
SYSCALL_DEF(setgroups, ARG_DEC, ARG_PTR);
#ifdef TARGET_NR_setgroups32
SYSCALL_DEF(setgroups32, ARG_DEC, ARG_PTR);
#endif
SYSCALL_DEF(setregid, ARG_DEC, ARG_DEC);
#ifdef TARGET_NR_setregid32
SYSCALL_DEF(setregid32, ARG_DEC, ARG_DEC);
#endif
#ifdef TARGET_NR_setresgid
SYSCALL_DEF(setresgid, ARG_DEC, ARG_DEC, ARG_DEC);
#endif
#ifdef TARGET_NR_setresgid32
SYSCALL_DEF(setresgid32, ARG_DEC, ARG_DEC, ARG_DEC);
#endif
#ifdef TARGET_NR_setresuid
SYSCALL_DEF(setresuid, ARG_DEC, ARG_DEC, ARG_DEC);
#endif
#ifdef TARGET_NR_setresuid32
SYSCALL_DEF(setresuid32, ARG_DEC, ARG_DEC, ARG_DEC);
#endif
SYSCALL_DEF(setreuid, ARG_DEC, ARG_DEC);
#ifdef TARGET_NR_setreuid32
SYSCALL_DEF(setreuid32, ARG_DEC, ARG_DEC);
#endif
SYSCALL_DEF(setsid);
SYSCALL_DEF(setuid, ARG_DEC);
#ifdef TARGET_NR_setuid32
SYSCALL_DEF(setuid32, ARG_DEC);
#endif
#ifdef TARGET_NR_get_thread_area
#if defined(TARGET_I386) && defined(TARGET_ABI32)
SYSCALL_DECL(get_thread_area, NULL, impl_get_thread_area, NULL,
             print_syscall_ptr_ret, ARG_PTR);
#else
SYSCALL_DECL(get_thread_area, NULL, impl_get_thread_area, NULL,
             print_syscall_ptr_ret);
#endif
#endif
#ifdef TARGET_NR_set_thread_area 
SYSCALL_DEF(set_thread_area, ARG_PTR);
#endif
SYSCALL_DEF(set_tid_address, ARG_PTR);
