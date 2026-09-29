"""Strict independent validator for the flat typed STRIPS/action-cost subset.

Not a general PDDL validator. Unsupported syntax is rejected at construction,
including unreachable action bodies. Plans prove feasibility/cost, not optimality.
"""
import re
from decimal import Decimal, InvalidOperation


def parse(text):
    tokens = re.findall(r'\(|\)|[^\s()]+', re.sub(r';[^\n]*', '', text).lower())
    stack, roots = [], []
    for token in tokens:
        if token == '(':
            item = []
            (stack[-1] if stack else roots).append(item)
            stack.append(item)
        elif token == ')':
            if not stack:
                raise ValueError('Unbalanced parentheses')
            stack.pop()
        else:
            if not stack:
                raise ValueError('Atom outside expression')
            stack[-1].append(token)
    if stack:
        raise ValueError('Unbalanced parentheses')
    return roots


def typed(tokens):
    out, pending = {}, []
    i = 0
    while i < len(tokens):
        x = tokens[i]
        if not isinstance(x, str):
            raise ValueError('Non-flat type')
        if x == '-':
            if not pending or i + 1 >= len(tokens):
                raise ValueError('Malformed typed list')
            for name in pending:
                if name in out:
                    raise ValueError('Duplicate symbol')
                out[name] = tokens[i + 1]
            pending = []
            i += 2
        else:
            pending.append(x)
            i += 1
    for name in pending:
        if name in out:
            raise ValueError('Duplicate symbol')
        out[name] = 'object'
    return out


class Task:
    def __init__(self, domain, problem):
        ds, ps = parse(domain), parse(problem)
        if len(ds) != 1 or len(ps) != 1 or ds[0][0] != 'define' or ps[0][0] != 'define':
            raise ValueError('Expected one domain/problem')
        d, p = ds[0][1:], ps[0][1:]
        allowed_d = {'domain', ':requirements', ':types', ':predicates', ':functions', ':action'}
        allowed_p = {'problem', ':domain', ':objects', ':init', ':goal', ':metric'}
        if any(s[0] not in allowed_d for s in d) or any(s[0] not in allowed_p for s in p):
            raise ValueError('Unsupported section')
        def one(sections, name):
            found = [s[1:] for s in sections if s[0] == name]
            if len(found) != 1:
                raise ValueError('Missing/duplicate section: ' + name)
            return found[0]
        if one(d, 'domain') != one(p, ':domain'):
            raise ValueError('Domain mismatch')
        self.types = {'object', *one(d, ':types')}
        if '-' in self.types:
            raise ValueError('Type hierarchy unsupported')
        self.objects = typed(one(p, ':objects'))
        self.predicates = {x[0]: typed(x[1:]) for x in one(d, ':predicates')}
        funcs = one(d, ':functions')
        self.functions = {}
        while funcs:
            decl, *funcs = funcs
            if not isinstance(decl, list):
                raise ValueError('Bad function declaration')
            self.functions[decl[0]] = typed(decl[1:])
            if funcs[:2] == ['-', 'number']:
                funcs = funcs[2:]
        for symbols in [self.objects, *self.predicates.values(), *self.functions.values()]:
            if any(t not in self.types for t in symbols.values()):
                raise ValueError('Unknown type')
        self.actions = {}
        for s in d:
            if s[0] != ':action':
                continue
            if len(s) != 8 or set(s[2::2]) != {':parameters', ':precondition', ':effect'}:
                raise ValueError('Unsupported action structure')
            opts = dict(zip(s[2::2], s[3::2]))
            params = typed(opts[':parameters'])
            if any(t not in self.types or not k.startswith('?') for k, t in params.items()):
                raise ValueError('Bad parameter types')
            if s[1] in self.actions:
                raise ValueError('Duplicate action')
            self.actions[s[1]] = (params, opts[':precondition'], opts[':effect'])
            self.check_expr(opts[':precondition'], params, False)
            self.check_expr(opts[':effect'], params, True)
        self.state, self.numbers = set(), {}
        for x in one(p, ':init'):
            if x[0] == '=' and len(x) == 3:
                self.atom(x[1], {}, self.functions)
                key = tuple(x[1])
                if key in self.numbers:
                    raise ValueError('Duplicate numeric initialization')
                self.numbers[key] = self.number(x[2])
            else:
                self.atom(x, {}, self.predicates)
                if tuple(x) in self.state:
                    raise ValueError('Duplicate initial fact')
                self.state.add(tuple(x))
        if self.numbers.get(('total-cost',)) != 0:
            raise ValueError('Initial cost must be zero')
        goal = one(p, ':goal')
        if len(goal) != 1 or one(p, ':metric') != ['minimize', ['total-cost']]:
            raise ValueError('Unsupported goal/metric')
        self.goal = goal[0]
        self.check_expr(self.goal, {}, False)

    @staticmethod
    def number(x):
        try:
            val = Decimal(x)
        except (InvalidOperation, TypeError):
            raise ValueError('Non-numeric cost') from None
        if not val.is_finite() or val < 0:
            raise ValueError('Negative/non-finite cost')
        return val

    def atom(self, expr, variables, declarations):
        if not isinstance(expr, list) or not expr or expr[0] not in declarations:
            raise ValueError('Unknown/unsupported atom: ' + str(expr))
        types = list(declarations[expr[0]].values())
        if len(expr) - 1 != len(types):
            raise ValueError('Arity mismatch')
        for name, expected in zip(expr[1:], types):
            if not isinstance(name, str) or name not in {**self.objects, **variables}:
                raise ValueError('Unknown term')
            actual = variables.get(name, self.objects.get(name))
            if actual != expected and expected != 'object':
                raise ValueError('Type mismatch')

    def check_expr(self, x, variables, effect):
        if not isinstance(x, list) or not x:
            raise ValueError('Empty expression')
        if x[0] == 'and':
            for child in x[1:]:
                self.check_expr(child, variables, effect)
        elif x[0] == 'not' and len(x) == 2:
            self.atom(x[1], variables, self.predicates)
        elif x[0] == 'increase' and effect and len(x) == 3 and x[1] == ['total-cost']:
            if isinstance(x[2], list):
                self.atom(x[2], variables, self.functions)
                if x[2][0] == 'total-cost':
                    raise ValueError('Dynamic numeric expression unsupported')
            else:
                self.number(x[2])
        else:
            self.atom(x, variables, self.predicates)

    def validate(self, plan):
        state, cost = set(self.state), Decimal(0)
        def ground(x, env):
            return tuple(env.get(t, t) for t in x)
        def holds(x, env):
            if x[0] == 'and':
                return all(holds(y, env) for y in x[1:])
            if x[0] == 'not':
                return ground(x[1], env) not in state
            return ground(x, env) in state
        steps = parse(plan)
        for i, step in enumerate(steps):
            if not step or step[0] not in self.actions:
                raise ValueError('Unknown plan action')
            params, pre, eff = self.actions[step[0]]
            self.atom(step, {}, {step[0]: params})
            env = dict(zip(params, step[1:]))
            if not holds(pre, env):
                raise ValueError(f'Unsatisfied precondition at step {i}')
            add, delete = set(), set()
            def apply(x):
                nonlocal cost
                if x[0] == 'and':
                    for y in x[1:]:
                        apply(y)
                elif x[0] == 'not':
                    delete.add(ground(x[1], env))
                elif x[0] == 'increase':
                    value = x[2]
                    if isinstance(value, list):
                        key = ground(value, env)
                        if key not in self.numbers:
                            raise ValueError('Undefined numeric function')
                        cost += self.numbers[key]
                    else:
                        cost += self.number(value)
                else:
                    add.add(ground(x, env))
            apply(eff)
            state = (state - delete) | add
        if not holds(self.goal, {}):
            raise ValueError('Goal not achieved')
        return {'valid': True, 'steps': len(steps), 'cost': str(cost),
                'validator': 'independent-strips-subset-v55', 'proves_optimality': False}
