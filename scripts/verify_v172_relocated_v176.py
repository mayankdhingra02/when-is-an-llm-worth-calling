"""V176 bundle wrapper: run the unchanged verify_v172 from a different directory.

verify_v172 compares each stage's recorded llama-server command with runtime_v172.server_command(), and that command
embeds the absolute project path. Unpacked anywhere else, the comparison fails although nothing recorded has changed.
This wrapper recovers the original project root from the recorded commands themselves (they must all agree), makes
server_command() build paths under that root, and then runs verify_v172.main() unmodified. Every other check is untouched.
"""
from pathlib import Path
from collect_smollm_v47 import ROOT, read
from common_v172 import STAGES
import runtime_v172, verify_v172

BINARY = ('.local-runtime', 'llama-b11146', 'llama-server')

def recorded_root():
    roots = set()
    for s in STAGES:
        parts = Path(read(ROOT/'results/v172_models'/s/'runtime.json')['command'][0]).parts
        assert parts[-3:] == BINARY, parts
        roots.add(Path(*parts[:-3]))
    assert len(roots) == 1, roots
    return roots.pop()

def main():
    orig = recorded_root()
    def relocated(model_path, port):
        rel = Path(model_path).relative_to(ROOT); runtime_v172.ROOT = orig
        try: return runtime_v172.server_command(orig/rel, port)
        finally: runtime_v172.ROOT = ROOT
    verify_v172.server_command = relocated
    verify_v172.main()

if __name__ == '__main__': main()
