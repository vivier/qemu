SYSCALL_DEF(mlock, ARG_PTR, ARG_DEC);
SYSCALL_DEF(mlockall, ARG_HEX);
#ifdef TARGET_NR_mmap
SYSCALL_DECL(mmap, args_mmap, impl_mmap, NULL, print_syscall_ptr_ret,
             ARG_PTR, ARG_DEC, ARG_MMAPPROT, ARG_MMAPFLAG, ARG_DEC, ARG_DEC);
#endif
#ifdef TARGET_NR_mmap2
SYSCALL_DECL(mmap2, args_mmap2, impl_mmap, NULL, print_syscall_ptr_ret,
             ARG_PTR, ARG_DEC, ARG_MMAPPROT, ARG_MMAPFLAG, ARG_DEC, ARG_DEC64);
#endif
SYSCALL_DEF(mprotect, ARG_PTR, ARG_DEC, ARG_MMAPPROT);
SYSCALL_DECL(mremap, NULL, impl_mremap, NULL, print_syscall_ptr_ret,
             ARG_PTR, ARG_DEC, ARG_DEC, ARG_HEX, ARG_PTR);
SYSCALL_DEF(msync, ARG_PTR, ARG_DEC, ARG_HEX);
SYSCALL_DEF(munlock, ARG_PTR, ARG_DEC);
SYSCALL_DEF(munlockall);
SYSCALL_DEF(munmap, ARG_PTR, ARG_DEC);
