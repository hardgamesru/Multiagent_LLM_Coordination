# Benchmark v3 task specifications

Predefined before any model run. Expected evaluation values are stored privately in catalog.py.

## v3_01: encode_runs (easy)

Domain: data processing. Rationale: One pass with adjacent-state tracking.

Implement encode_runs(text: str) -> list[list]. Return consecutive Unicode character runs as [character, positive_count], preserving case and spaces. Empty string returns []. Length <= 2000. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `encode_runs('aaabb',) -> [['a', 3], ['b', 2]]`
- `encode_runs('',) -> []`

Development cases: 4. Held-out cases: 6.

## v3_02: rotate_grid (easy)

Domain: data structures. Rationale: Index mapping on a rectangular structure.

Implement rotate_grid(grid: list[list[int]]) -> list[list[int]]. Rotate a rectangular grid 90 degrees clockwise. [] returns []; any empty row or unequal row lengths raises ValueError. Dimensions <= 30. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `rotate_grid([[1, 2], [3, 4]],) -> [[3, 1], [4, 2]]`
- `rotate_grid([],) -> []`

Development cases: 4. Held-out cases: 6.

## v3_03: range_sums (easy)

Domain: algorithms. Rationale: Prefix sums and half-open boundary validation.

Implement range_sums(values: list[int], queries: list[list[int]]) -> list[int]. For each [left,right] return sum(values[left:right]). Require 0 <= left <= right <= len(values), otherwise raise ValueError for the entire call. Empty intervals sum to 0. <=2000 values and queries. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `range_sums([1, 2, 3], [[0, 2], [1, 3]]) -> [3, 5]`
- `range_sums([], []) -> []`

Development cases: 4. Held-out cases: 6.

## v3_04: merge_records (easy)

Domain: software engineering. Rationale: Stable identity grouping with last-write field semantics.

Implement merge_records(records: list[dict]) -> list[dict]. Every record has a string id. Merge records with the same id by field update in encounter order, later values replacing earlier values including None. Output ids in first-appearance order. Fields hold JSON scalars. <=200 records. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `merge_records([{'id': 'a', 'x': 1}, {'id': 'a', 'y': 2}],) -> [{'id': 'a', 'x': 1, 'y': 2}]`
- `merge_records([],) -> []`

Development cases: 3. Held-out cases: 4.

## v3_05: normalize_path (medium)

Domain: parsing. Rationale: Stack processing with root and literal-name distinctions.

Implement normalize_path(path: str) -> str for POSIX absolute paths. Collapse repeated /, remove . segments, and resolve .. without going above root. Preserve all other segment text, including spaces and ... . Reject paths not starting with / using ValueError. No filesystem access. Length <=2000. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `normalize_path('/a//b/../c',) -> '/a/c'`
- `normalize_path('/',) -> '/'`

Development cases: 4. Held-out cases: 6.

## v3_06: split_fields (medium)

Domain: parsing. Rationale: Finite-state quote and escape handling.

Implement split_fields(text: str) -> list[str]. Unquoted semicolons separate fields; preserve empty fields and whitespace. Single or double quotes can begin inside a field and are removed; matching quote ends quoting, opposite quote is literal inside quotes. Backslash anywhere escapes exactly the next character and is removed. A dangling escape or unclosed quote raises ValueError. Empty input returns ['']. Length <=2000. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `split_fields('a;"b;c"',) -> ['a', 'b;c']`
- `split_fields('',) -> ['']`

Development cases: 4. Held-out cases: 7.

## v3_07: window_minima (medium)

Domain: data structures. Rationale: Sliding-window state, duplicate values and eviction.

Implement window_minima(values: list[int], width: int) -> list[int]. Return the minimum of each consecutive window of exactly width elements. Require 1 <= width <= len(values), else ValueError. <=5000 values. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `window_minima([4, 2, 3, 1], 2) -> [2, 2, 1]`
- `window_minima([8], 1) -> [8]`

Development cases: 4. Held-out cases: 6.

## v3_08: build_layers (medium)

Domain: graph algorithms. Rationale: Deterministic simultaneous topological layers and cycle rejection.

Implement build_layers(dependencies: dict[str,list[str]]) -> list[list[str]]. A key depends on every listed node. Include dependency-only nodes; duplicate edges count once. Repeatedly output all currently dependency-free remaining nodes sorted lexicographically as one layer, then remove them simultaneously. Cycle anywhere raises ValueError. <=100 nodes. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `build_layers({'app': ['lib'], 'lib': []},) -> [['lib'], ['app']]`
- `build_layers({},) -> []`

Development cases: 4. Held-out cases: 5.

## v3_09: shortest_distances (medium)

Domain: graph algorithms. Rationale: Weighted shortest paths with unreachable nodes and parallel edges.

Implement shortest_distances(edges: list[list], source: str) -> dict. Each [u,v,w] is a directed edge with nonnegative integer weight. Include every endpoint and source. Return shortest distance from source, or None for unreachable nodes. Any negative weight anywhere raises ValueError. Allow loops and parallel edges. <=100 nodes, 500 edges. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `shortest_distances([['a', 'b', 3], ['a', 'c', 1], ['c', 'b', 1]], 'a') -> {'a': 0, 'b': 2, 'c': 1}`
- `shortest_distances([], 's') -> {'s': 0}`

Development cases: 3. Held-out cases: 5.

## v3_10: lru_trace (medium)

Domain: data structures. Rationale: State transitions, update recency and zero-capacity behavior.

Implement lru_trace(capacity: int, operations: list[list]) -> dict. Operations are ["put",string_key,integer_value] or ["get",string_key]. Gets return value or None on miss; successful gets and puts make the key most recent, including updates. Evict least recent key on overflow. Return {"gets": all get outputs, "keys": final keys least-to-most recent}. Capacity 0 stores nothing; negative capacity raises ValueError. <=1000 operations. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `lru_trace(2, [['put', 'a', 1], ['put', 'b', 2], ['get', 'a'], ['put', 'c', 3], ['get', 'b']]) -> {'gets': [1, None], 'keys': ['a', 'c']}`
- `lru_trace(0, [['put', 'a', 1], ['get', 'a']]) -> {'gets': [None], 'keys': []}`

Development cases: 3. Held-out cases: 4.

## v3_11: subtract_intervals (medium)

Domain: algorithms. Rationale: Interval-set algebra with union normalization and boundary semantics.

Implement subtract_intervals(base: list[list[int]], cuts: list[list[int]]) -> list[list[int]]. Each pair denotes half-open [start,end). Return union(base) minus union(cuts), as sorted maximal disjoint nonempty intervals, merging touching output intervals. Inputs may overlap and be unsorted; empty intervals ignored. Reversed interval raises ValueError even if irrelevant. <=100 intervals each. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `subtract_intervals([[0, 10]], [[3, 7]]) -> [[0, 3], [7, 10]]`
- `subtract_intervals([], []) -> []`

Development cases: 4. Held-out cases: 6.

## v3_12: aggregate_orders (medium)

Domain: data processing. Rationale: Validated join, stable output and exact integer aggregation.

Implement aggregate_orders(customers: list[dict], orders: list[dict]) -> list[dict]. Customers have unique string id; orders have customer string and amount integer in cents. Sum amounts for each customer, output {"id": id, "total": cents} in customer order, including zero-order customers. Duplicate customer id, unknown order customer, or negative amount raises ValueError. <=1000 records each. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `aggregate_orders([{'id': 'b'}, {'id': 'a'}], [{'customer': 'a', 'amount': 3}]) -> [{'id': 'b', 'total': 0}, {'id': 'a', 'total': 3}]`
- `aggregate_orders([], []) -> []`

Development cases: 3. Held-out cases: 4.

## v3_13: evaluate_expression (hard)

Domain: parsing. Rationale: Recursive precedence, unary operators, strict token consumption and errors.

Implement evaluate_expression(text: str) -> int. Grammar: expr=term ((+|-) term)*; term=atom (* atom)*; atom=ASCII nonnegative integer | (+|-) atom | ( expr ). Operators associate left, unary binds tighter than *. Ignore whitespace between tokens, not within a number. Leading zeroes allowed. Empty/invalid/trailing tokens or unbalanced parentheses raise ValueError. No eval/exec. Length <=300, nesting <=30. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `evaluate_expression('2+3*4',) -> 14`
- `evaluate_expression('-(2+3)*4',) -> -20`

Development cases: 5. Held-out cases: 11.

## v3_14: strongly_connected (hard)

Domain: graph algorithms. Rationale: Directed SCC partition with canonical ordering and implicit vertices.

Implement strongly_connected(graph: dict[str,list[str]]) -> list[list[str]]. Return strongly connected components of a directed graph. Include nodes appearing only as neighbors; allow loops/duplicate edges. Sort each component lexicographically and sort outer list lexicographically by component lists. <=100 nodes, 500 edges. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `strongly_connected({'a': ['b'], 'b': ['a', 'c']},) -> [['a', 'b'], ['c']]`
- `strongly_connected({},) -> []`

Development cases: 3. Held-out cases: 5.

## v3_15: maximum_matching (hard)

Domain: graph algorithms. Rationale: Augmenting paths and reassignment rather than greedy edge choice.

Implement maximum_matching(adjacency: dict[str,list[str]]) -> int. Keys are left vertices; values are adjacent right vertices. Left/right namespaces are distinct even for equal strings. Return maximum cardinality bipartite matching, not the matching itself. Duplicate edges count once. <=80 vertices per side, <=500 edges. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `maximum_matching({'a': ['x', 'y'], 'b': ['x']},) -> 2`
- `maximum_matching({},) -> 0`

Development cases: 3. Held-out cases: 5.

## v3_16: weighted_schedule (hard)

Domain: algorithms. Rationale: Dynamic programming with predecessor search, excluding greedy solutions.

Implement weighted_schedule(jobs: list[list[int]]) -> int. A job [start,end,value] occupies half-open [start,end). Choose compatible jobs maximizing sum of values; jobs touching endpoints are compatible. Require start < end and value >=0, otherwise ValueError. Empty set allowed. Jobs unordered, duplicates distinct but overlapping. <=1000 jobs. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `weighted_schedule([[0, 3, 5], [1, 2, 4], [2, 4, 4]],) -> 8`
- `weighted_schedule([],) -> 0`

Development cases: 3. Held-out cases: 7.

## v3_17: transaction_trace (hard)

Domain: software engineering. Rationale: Nested transaction semantics, rollback isolation and persistent read history.

Implement transaction_trace(operations: list[list]) -> dict. Start empty key/value state. Commands: ["set",string_key,integer_value], ["delete",key] (missing is no-op), ["get",key] appends value or None to reads, ["begin"], ["commit"], ["rollback"]. Begin snapshots current state; commit removes innermost snapshot keeping changes; rollback restores innermost snapshot. Outer rollback also undoes inner committed changes. Reads are never rolled back. Commit/rollback without transaction, or open transactions at end, raises ValueError. Return {"state": final_dict, "reads": outputs}. <=500 operations. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `transaction_trace([['set', 'x', 1], ['begin'], ['set', 'x', 2], ['get', 'x'], ['rollback'], ['get', 'x']],) -> {'state': {'x': 1}, 'reads': [2, 1]}`
- `transaction_trace([],) -> {'state': {}, 'reads': []}`

Development cases: 3. Held-out cases: 6.

## v3_18: apply_patch_lines (hard)

Domain: software engineering. Rationale: Atomic patch validation using original coordinates and exact context.

Implement apply_patch_lines(lines: list[str], hunks: list[list]) -> list[str]. Hunk [start,old,new] replaces original lines[start:start+len(old)] with list new; old must match exactly. All coordinates refer to original input. Require 0<=start and start+len(old)<=len(lines); starts strictly increasing, consumed ranges nonoverlapping (next start >= previous start+len(old)). Empty old permits insertion including at EOF. Any violation raises ValueError. Empty hunks return equal copy. <=1000 lines/hunks. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `apply_patch_lines(['a', 'b', 'c'], [[1, ['b'], ['B', 'X']]]) -> ['a', 'B', 'X', 'c']`
- `apply_patch_lines([], [[0, [], ['x']]]) -> ['x']`

Development cases: 3. Held-out cases: 7.

## v3_19: wildcard_matches (hard)

Domain: parsing and algorithms. Rationale: Glob matching with empty matches, escapes and full-string semantics.

Implement wildcard_matches(pattern: str, words: list[str]) -> list[str]. Match entire Unicode strings case-sensitively. Unescaped ? matches one character, * matches zero or more characters. Backslash escapes the next character literally; trailing backslash raises ValueError. No special meaning for any other character, including brackets and /. Return matching words in input order with duplicates. Pattern length <=100, <=200 words, each length <=100. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `wildcard_matches('a*?', ['a', 'ab', 'abc', 'ba']) -> ['ab', 'abc']`
- `wildcard_matches('', ['', 'a']) -> ['']`

Development cases: 3. Held-out cases: 7.

## v3_20: edit_distance (hard)

Domain: algorithms. Rationale: Two-dimensional dynamic programming with restricted transposition recurrence.

Implement edit_distance(source: str, target: str) -> int, the optimal string alignment (restricted Damerau-Levenshtein) distance. Each insertion, deletion, substitution or adjacent transposition costs 1. Precisely: D[i,0]=i; D[0,j]=j; D[i,j]=min(D[i-1,j]+1,D[i,j-1]+1,D[i-1,j-1]+(s[i-1]!=t[j-1])); if i,j>=2 and s[i-1]==t[j-2] and s[i-2]==t[j-1], also consider D[i-2,j-2]+1. Return D[len(s),len(t)]. Unicode code points; length <=100 each. Do not mutate any input. Use only Python standard library. Inputs satisfy the stated types and size bounds; only explicitly specified invalid inputs need rejection.

Visible examples:

- `edit_distance('ab', 'ba') -> 1`
- `edit_distance('', 'cat') -> 3`

Development cases: 3. Held-out cases: 8.
