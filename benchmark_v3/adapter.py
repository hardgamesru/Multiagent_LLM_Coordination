"""Portable publication adapter; frozen measured v2 backend, immutable v3 tasks."""
import hashlib
import importlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
V2=ROOT/'multiagent_llm_experiment'
def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load_backend(path=V2):
    path=Path(path).resolve()
    frozen=json.loads((ROOT/'provenance/publication-freeze.json').read_text())
    for name,expected in frozen['frozen_v3'].items():
        if digest(ROOT/'benchmark_v3'/name)!=expected:raise RuntimeError('Frozen v3 mismatch: '+name)
    for name,expected in frozen['frozen_v2'].items():
        if digest(path/name)!=expected:raise RuntimeError('Frozen v2 mismatch: '+name)
    for name in ('tasks','agents','prompts','sandbox_runner','utils','llm_client','coordinators'):
        if name in sys.modules and Path(sys.modules[name].__file__).resolve().parent!=path:
            raise RuntimeError('Refusing mixed implementation: '+name)
    sys.path.insert(0,str(path))
    module=importlib.import_module('coordinators')
    assert len(module.COORDINATORS)==6
    return module,frozen['frozen_v2']
