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
