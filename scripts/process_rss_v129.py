"""macOS process-group RSS using libproc; no repeated ps subprocess launches.

ABI from the installed SDK sys/proc_info.h and libproc.h. Apple XNU's
libsyscall/wrappers/libproc/libproc.c confirms listpgrppids returns PID count.
Unknown/truncated/failed readings fail closed, never masquerade as zero usage.
"""
import ctypes,os,sys,errno

class TaskInfo(ctypes.Structure):
    _fields_=[(n,ctypes.c_uint64) for n in ['virtual_size','resident_size','total_user','total_system','threads_user','threads_system']]+[(n,ctypes.c_int32) for n in ['policy','faults','pageins','cow_faults','messages_sent','messages_received','syscalls_mach','syscalls_unix','csw','threadnum','numrunning','priority']]

def library():
    if sys.platform!='darwin':raise RuntimeError('This resource monitor requires macOS')
    lib=ctypes.CDLL('/usr/lib/libproc.dylib',use_errno=True)
    lib.proc_pidinfo.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_uint64,ctypes.c_void_p,ctypes.c_int]
    lib.proc_pidinfo.restype=ctypes.c_int
    lib.proc_listpgrppids.argtypes=[ctypes.c_int,ctypes.c_void_p,ctypes.c_int]
    lib.proc_listpgrppids.restype=ctypes.c_int
    return lib

def read_pid(lib,pid):
    info=TaskInfo();assert ctypes.sizeof(info)==96
    ctypes.set_errno(0);n=lib.proc_pidinfo(pid,4,0,ctypes.byref(info),ctypes.sizeof(info))
    if n!=ctypes.sizeof(info) or info.resident_size<=0:
        raise OSError(ctypes.get_errno() or errno.EIO,'Unknown process RSS',pid)
    return int(info.resident_size)

def group_rss(lib,pgid):
    pids=(ctypes.c_int*4096)();ctypes.set_errno(0)
    count=lib.proc_listpgrppids(pgid,pids,ctypes.sizeof(pids))
    if not 0<count<len(pids):raise OSError(ctypes.get_errno() or errno.EIO,'Missing or truncated process group',pgid)
    ids=list(pids[:count])
    if len(set(ids))!=count or any(p<=0 for p in ids):raise ValueError('Invalid process enumeration')
    return sum(read_pid(lib,pid) for pid in ids)

def rss(pgid):
    lib=library()
    return read_pid(lib,os.getpid()) if pgid==-1 else group_rss(lib,pgid)
