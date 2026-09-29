"""V182: build the public repository tree as V181 does, plus the licence files (MIT for code, CC BY 4.0 for data and
documentation). The README and manuscript it copies are the V182 versions.

    .venv/bin/python scripts/build_public_repo_v182.py --dest DIR [--private-string S ...]
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_public_repo_v181 as v181

v181.EXTRA.update({'LICENSE': 'LICENSE', 'LICENSE-DATA': 'LICENSE-DATA', 'scripts/build_public_repo_v182.py': 'scripts/build_public_repo_v182.py'})

if __name__ == '__main__': v181.main()
