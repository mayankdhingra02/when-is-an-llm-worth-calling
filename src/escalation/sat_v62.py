"""Deterministic planted-CNF workload and independent clause-by-clause validator."""
import random

def generate(n,seed):
    rng=random.Random(seed);witness={v:rng.choice([False,True]) for v in range(1,n+1)}
    clauses=[];seen=set()
    while len(clauses)<43*n//10:
        variables=rng.sample(range(1,n+1),3)
        clause=tuple(sorted((v if rng.choice([False,True]) else -v for v in variables),key=abs))
        if clause not in seen and any(witness[abs(l)]==(l>0) for l in clause):seen.add(clause);clauses.append(clause)
    return clauses,witness

def dimacs(n,clauses):return f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)

def parse(text):
    header=None;clauses=[];pending=[]
    for line in text.splitlines():
        if not line or line.startswith('c'):continue
        if line.startswith('p '):
            if header is not None:raise ValueError('Duplicate header')
            p,kind,n,m=line.split()
            if kind!='cnf':raise ValueError('Wrong format')
            header=int(n),int(m);continue
        if header is None:raise ValueError('Missing header')
        for word in line.split():
            lit=int(word)
            if lit==0:clauses.append(tuple(pending));pending=[]
            elif abs(lit)>header[0]:raise ValueError('Out-of-range literal')
            else:pending.append(lit)
    if header is None or pending or len(clauses)!=header[1]:raise ValueError('Incomplete DIMACS')
    return header[0],clauses

def validate_model(n,clauses,text):
    words=text.split()
    if not words or words[0]!='SAT' or words[-1]!='0':raise ValueError('Expected SAT model')
    assignment={}
    for word in words[1:-1]:
        lit=int(word);v=abs(lit)
        if not 1<=v<=n or v in assignment:raise ValueError('Invalid/duplicate variable')
        assignment[v]=lit>0
    for i,c in enumerate(clauses):
        if not any(abs(l) in assignment and assignment[abs(l)]==(l>0) for l in c):raise ValueError(f'Unsatisfied clause {i}')
    return {'variables_assigned':len(assignment),'clauses_verified':len(clauses),'satisfies_every_clause':True}
