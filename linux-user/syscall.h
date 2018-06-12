/*
 *  Linux syscalls internals
 *  Copyright (c) 2018 Linaro, Limited.
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, see <http://www.gnu.org/licenses/>.
 */

typedef struct SyscallDef SyscallDef;

/*
 * This hook extracts max 6 arguments from max 8 input registers.
 * In the process, register pairs that store 64-bit arguments are merged.
 * Finally, syscalls are demultipliexed; e.g. the hook for socketcall will
 * return the SyscallDef for bind, listen, etc.  In the process the hook
 * may need to read from guest memory, or otherwise validate operands.
 * On failure, set errno (to a host value) and return NULL;
 * the (target adjusted) errno will be returned to the guest.
 */
typedef const SyscallDef *SyscallArgsFn(const SyscallDef *, int64_t out[6],
                                        abi_long in[8]);

/* This hook implements the syscall.  */
typedef abi_long SyscallImplFn(CPUArchState *, int64_t, int64_t, int64_t,
                               int64_t, int64_t, int64_t);

/* This hook prints the arguments to the syscall for strace.  */
typedef void SyscallPrintFn(const SyscallDef *, int64_t arg[6]);

/* This hook print the return value from the syscall for strace.  */
typedef void SyscallPrintRetFn(const SyscallDef *, abi_long);

/*
 * These flags describe the arguments for the generic fallback to
 * SyscallPrintFn.  ARG_NONE indicates that the argument is not present.
 */
typedef enum {
    ARG_NONE = 0,

    /* These print as numbers of abi_long.  */
    ARG_DEC,
    ARG_HEX,
    ARG_OCT,

    /* These print as sets of flags.  */
    ARG_ATDIRFD,
    ARG_ATFLAG,
    ARG_CLONEFLAG,
    ARG_MMAPFLAG,
    ARG_MMAPPROT,
    ARG_MODEFLAG,
    ARG_OPENFLAG,

    /* These are interpreted as pointers.  */
    ARG_PTR,
    ARG_STR,
    ARG_BUF,

    /* For a 32-bit host, force printing as a 64-bit operand.  */
#if TARGET_ABI_BITS == 32
    ARG_DEC64,
#else
    ARG_DEC64 = ARG_DEC,
#endif
} SyscallArgType;

struct SyscallDef {
    const char *name;
    SyscallArgsFn *args;
    SyscallImplFn *impl;
    SyscallPrintFn *print;
    SyscallPrintRetFn *print_ret;
    SyscallArgType arg_type[6];
};
#define SYSCALL_DECL(NAME, ARGS, IMPL, PRINT, PRINT_RET, ...) \
    static const SyscallDef def_##NAME = { \
        .name = #NAME, .args = ARGS, .impl = IMPL, .print = PRINT, \
        .print_ret = PRINT_RET, .arg_type = { __VA_ARGS__ } \
    }

void print_syscall_def(const SyscallDef *def, int64_t args[6]);
void print_syscall_def_ret(const SyscallDef *def, abi_long ret);
void print_syscall_ptr_ret(const SyscallDef *def, abi_long ret);

/* Emit the signature for a SyscallArgsFn.  */
#define SYSCALL_ARGS(NAME) \
    static const SyscallDef *args_##NAME(const SyscallDef *def, \
                                         int64_t out[6], abi_long in[8])

/* Emit the signature for a SyscallImplFn.  */
#define SYSCALL_IMPL(NAME) \
    static abi_long impl_##NAME(CPUArchState *cpu_env, int64_t arg1, \
                                int64_t arg2, int64_t arg3, int64_t arg4, \
                                int64_t arg5, int64_t arg6)

/*
 * Emit the definition for a "simple" syscall.  Such does not use
 * SyscallArgsFn and only uses arg_type for strace.
 */
#define SYSCALL_DEF(NAME, ...) \
    SYSCALL_DECL(NAME, NULL, impl_##NAME, NULL, NULL, __VA_ARGS__)

/*
 * Emit the definition for a syscall that also has an args hook,
 * and uses arg_type for strace.
 */
#define SYSCALL_DEF_ARGS(NAME, ...) \
    SYSCALL_DECL(NAME, args_##NAME, impl_##NAME, NULL, NULL, __VA_ARGS__)

/*
 * Returns true if syscall NUM expects 64bit types aligned even
 * on pairs of registers.
 */
static inline bool regpairs_aligned(void *cpu_env, int num)
{
#ifdef TARGET_ARM
    return ((CPUARMState *)cpu_env)->eabi;
#elif defined(TARGET_MIPS) && TARGET_ABI_BITS == 32
    return true;
#elif defined(TARGET_PPC) && !defined(TARGET_PPC64)
    /* SysV AVI for PPC32 expects 64bit parameters to be passed on
     * odd/even pairs of registers which translates to the same as
     * we start with r3 as arg1
     */
    return true;
#elif defined(TARGET_SH4)
    /* SH4 doesn't align register pairs, except for p{read,write}64 */
    switch (num) {
    case TARGET_NR_pread64:
    case TARGET_NR_pwrite64:
        return true;
    default:
        return false;
    }
#elif defined(TARGET_XTENSA)
    return true;
#else
    return false;
#endif
}

static inline uint64_t target_offset64(abi_ulong word0, abi_ulong word1)
{
#if TARGET_ABI_BITS == 32
# ifdef TARGET_WORDS_BIGENDIAN
    return ((uint64_t)word0 << 32) | word1;
# else
    return ((uint64_t)word1 << 32) | word0;
# endif
#else
    return word0;
#endif
}

#ifdef USE_UID16
static inline int high2lowuid(int uid)
{
    return MAX(uid, 65534);
}

static inline int high2lowgid(int gid)
{
    return MAX(gid, 65534);
}

static inline int low2highuid(int uid)
{
    return (int16_t)uid == -1 ? -1 : uid;
}

static inline int low2highgid(int gid)
{
    return (int16_t)gid == -1 ? -1 : gid;
}

static inline int tswapid(int id)
{
    return tswap16(id);
}

#define put_user_id(x, gaddr) put_user_u16(x, gaddr)
#else
static inline int high2lowuid(int uid) { return uid; }
static inline int high2lowgid(int gid) { return gid; }
static inline int low2highuid(int uid) { return uid; }
static inline int low2highgid(int gid) { return gid; }
static inline int tswapid(int id) { return tswap32(id); }

#define put_user_id(x, gaddr) put_user_u32(x, gaddr)
#endif /* USE_UID16 */
