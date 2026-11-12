"""Offline validation of trusted fixtures; optional unchanged v2 Docker backend.

Usage: python -m benchmark_v3.validate [--sandbox-dir PATH] [--output PATH]
No LLM client is imported and no API credentials are read.
"""
import argparse
import copy
import itertools
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path
from .catalog import get_tasks
from . import references as r


def run_source(code, tests):
    namespace = {}
    exec(compile(code, '<trusted-fixture>', 'exec'), namespace)
    exec(compile(tests, '<trusted-tests>', 'exec'), namespace)


def oracle_checks():
    """Deterministic extra reference checks, not additional experimental tasks."""
    rng = random.Random(38197)
    count = 0
    for _ in range(150):
        values = [rng.randrange(-9, 10) for _ in range(rng.randrange(1, 30))]
        width = rng.randrange(1, len(values)+1)
        assert r.window_minima(values,width) == [min(values[i:i+width]) for i in range(len(values)-width+1)]
        queries = [sorted([rng.randrange(len(values)+1),rng.randrange(len(values)+1)]) for _ in range(10)]
        assert r.range_sums(values, queries) == [sum(values[a:b]) for a,b in queries]
        matrix = [[rng.randrange(10) for _ in range(3)] for _ in range(2)]
        rotated = matrix
        for _ in range(4):
            rotated = r.rotate_grid(rotated)
        assert rotated == matrix
        jobs = []
        for _ in range(rng.randrange(0, 9)):
            start = rng.randrange(8)
            jobs.append([start, start+rng.randrange(1,5), rng.randrange(10)])
        best = 0
        for mask in range(1 << len(jobs)):
            selected = sorted(jobs[i] for i in range(len(jobs)) if mask & (1 << i))
            if all(a[1] <= b[0] for a,b in zip(selected,selected[1:])):
                best = max(best, sum(j[2] for j in selected))
        assert r.weighted_schedule(jobs) == best
        graph = {str(i): [str(j) for j in range(4) if rng.randrange(3)==0] for i in range(4)}
        def matching_oracle(left, used):
            if not left:
                return 0
            return max([matching_oracle(left[1:],used)] + [1+matching_oracle(left[1:],used|{v}) for v in graph[left[0]] if v not in used])
        assert r.maximum_matching(graph) == matching_oracle(list(graph),set())
        base = [sorted([rng.randrange(-5,6),rng.randrange(-5,6)]) for _ in range(4)]
        cuts = [sorted([rng.randrange(-5,6),rng.randrange(-5,6)]) for _ in range(3)]
        actual = r.subtract_intervals(base,cuts)
        expected_points = {x for x in range(-5,5) if any(a<=x<b for a,b in base) and not any(a<=x<b for a,b in cuts)}
        assert {x for a,b in actual for x in range(a,b)} == expected_points
        assert all(a<b for a,b in actual) and all(a[1]<b[0] for a,b in zip(actual,actual[1:]))
        a,b,c = [rng.randrange(-10,11) for _ in range(3)]
        assert r.evaluate_expression(f'({a})+({b})*({c})') == a+b*c
        edges = [[str(i),str(j),rng.randrange(5)] for i in range(4) for j in range(4) if rng.randrange(3)==0]
        expected = {'0':0}
        for u,v,w in edges:
            expected.setdefault(u,None)
            expected.setdefault(v,None)
        for _ in range(len(expected)):
            for u,v,w in edges:
                if expected[u] is not None and (expected[v] is None or expected[v]>expected[u]+w):
                    expected[v]=expected[u]+w
        assert r.shortest_distances(edges,'0') == expected
        count += 8
    # Independent recursive glob oracle on a small exhaustive alphabet.
    def glob(p,w):
        if not p:
            return not w
        if p[0]=='*':
            return glob(p[1:],w) or bool(w) and glob(p,w[1:])
        return bool(w) and (p[0]=='?' or p[0]==w[0]) and glob(p[1:],w[1:])
    words = [''.join(x) for n in range(4) for x in itertools.product('ab',repeat=n)]
    for size in range(4):
        for tokens in itertools.product('ab*?',repeat=size):
            pattern=''.join(tokens)
            assert r.wildcard_matches(pattern,words)==[w for w in words if glob(pattern,w)]
            count += 1
    return count


def validate(sandbox_dir=None):
    tasks = get_tasks()
    assert len(tasks)==20 and len({t.task_id for t in tasks})==20
    assert Counter(t.difficulty for t in tasks)=={'easy':4,'medium':8,'hard':8}
    oracle_count = oracle_checks()
    results = []
    backend = None
    if sandbox_dir:
        sys.path.insert(0,str(Path(sandbox_dir).resolve()))
        from sandbox_runner import run_code_in_sandbox
        backend = run_code_in_sandbox
    for task in tasks:
        assert task.rationale and task.visible_examples and task.specification
        assert len(task.development)>=3 and len(task.evaluation)>=4
        assert not ({repr(c.args) for c in task.development} & {repr(c.args) for c in task.evaluation}), task.task_id
        record = {'task_id':task.task_id,'difficulty':task.difficulty,
                  'development_cases':len(task.development),'evaluation_cases':len(task.evaluation),'splits':{}}
        for split,cases in [('development',task.development),('evaluation',task.evaluation)]:
            tests = task.tests(cases)
            run_source(task.reference_source,tests)
            # None-return and first-example overfit are separate weak fixtures.
            mutants = [f'def {task.name}(*args): return None\n',f'def {task.name}(*args): return {task.development[0].expected!r}\n']
            for code in mutants:
                try:
                    run_source(code,tests)
                except (AssertionError,ValueError,TypeError):
                    pass
                else:
                    raise AssertionError(f'{task.task_id}/{split}: mutant survived')
            info = {'reference':'passed','mutants_rejected':len(mutants)}
            if backend:
                result = backend(task.reference_source,tests,timeout=20,diagnostics=True)
                if result.status!='passed':
                    raise AssertionError(f'{task.task_id}/{split}: Docker {result.status}: {result.error_message}')
                # One bad fixture per split verifies backend failure classification.
                bad = backend(mutants[0],tests,timeout=20)
                assert bad.status=='failed_tests', (task.task_id, split, bad.status)
                info['docker_reference']='passed'
                info['docker_bad_fixture']='failed_tests'
            record['splits'][split]=info
        results.append(record)
        print(f'{task.task_id} {task.difficulty}: development/evaluation passed',flush=True)
    return {'status':'passed','api_calls':0,'oracle_checks':oracle_count,'docker_checked':bool(backend),'tasks':results}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--sandbox-dir')
    parser.add_argument('--output',default='benchmark_v3/validation-results.json')
    args=parser.parse_args()
    started=time.perf_counter()
    try:
        result=validate(args.sandbox_dir)
    except Exception as exc:
        result={'status':'failed','error':str(exc),'api_calls':0}
        raise
    finally:
        result['elapsed_seconds']=round(time.perf_counter()-started,3)
        Path(args.output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
