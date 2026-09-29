"""Small ctypes bindings to installed, pinned public codec C APIs; no remote code."""
import ctypes as C
class FrameInfo(C.Structure):
 _fields_=[('blockSizeID',C.c_int),('blockMode',C.c_int),('contentChecksumFlag',C.c_int),('frameType',C.c_int),('contentSize',C.c_ulonglong),('dictID',C.c_uint),('blockChecksumFlag',C.c_int)]
class Preferences(C.Structure):
 _fields_=[('frameInfo',FrameInfo),('compressionLevel',C.c_int),('autoFlush',C.c_uint),('favorDecSpeed',C.c_uint),('reserved',C.c_uint*3)]

def function(lib,name,result,args):
 f=getattr(lib,name);f.restype=result;f.argtypes=args;return f
class Codec:
 def __init__(self,family,path):
  self.family=family;self.lib=C.CDLL(path);L=self.lib;size=C.c_size_t;ptr=C.c_void_p
  if family=='zstd':
   self.error=function(L,'ZSTD_isError',C.c_uint,[size]);self.bound=function(L,'ZSTD_compressBound',size,[size]);self.create=function(L,'ZSTD_createCCtx',ptr,[]);self.free=function(L,'ZSTD_freeCCtx',size,[ptr]);self.param=function(L,'ZSTD_CCtx_setParameter',size,[ptr,C.c_int,C.c_int]);self.run=function(L,'ZSTD_compress2',size,[ptr,ptr,size,ptr,size])
  elif family=='lz4':
   assert C.sizeof(FrameInfo)==32 and C.sizeof(Preferences)==56
   self.error=function(L,'LZ4F_isError',C.c_uint,[size]);self.bound=function(L,'LZ4F_compressFrameBound',size,[size,C.POINTER(Preferences)]);self.run=function(L,'LZ4F_compressFrame',size,[ptr,size,ptr,size,C.POINTER(Preferences)])
  else:raise ValueError('Unknown family')
 def checked(self,n):
  if self.error(n):raise RuntimeError('Codec error '+str(n))
  return n
 def compress(self,payload,setting):
  source=C.create_string_buffer(payload)
  if self.family=='zstd':
   context=self.create()
   if not context:raise MemoryError('ZSTD context')
   try:
    for p,v in [(100,setting['level']),(101,setting['window_log']),(200,0),(201,1),(400,0)]:self.checked(self.param(context,p,v))
    bound=self.bound(len(payload));dest=C.create_string_buffer(bound)
    n=self.checked(self.run(context,dest,bound,source,len(payload)));return dest.raw[:n]
   finally:self.checked(self.free(context))
  prefs=Preferences();prefs.frameInfo.blockSizeID=setting['block_id'];prefs.frameInfo.blockMode=1;prefs.frameInfo.contentChecksumFlag=1;prefs.compressionLevel=setting['level']
  bound=self.checked(self.bound(len(payload),C.byref(prefs)));dest=C.create_string_buffer(bound)
  n=self.checked(self.run(dest,bound,source,len(payload),C.byref(prefs)));return dest.raw[:n]
