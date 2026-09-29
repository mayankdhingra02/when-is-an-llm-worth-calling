import importlib.util,ctypes as C
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'scripts/codec_api_v51.py';s=importlib.util.spec_from_file_location('v51',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_lz4_pinned_abi_layout():
 assert C.sizeof(m.FrameInfo)==32 and C.sizeof(m.Preferences)==56
 assert m.FrameInfo.contentSize.offset==16 and m.Preferences.compressionLevel.offset==32
 assert bytes(m.Preferences())==bytes(56)
