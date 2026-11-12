"""Run with python -m unittest benchmark_v3.test_validation."""
import unittest
from .validate import validate
from .catalog import get_tasks


class TaskValidationTests(unittest.TestCase):
    def test_contracts_references_oracles_and_mutants(self):
        result=validate()
        self.assertEqual(result['status'],'passed')
        self.assertEqual(len(result['tasks']),20)

    def test_prompt_material_has_no_private_tests_or_reference(self):
        for task in get_tasks():
            # Only these fields may be supplied to a generator.
            material=task.description+'\n'+'\n'.join(task.visible_examples)
            self.assertNotIn(task.reference_source,material)
            self.assertNotIn(task.hidden_tests,material)
            self.assertNotEqual(task.development_tests,task.hidden_tests)


if __name__=='__main__':
    unittest.main()
