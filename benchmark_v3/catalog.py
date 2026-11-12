"""Preregistered task contracts and independent, literal expected test cases.

Evaluation cases and references are private scoring material, not prompt context.
Difficulty is an a-priori complexity judgement, not a measured model outcome.
"""
from dataclasses import dataclass
import inspect
from . import references


@dataclass(frozen=True)
class Case:
    args: tuple
    expected: object = None
    error: str | None = None


def C(*args, expected=None):
    return Case(args, expected)


def E(*args):
    return Case(args, error='ValueError')


@dataclass(frozen=True)
class Task:
    task_id: str
    name: str
    difficulty: str
    domain: str
    rationale: str
    specification: str
    development: tuple[Case, ...]
    evaluation: tuple[Case, ...]

    @property
    def function_name(self):
        return self.name

    @property
    def description(self):
        return self.specification + ' Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.'

    @property
    def visible_examples(self):
        return [f'{self.name}{case.args!r} -> {case.expected!r}' if not case.error else f'{self.name}{case.args!r} raises ValueError' for case in self.development[:2]]

    @property
    def reference_source(self):
        return inspect.getsource(getattr(references, self.name))

    def tests(self, cases):
        lines = []
        for i, case in enumerate(cases):
            # Fresh literal inputs prevent one case from contaminating another.
            lines.append(f'_args = {case.args!r}')
            lines.append('_before = repr(_args)')
            if case.error:
                lines += ['try:', f'    {self.name}(*_args)', 'except ValueError:', '    pass', 'else:', f'    raise AssertionError("case {i}: expected ValueError")']
            else:
                lines.append(f'assert {self.name}(*_args) == {case.expected!r}, "case {i}"')
            lines.append(f'assert repr(_args) == _before, "case {i}: input mutation"')
        return '\n'.join(lines)

    @property
    def development_tests(self):
        return self.tests(self.development)

    @property
    def hidden_tests(self):
        return self.tests(self.evaluation)


def T(number, name, difficulty, domain, rationale, spec, dev, held):
    return Task(f'v3_{number:02}', name, difficulty, domain, rationale, spec, tuple(dev), tuple(held))


def get_tasks():
    return [
        T(1, 'encode_runs', 'easy', 'data processing', 'One pass with adjacent-state tracking.',
          'Implement encode_runs(text: str) -> list[list]. Return consecutive Unicode character runs as [character, positive_count], preserving case and spaces. Empty string returns []. Length <= 2000.',
          [C('aaabb', expected=[['a',3],['b',2]]), C('',expected=[]), C('aAa',expected=[['a',1],['A',1],['a',1]]), C('  ',expected=[[' ',2]])],
          [C('x',expected=[['x',1]]), C('abbaa',expected=[['a',1],['b',2],['a',2]]), C('яя🙂🙂',expected=[['я',2],['🙂',2]]), C('\n\n\t',expected=[['\n',2],['\t',1]]), C('11122',expected=[['1',3],['2',2]]), C('abab',expected=[['a',1],['b',1],['a',1],['b',1]])]),
        T(2, 'rotate_grid', 'easy', 'data structures', 'Index mapping on a rectangular structure.',
          'Implement rotate_grid(grid: list[list[int]]) -> list[list[int]]. Rotate a rectangular grid 90 degrees clockwise. [] returns []; any empty row or unequal row lengths raises ValueError. Dimensions <= 30.',
          [C([[1,2],[3,4]],expected=[[3,1],[4,2]]), C([],expected=[]), C([[1,2,3]],expected=[[1],[2],[3]]), E([[]])],
          [C([[1],[2],[3]],expected=[[3,2,1]]), C([[7]],expected=[[7]]), C([[1,2,3],[4,5,6]],expected=[[4,1],[5,2],[6,3]]), E([[1],[2,3]]), E([[],[]]), C([[-1,0],[2,-3]],expected=[[2,-1],[-3,0]])]),
        T(3, 'range_sums', 'easy', 'algorithms', 'Prefix sums and half-open boundary validation.',
          'Implement range_sums(values: list[int], queries: list[list[int]]) -> list[int]. For each [left,right] return sum(values[left:right]). Require 0 <= left <= right <= len(values), otherwise raise ValueError for the entire call. Empty intervals sum to 0. <=2000 values and queries.',
          [C([1,2,3],[[0,2],[1,3]],expected=[3,5]), C([],[],expected=[]), C([5],[[0,0],[0,1]],expected=[0,5]), E([1],[[-1,1]])],
          [C([-2,4,-1],[[0,3],[1,1],[2,3]],expected=[1,0,-1]), C([],[[0,0]],expected=[0]), C([9,8],[],expected=[]), E([1],[[0,2]]), E([1,2],[[2,1]]), C([0,0],[[0,2],[2,2]],expected=[0,0])]),
        T(4, 'merge_records', 'easy', 'software engineering', 'Stable identity grouping with last-write field semantics.',
          'Implement merge_records(records: list[dict]) -> list[dict]. Every record has a string id. Merge records with the same id by field update in encounter order, later values replacing earlier values including None. Output ids in first-appearance order. Fields hold JSON scalars. <=200 records.',
          [C([{'id':'a','x':1},{'id':'a','y':2}],expected=[{'id':'a','x':1,'y':2}]), C([],expected=[]), C([{'id':'b'},{'id':'a'},{'id':'b','x':None}],expected=[{'id':'b','x':None},{'id':'a'}])],
          [C([{'id':'z','x':2},{'id':'z','x':0}],expected=[{'id':'z','x':0}]), C([{'id':''}],expected=[{'id':''}]), C([{'id':'x','a':False},{'id':'y','a':1},{'id':'x','a':None}],expected=[{'id':'x','a':None},{'id':'y','a':1}]), C([{'id':'1'},{'id':'2'},{'id':'1'}],expected=[{'id':'1'},{'id':'2'}])]),
        T(5, 'normalize_path', 'medium', 'parsing', 'Stack processing with root and literal-name distinctions.',
          'Implement normalize_path(path: str) -> str for POSIX absolute paths. Collapse repeated /, remove . segments, and resolve .. without going above root. Preserve all other segment text, including spaces and ... . Reject paths not starting with / using ValueError. No filesystem access. Length <=2000.',
          [C('/a//b/../c',expected='/a/c'), C('/',expected='/'), C('/../../x/',expected='/x'), E('a/b')],
          [C('/a/./b/',expected='/a/b'), C('////',expected='/'), C('/a/../..',expected='/'), C('/.../a b',expected='/.../a b'), E(''), C('/x/.hidden/..',expected='/x')]),
        T(6, 'split_fields', 'medium', 'parsing', 'Finite-state quote and escape handling.',
          'Implement split_fields(text: str) -> list[str]. Unquoted semicolons separate fields; preserve empty fields and whitespace. Single or double quotes can begin inside a field and are removed; matching quote ends quoting, opposite quote is literal inside quotes. Backslash anywhere escapes exactly the next character and is removed. A dangling escape or unclosed quote raises ValueError. Empty input returns [\'\']. Length <=2000.',
          [C('a;"b;c"',expected=['a','b;c']), C('',expected=['']), C('a\\;b;c',expected=['a;b','c']), E("'bad")],
          [C(';x;',expected=['','x','']), C("a'bc'd;z",expected=['abcd','z']), C('"x\'y"; q ',expected=["x'y",' q ']), C('"";\'\'',expected=['','']), C('x\\\\;y',expected=['x\\','y']), E('x\\'), C('"a\\"b"',expected=['a"b'])]),
        T(7, 'window_minima', 'medium', 'data structures', 'Sliding-window state, duplicate values and eviction.',
          'Implement window_minima(values: list[int], width: int) -> list[int]. Return the minimum of each consecutive window of exactly width elements. Require 1 <= width <= len(values), else ValueError. <=5000 values.',
          [C([4,2,3,1],2,expected=[2,2,1]), C([8],1,expected=[8]), E([],1), E([1],0)],
          [C([2,2,2],2,expected=[2,2]), C([1,2,3,4],3,expected=[1,2]), C([4,3,2,1],3,expected=[2,1]), C([-1,-3,0],1,expected=[-1,-3,0]), C([3,1,2],3,expected=[1]), E([1,2],3)]),
        T(8, 'build_layers', 'medium', 'graph algorithms', 'Deterministic simultaneous topological layers and cycle rejection.',
          'Implement build_layers(dependencies: dict[str,list[str]]) -> list[list[str]]. A key depends on every listed node. Include dependency-only nodes; duplicate edges count once. Repeatedly output all currently dependency-free remaining nodes sorted lexicographically as one layer, then remove them simultaneously. Cycle anywhere raises ValueError. <=100 nodes.',
          [C({'app':['lib'],'lib':[]},expected=[['lib'],['app']]), C({},expected=[]), C({'b':[],'a':[]},expected=[['a','b']]), E({'x':['x']})],
          [C({'a':['b','b'],'c':['b']},expected=[['b'],['a','c']]), C({'a':['b'],'b':['c'],'z':[]},expected=[['c','z'],['b'],['a']]), E({'a':['b'],'b':['a'],'z':[]}), C({'leaf':[]},expected=[['leaf']]), C({'x':['a','b'],'a':['c'],'b':['c']},expected=[['c'],['a','b'],['x']])]),
        T(9, 'shortest_distances', 'medium', 'graph algorithms', 'Weighted shortest paths with unreachable nodes and parallel edges.',
          'Implement shortest_distances(edges: list[list], source: str) -> dict. Each [u,v,w] is a directed edge with nonnegative integer weight. Include every endpoint and source. Return shortest distance from source, or None for unreachable nodes. Any negative weight anywhere raises ValueError. Allow loops and parallel edges. <=100 nodes, 500 edges.',
          [C([['a','b',3],['a','c',1],['c','b',1]],'a',expected={'a':0,'b':2,'c':1}), C([],'s',expected={'s':0}), E([['x','y',-1]],'s')],
          [C([['x','y',2]],'s',expected={'s':0,'x':None,'y':None}), C([['a','a',0],['a','b',0],['b','a',1]],'a',expected={'a':0,'b':0}), C([['a','b',7],['a','b',2]],'a',expected={'a':0,'b':2}), C([['a','b',3],['b','c',4]],'c',expected={'a':None,'b':None,'c':0}), E([['a','b',1],['z','z',-2]],'a')]),
        T(10, 'lru_trace', 'medium', 'data structures', 'State transitions, update recency and zero-capacity behavior.',
          'Implement lru_trace(capacity: int, operations: list[list]) -> dict. Operations are ["put",string_key,integer_value] or ["get",string_key]. Gets return value or None on miss; successful gets and puts make the key most recent, including updates. Evict least recent key on overflow. Return {"gets": all get outputs, "keys": final keys least-to-most recent}. Capacity 0 stores nothing; negative capacity raises ValueError. <=1000 operations.',
          [C(2,[['put','a',1],['put','b',2],['get','a'],['put','c',3],['get','b']],expected={'gets':[1,None],'keys':['a','c']}), C(0,[['put','a',1],['get','a']],expected={'gets':[None],'keys':[]}), E(-1,[])],
          [C(2,[['put','a',1],['put','b',2],['put','a',4]],expected={'gets':[],'keys':['b','a']}), C(1,[['get','z'],['put','a',0],['put','b',2],['get','a']],expected={'gets':[None,None],'keys':['b']}), C(3,[],expected={'gets':[],'keys':[]}), C(1,[['put','',7],['get','']],expected={'gets':[7],'keys':['']})]),
        T(11, 'subtract_intervals', 'medium', 'algorithms', 'Interval-set algebra with union normalization and boundary semantics.',
          'Implement subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]. Each pair denotes half-open [start,end). Return union(base) minus union(cuts), as sorted maximal disjoint nonempty intervals, merging touching output intervals. Inputs may overlap and be unsorted; empty intervals ignored. Reversed interval raises ValueError even if irrelevant. <=100 intervals each.',
          [C([[0,10]],[[3,7]],expected=[[0,3],[7,10]]), C([],[],expected=[]), C([[1,3],[3,5]],[],expected=[[1,5]]), E([[2,1]],[])],
          [C([[0,4],[2,8]],[[1,3],[5,9]],expected=[[0,1],[3,5]]), C([[1,2]],[[0,3]],expected=[]), C([[2,2],[4,6]],[[0,4],[6,9]],expected=[[4,6]]), C([[-5,0]], [[-3,-1]],expected=[[-5,-3],[-1,0]]), E([],[[9,2]]), C([[4,8],[0,1]],[],expected=[[0,1],[4,8]])]),
        T(12, 'aggregate_orders', 'medium', 'data processing', 'Validated join, stable output and exact integer aggregation.',
          'Implement aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]. Customers have unique string id; orders have customer string and amount integer in cents. Sum amounts for each customer, output {"id": id, "total": cents} in customer order, including zero-order customers. Duplicate customer id, unknown order customer, or negative amount raises ValueError. <=1000 records each.',
          [C([{'id':'b'},{'id':'a'}],[{'customer':'a','amount':3}],expected=[{'id':'b','total':0},{'id':'a','total':3}]), C([],[],expected=[]), E([{'id':'x'},{'id':'x'}],[])],
          [C([{'id':'a'}],[{'customer':'a','amount':0},{'customer':'a','amount':7},{'customer':'a','amount':8}],expected=[{'id':'a','total':15}]), E([],[{'customer':'x','amount':1}]), E([{'id':'a'}],[{'customer':'a','amount':-1}]), C([{'id':''}],[],expected=[{'id':'','total':0}])]),
        T(13, 'evaluate_expression', 'hard', 'parsing', 'Recursive precedence, unary operators, strict token consumption and errors.',
          'Implement evaluate_expression(text: str) -> int. Grammar: expr=term ((+|-) term)*; term=atom (* atom)*; atom=ASCII nonnegative integer | (+|-) atom | ( expr ). Operators associate left, unary binds tighter than *. Ignore whitespace between tokens, not within a number. Leading zeroes allowed. Empty/invalid/trailing tokens or unbalanced parentheses raise ValueError. No eval/exec. Length <=300, nesting <=30.',
          [C('2+3*4',expected=14), C('-(2+3)*4',expected=-20), C('1--2',expected=3), E('2/1'), E('')],
          [C('10-3-2',expected=5), C(' --5 + +2 ',expected=7), C('2*-3',expected=-6), C('(1+(2*3))',expected=7), C('007',expected=7), E('1 2'), E('()'), E('(1+2'), E('3+'), E('2(3)'), E('a')]),
        T(14, 'strongly_connected', 'hard', 'graph algorithms', 'Directed SCC partition with canonical ordering and implicit vertices.',
          'Implement strongly_connected(graph: dict[str,list[str]]) -> list[list[str]]. Return strongly connected components of a directed graph. Include nodes appearing only as neighbors; allow loops/duplicate edges. Sort each component lexicographically and sort outer list lexicographically by component lists. <=100 nodes, 500 edges.',
          [C({'a':['b'],'b':['a','c']},expected=[['a','b'],['c']]), C({},expected=[]), C({'z':['z']},expected=[['z']])],
          [C({'a':['b'],'b':['c'],'c':['a','d'],'d':['e'],'e':['d']},expected=[['a','b','c'],['d','e']]), C({'b':[],'a':[]},expected=[['a'],['b']]), C({'a':['b','b']},expected=[['a'],['b']]), C({'a':['c'],'b':['c'],'c':[]},expected=[['a'],['b'],['c']]), C({'x':['y'],'y':['z'],'z':['y']},expected=[['x'],['y','z']])]),
        T(15, 'maximum_matching', 'hard', 'graph algorithms', 'Augmenting paths and reassignment rather than greedy edge choice.',
          'Implement maximum_matching(adjacency: dict[str,list[str]]) -> int. Keys are left vertices; values are adjacent right vertices. Left/right namespaces are distinct even for equal strings. Return maximum cardinality bipartite matching, not the matching itself. Duplicate edges count once. <=80 vertices per side, <=500 edges.',
          [C({'a':['x','y'],'b':['x']},expected=2), C({},expected=0), C({'a':[]},expected=0)],
          [C({'a':['x'],'b':['x'],'c':['x']},expected=1), C({'a':['a'],'b':['b']},expected=2), C({'a':['1','2'],'b':['2','3'],'c':['1']},expected=3), C({'u':['v','v']},expected=1), C({'a':[],'b':['r'],'c':['s']},expected=2)]),
        T(16, 'weighted_schedule', 'hard', 'algorithms', 'Dynamic programming with predecessor search, excluding greedy solutions.',
          'Implement weighted_schedule(jobs: list[list[int]]) -> int. A job [start,end,value] occupies half-open [start,end). Choose compatible jobs maximizing sum of values; jobs touching endpoints are compatible. Require start < end and value >=0, otherwise ValueError. Empty set allowed. Jobs unordered, duplicates distinct but overlapping. <=1000 jobs.',
          [C([[0,3,5],[1,2,4],[2,4,4]],expected=8), C([],expected=0), E([[2,2,1]])],
          [C([[0,10,20],[0,4,9],[4,10,9]],expected=20), C([[2,3,5],[0,2,4]],expected=9), C([[1,4,0],[1,4,0]],expected=0), C([[-3,-1,2],[-1,1,3]],expected=5), E([[0,1,-1]]), E([[3,1,1]]), C([[0,2,5],[0,2,5]],expected=5)]),
        T(17, 'transaction_trace', 'hard', 'software engineering', 'Nested transaction semantics, rollback isolation and persistent read history.',
          'Implement transaction_trace(operations: list[list]) -> dict. Start empty key/value state. Commands: ["set",string_key,integer_value], ["delete",key] (missing is no-op), ["get",key] appends value or None to reads, ["begin"], ["commit"], ["rollback"]. Begin snapshots current state; commit removes innermost snapshot keeping changes; rollback restores innermost snapshot. Outer rollback also undoes inner committed changes. Reads are never rolled back. Commit/rollback without transaction, or open transactions at end, raises ValueError. Return {"state": final_dict, "reads": outputs}. <=500 operations.',
          [C([['set','x',1],['begin'],['set','x',2],['get','x'],['rollback'],['get','x']],expected={'state':{'x':1},'reads':[2,1]}), C([],expected={'state':{},'reads':[]}), E([['commit']])],
          [C([['begin'],['set','x',1],['begin'],['set','x',2],['commit'],['rollback'],['get','x']],expected={'state':{},'reads':[None]}), C([['set','x',0],['begin'],['delete','x'],['get','x'],['rollback']],expected={'state':{'x':0},'reads':[None]}), C([['delete','a'],['get','a']],expected={'state':{},'reads':[None]}), C([['begin'],['set','x',3],['commit']],expected={'state':{'x':3},'reads':[]}), E([['begin']]), E([['rollback']])]),
        T(18, 'apply_patch_lines', 'hard', 'software engineering', 'Atomic patch validation using original coordinates and exact context.',
          'Implement apply_patch_lines(lines: list[str], hunks: list[list]) -> list[str]. Hunk [start,old,new] replaces original lines[start:start+len(old)] with list new; old must match exactly. All coordinates refer to original input. Require 0<=start and start+len(old)<=len(lines); starts strictly increasing, consumed ranges nonoverlapping (next start >= previous start+len(old)). Empty old permits insertion including at EOF. Any violation raises ValueError. Empty hunks return equal copy. <=1000 lines/hunks.',
          [C(['a','b','c'],[[1,['b'],['B','X']]],expected=['a','B','X','c']), C([],[[0,[],['x']]],expected=['x']), E(['a'],[[0,['b'],[]]])],
          [C(['a','b','c','d'],[[0,['a'],[]],[2,['c'],['C']]],expected=['b','C','d']), C(['a'],[[1,[],['z']]],expected=['a','z']), C(['a','b'],[],expected=['a','b']), E(['a','b'],[[0,['a','b'],[]],[1,['b'],[]]]), E(['a'],[[0,[],['x']],[0,[],['y']]]), E(['a'],[[2,[],[]]]), E(['a'],[[-1,[],[]]])]),
        T(19, 'wildcard_matches', 'hard', 'parsing and algorithms', 'Glob matching with empty matches, escapes and full-string semantics.',
          'Implement wildcard_matches(pattern: str, words: list[str]) -> list[str]. Match entire Unicode strings case-sensitively. Unescaped ? matches one character, * matches zero or more characters. Backslash escapes the next character literally; trailing backslash raises ValueError. No special meaning for any other character, including brackets and /. Return matching words in input order with duplicates. Pattern length <=100, <=200 words, each length <=100.',
          [C('a*?',['a','ab','abc','ba'],expected=['ab','abc']), C('', ['', 'a'],expected=['']), E('x\\',[])],
          [C('*',['','x','x'],expected=['','x','x']), C('a\\*b',['ab','a*b','axxb'],expected=['a*b']), C('a?c',['ac','abc','a🙂c'],expected=['abc','a🙂c']), C('**a**',['a','ba','ab',''],expected=['a','ba','ab']), C('[x]',['x','[x]'],expected=['[x]']), C('\\?',['?','a'],expected=['?']), C('A',['a','A'],expected=['A'])]),
        T(20, 'edit_distance', 'hard', 'algorithms', 'Two-dimensional dynamic programming with restricted transposition recurrence.',
          'Implement edit_distance(source: str, target: str) -> int, the optimal string alignment (restricted Damerau-Levenshtein) distance. Each insertion, deletion, substitution or adjacent transposition costs 1. Precisely: D[i,0]=i; D[0,j]=j; D[i,j]=min(D[i-1,j]+1,D[i,j-1]+1,D[i-1,j-1]+(s[i-1]!=t[j-1])); if i,j>=2 and s[i-1]==t[j-2] and s[i-2]==t[j-1], also consider D[i-2,j-2]+1. Return D[len(s),len(t)]. Unicode code points; length <=100 each.',
          [C('ab','ba',expected=1), C('','cat',expected=3), C('same','same',expected=0)],
          [C('kitten','sitting',expected=3), C('CA','ABC',expected=3), C('abc','acb',expected=1), C('abc','',expected=3), C('aab','aba',expected=1), C('🙂a','a🙂',expected=1), C('','',expected=0), C('abc','xyz',expected=3)])
    ]
