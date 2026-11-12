import unittest
from tools.verify_publication import verify

class PublicationTests(unittest.TestCase):
    def test_all_240_records_tables_hashes_and_usage(self):
        self.assertEqual(verify()['main_records'],240)

    def test_paid_generation_requires_explicit_opt_in(self):
        import subprocess
        import sys
        result=subprocess.run([sys.executable,'-m','benchmark_v3.runner','--pilot'],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertIn('--enable-paid',result.stderr)

    def test_reproduction_preserves_captured_evidence(self):
        import hashlib
        import os
        from pathlib import Path
        import subprocess
        import sys
        import tempfile
        root=Path(__file__).resolve().parents[1]
        report=root/'research/benchmark-v3/report.md'
        protected={p:hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (root/'research').rglob('*')
                   if p.is_file() and p!=report and p.suffix in {'.csv','.json','.py','.md','.svg'}}
        executable=os.environ.get('V3_ANALYSIS_PYTHON',sys.executable)
        with tempfile.TemporaryDirectory() as config:
            env=dict(os.environ,MPLBACKEND='Agg',MPLCONFIGDIR=config)
            figures=Path(config)/'figures'
            result=subprocess.run([executable,str(root/'tools/reproduce.py'),'--figures-dir',str(figures)],cwd=root,
                                  env=env,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual({p.name for p in figures.glob('*.svg')},
                             {'success-by-repetition.svg','success-by-difficulty-two-repetitions.svg','task-stability.svg'})
            for path in figures.glob('*.svg'):
                self.assertIn('<svg',path.read_text(encoding='utf-8'))
        for path,expected in protected.items():
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),expected,str(path))
        self.assertNotIn(b'\r',report.read_bytes())
        text=report.read_bytes().decode('utf-8')
        self.assertNotIn('\ufffd',text)
        self.assertFalse(any('\u0400'<=ch<='\u04ff' for ch in text))
        self.assertEqual(verify()['main_records'],240)
