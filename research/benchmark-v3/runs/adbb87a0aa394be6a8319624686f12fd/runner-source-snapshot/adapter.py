"""Explicit, hash-checked bridge to the frozen v2 implementation."""
import hashlib
import importlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
V2 = Path(r'multiagent_llm_experiment')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_backend(path=V2):
    path=Path(path).resolve()
    manifest=json.loads((ROOT/'benchmark_v3/preparation-manifest.json').read_text())
    for name, expected in manifest['sha256'].items():
        if digest(ROOT/'benchmark_v3'/name)!=expected:
            raise RuntimeError('Frozen v3 preparation mismatch: '+name)
    hashes={}
    for source in (ROOT/'lite-benchmark-work').glob('*.py'):
        actual=digest(path/source.name)
        if actual!=digest(source):
            raise RuntimeError('Frozen v2 implementation mismatch: '+source.name)
        hashes[source.name]=actual
    for name in ('tasks','agents','prompts','sandbox_runner','utils','llm_client','coordinators'):
        if name in sys.modules and Path(sys.modules[name].__file__).resolve().parent!=path:
            raise RuntimeError('Refusing mixed implementation: '+name)
    sys.path.insert(0,str(path))
    module=importlib.import_module('coordinators')
    assert len(module.COORDINATORS)==6
    return module, hashes
