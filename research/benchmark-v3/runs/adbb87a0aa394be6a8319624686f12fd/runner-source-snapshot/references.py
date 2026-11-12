"""Trusted reference implementations; never include this module in model prompts."""


def encode_runs(text):
    result = []
    for ch in text:
        if result and result[-1][0] == ch:
            result[-1][1] += 1
        else:
            result.append([ch, 1])
    return result


def rotate_grid(grid):
    if not grid:
        return []
    if not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError('nonempty rectangular rows required')
    return [list(row) for row in zip(*grid[::-1])]


def range_sums(values, queries):
    prefix = [0]
    for n in values:
        prefix.append(prefix[-1] + n)
    result = []
    for left, right in queries:
        if not 0 <= left <= right <= len(values):
            raise ValueError('invalid range')
        result.append(prefix[right] - prefix[left])
    return result


def merge_records(records):
    merged = {}
    for record in records:
        key = record['id']
        merged.setdefault(key, {}).update(record)
    return list(merged.values())


def normalize_path(path):
    if not path.startswith('/'):
        raise ValueError('absolute path required')
    parts = []
    for part in path.split('/'):
        if part == '..':
            if parts:
                parts.pop()
        elif part and part != '.':
            parts.append(part)
    return '/' + '/'.join(parts)


def split_fields(text):
    result, token, quote, escape = [], [], None, False
    for ch in text:
        if escape:
            token.append(ch)
            escape = False
        elif ch == '\\':
            escape = True
        elif quote:
            if ch == quote:
                quote = None
            else:
                token.append(ch)
        elif ch in "\"'":
            quote = ch
        elif ch == ';':
            result.append(''.join(token))
            token = []
        else:
            token.append(ch)
    if escape or quote:
        raise ValueError('incomplete field')
    return result + [''.join(token)]


def window_minima(values, width):
    from collections import deque
    if width < 1 or width > len(values):
        raise ValueError('invalid width')
    q, result = deque(), []
    for i, value in enumerate(values):
        while q and q[0] <= i - width:
            q.popleft()
        while q and values[q[-1]] >= value:
            q.pop()
        q.append(i)
        if i >= width - 1:
            result.append(values[q[0]])
    return result


def build_layers(dependencies):
    nodes = set(dependencies)
    for deps in dependencies.values():
        nodes.update(deps)
    pending = {n: set(dependencies.get(n, [])) for n in nodes}
    result = []
    while pending:
        layer = sorted(n for n, deps in pending.items() if not deps)
        if not layer:
            raise ValueError('cycle')
        result.append(layer)
        pending = {n: deps - set(layer) for n, deps in pending.items() if n not in layer}
    return result


def shortest_distances(edges, source):
    import heapq
    graph = {source: []}
    for u, v, weight in edges:
        if weight < 0:
            raise ValueError('negative weight')
        graph.setdefault(u, []).append((v, weight))
        graph.setdefault(v, [])
    distances = {n: None for n in graph}
    distances[source] = 0
    queue = [(0, source)]
    while queue:
        distance, u = heapq.heappop(queue)
        if distance != distances[u]:
            continue
        for v, weight in graph[u]:
            new = distance + weight
            if distances[v] is None or new < distances[v]:
                distances[v] = new
                heapq.heappush(queue, (new, v))
    return distances


def lru_trace(capacity, operations):
    from collections import OrderedDict
    if capacity < 0:
        raise ValueError('negative capacity')
    cache, outputs = OrderedDict(), []
    for op in operations:
        if op[0] == 'put':
            _, key, value = op
            if capacity:
                cache[key] = value
                cache.move_to_end(key)
                if len(cache) > capacity:
                    cache.popitem(last=False)
        else:
            _, key = op
            outputs.append(cache.get(key))
            if key in cache:
                cache.move_to_end(key)
    return {'gets': outputs, 'keys': list(cache)}


def subtract_intervals(base, cuts):
    for a, b in base + cuts:
        if a > b:
            raise ValueError('reversed interval')
    points = sorted(set(x for pair in base + cuts for x in pair))
    result = []
    for a, b in zip(points, points[1:]):
        if any(x <= a < y for x, y in base) and not any(x <= a < y for x, y in cuts):
            if result and result[-1][1] == a:
                result[-1][1] = b
            else:
                result.append([a, b])
    return result


def aggregate_orders(customers, orders):
    if len({c['id'] for c in customers}) != len(customers):
        raise ValueError('duplicate customer')
    totals = {c['id']: 0 for c in customers}
    for order in orders:
        if order['customer'] not in totals or order['amount'] < 0:
            raise ValueError('invalid order')
        totals[order['customer']] += order['amount']
    return [{'id': c['id'], 'total': totals[c['id']]} for c in customers]


def evaluate_expression(text):
    import re
    tokens = re.findall(r'[0-9]+|[^\s]', text)
    index = 0
    def atom():
        nonlocal index
        if index == len(tokens):
            raise ValueError('missing atom')
        token = tokens[index]
        index += 1
        if token in ('+', '-'):
            return atom() * (1 if token == '+' else -1)
        if token == '(':
            value = expr()
            if index == len(tokens) or tokens[index] != ')':
                raise ValueError('missing closing parenthesis')
            index += 1
            return value
        if re.fullmatch('[0-9]+', token):
            return int(token)
        raise ValueError('invalid atom')
    def term():
        nonlocal index
        value = atom()
        while index < len(tokens) and tokens[index] == '*':
            index += 1
            value *= atom()
        return value
    def expr():
        nonlocal index
        value = term()
        while index < len(tokens) and tokens[index] in ('+', '-'):
            op = tokens[index]
            index += 1
            other = term()
            value = value + other if op == '+' else value - other
        return value
    result = expr()
    if index != len(tokens):
        raise ValueError('trailing tokens')
    return result


def strongly_connected(graph):
    # Reachability-based trusted oracle, independent of a typical Tarjan solution.
    nodes = set(graph)
    for neighbors in graph.values():
        nodes.update(neighbors)
    reach = {}
    for start in nodes:
        visited, stack = set(), [start]
        while stack:
            n = stack.pop()
            if n not in visited:
                visited.add(n)
                stack.extend(graph.get(n, []))
        reach[start] = visited
    result, remaining = [], set(nodes)
    while remaining:
        n = min(remaining)
        group = sorted(v for v in remaining if v in reach[n] and n in reach[v])
        result.append(group)
        remaining.difference_update(group)
    return sorted(result)


def maximum_matching(adjacency):
    matched = {}
    def augment(left, seen):
        for right in sorted(set(adjacency[left])):
            if right in seen:
                continue
            seen.add(right)
            if right not in matched or augment(matched[right], seen):
                matched[right] = left
                return True
        return False
    return sum(augment(left, set()) for left in sorted(adjacency))


def weighted_schedule(jobs):
    import bisect
    if any(start >= end or value < 0 for start, end, value in jobs):
        raise ValueError('invalid job')
    ordered = sorted(jobs, key=lambda job: job[1])
    ends, best = [j[1] for j in ordered], [0]
    for i, (start, end, value) in enumerate(ordered):
        previous = bisect.bisect_right(ends, start, 0, i)
        best.append(max(best[-1], best[previous] + value))
    return best[-1]


def transaction_trace(operations):
    state, stack, reads = {}, [], []
    for op in operations:
        command = op[0]
        if command == 'begin':
            stack.append(state.copy())
        elif command in ('commit', 'rollback'):
            if not stack:
                raise ValueError('no transaction')
            saved = stack.pop()
            if command == 'rollback':
                state = saved
        elif command == 'set':
            state[op[1]] = op[2]
        elif command == 'delete':
            state.pop(op[1], None)
        else:
            reads.append(state.get(op[1]))
    if stack:
        raise ValueError('unclosed transaction')
    return {'state': state, 'reads': reads}


def apply_patch_lines(lines, hunks):
    result, cursor, previous_start = [], 0, -1
    for start, old, new in hunks:
        if start <= previous_start or start < cursor or start < 0 or start + len(old) > len(lines):
            raise ValueError('invalid position')
        if lines[start:start + len(old)] != old:
            raise ValueError('context mismatch')
        result.extend(lines[cursor:start])
        result.extend(new)
        cursor, previous_start = start + len(old), start
    return result + lines[cursor:]


def wildcard_matches(pattern, words):
    tokens, index = [], 0
    while index < len(pattern):
        ch = pattern[index]
        if ch == '\\':
            index += 1
            if index == len(pattern):
                raise ValueError('dangling escape')
            tokens.append(('literal', pattern[index]))
        elif ch in '*?':
            tokens.append((ch, ch))
        else:
            tokens.append(('literal', ch))
        index += 1
    def matches(word):
        reachable = {0}
        for kind, value in tokens:
            if kind == '*':
                reachable = set(range(min(reachable), len(word) + 1)) if reachable else set()
            else:
                reachable = {i + 1 for i in reachable if i < len(word) and (kind == '?' or word[i] == value)}
        return len(word) in reachable
    return [word for word in words if matches(word)]


def edit_distance(source, target):
    # Optimal string alignment distance, including one adjacent transposition.
    d = [[0] * (len(target) + 1) for _ in range(len(source) + 1)]
    for i in range(len(source) + 1):
        d[i][0] = i
    for j in range(len(target) + 1):
        d[0][j] = j
    for i in range(1, len(source) + 1):
        for j in range(1, len(target) + 1):
            d[i][j] = min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + (source[i-1] != target[j-1]))
            if i > 1 and j > 1 and source[i-1] == target[j-2] and source[i-2] == target[j-1]:
                d[i][j] = min(d[i][j], d[i-2][j-2] + 1)
    return d[-1][-1]
