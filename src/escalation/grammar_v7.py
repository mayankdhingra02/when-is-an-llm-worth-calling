"""Feature-only exclusion of original acquired-prefix configurations.

This is an explicit optimizer constraint, not merely a syntax constraint. It
never uses objective values and does not ban repeated novel rows within a batch.
"""
import hashlib,json,math,random
from .grammar_v6 import FiniteSymbolsGrammar
from .finite_v6 import ALPHABET

class PrefixExcludingGrammar(FiniteSymbolsGrammar):
    def __init__(self,tokenizer,domains,forbidden):
        super().__init__(tokenizer,domains)
        self.domains=domains;self.positions={};self.row_positions=[];self.forbidden=set()
        offset=0;newline=len(tokenizer.encode('\n',add_special_tokens=False))
        for row in range(10):
            positions=list(range(offset,offset+len(domains)));self.row_positions.append(positions)
            for col,pos in enumerate(positions):self.positions[pos]=(row,col)
            offset+=len(domains)+newline
        tokens=[self.schedule[p] for p in self.row_positions[0]]
        for text in forbidden:
            if not isinstance(text,str) or len(text)!=len(domains):raise ValueError('forbidden row shape')
            row=[]
            for col,symbol in enumerate(text):
                if symbol not in ALPHABET[:len(domains[col])]:raise ValueError('forbidden symbol outside domain')
                row.append(tokens[col][ALPHABET.index(symbol)])
            self.forbidden.add(tuple(row))
        if len(self.forbidden)>=math.prod(map(len,domains)):raise ValueError('all domain combinations forbidden')
        self.tail_counts=[math.prod(len(d) for d in domains[j+1:]) for j in range(len(domains))]
        self.base_sha256=self.sha256
        self.sha256=hashlib.sha256(json.dumps({'base':self.base_sha256,'forbidden_tokens':sorted(self.forbidden),'rule':'original_prefix_only_v7'},sort_keys=True).encode()).hexdigest()
    def allowed_after(self,generated):
        pos=len(generated);base=self.allowed(pos)
        if pos not in self.positions:return base
        row,col=self.positions[pos];prefix=tuple(generated[p] for p in self.row_positions[row][:col])
        matching=[f for f in self.forbidden if f[:col]==prefix]
        result=[token for token in base if sum(f[col]==token for f in matching)<self.tail_counts[col]]
        if not result:raise ValueError('no legal unobserved completion')
        return result
    def constraint(self,prompt_length):
        def allowed_tokens(batch_id,ids):return self.allowed_after(ids[prompt_length:].tolist())
        return allowed_tokens
    def replay(self,generated):
        trace=[]
        for pos,token in enumerate(generated):
            options=self.allowed_after(generated[:pos])
            if token not in options:raise ValueError('token violates dynamic exclusion')
            if options!=self.schedule[pos]:trace.append({'position':pos,'base':self.schedule[pos],'allowed':options})
        return trace

def uniform_without_prefix(domains,forbidden,seed,count=10):
    """Exact uniform Cartesian sampling conditioned on avoiding the prefix.

Select a uniform rank in the sorted complement, then decode mixed radix. No
rejection-loop timeout or dependence on objective values. Repeated novel rows
within the ten-row batch remain possible, as with the model treatment.
"""
    dims=[len(d) for d in domains]
    if not dims or any(n<=0 for n in dims):raise ValueError('empty domains')
    blocked=set()
    for text in forbidden:
        if len(text)!=len(dims):raise ValueError('forbidden shape')
        rank=0
        for n,symbol in zip(dims,text):
            if symbol not in ALPHABET[:n]:raise ValueError('invalid forbidden symbol')
            rank=rank*n+ALPHABET.index(symbol)
        blocked.add(rank)
    total=math.prod(dims)-len(blocked)
    if total<=0:raise ValueError('all forbidden')
    rng=random.Random(seed);result=[]
    for _ in range(count):
        rank=rng.randrange(total)
        for b in sorted(blocked):
            if b<=rank:rank+=1
            else:break
        indices=[]
        for n in reversed(dims):indices.append(rank%n);rank//=n
        result.append([d[j] for d,j in zip(domains,reversed(indices))])
    return result
