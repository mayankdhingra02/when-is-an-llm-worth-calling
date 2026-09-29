"""Syntax constraints only: every nonconstant setting comes from model logits."""
import hashlib,json
from .finite_v6 import ALPHABET
from .grammar import BinaryJSONGrammar

class FiniteSymbolsGrammar:
    def __init__(self,tokenizer,domains,count=10):
        if count!=10 or not 1<=len(domains)<=64 or any(not d or len(d)>len(ALPHABET) or len(d)!=len(set(d)) for d in domains):raise ValueError('unsupported domains')
        self.schedule=[];self.choice_positions=[]
        for row in range(count):
            if row:
                ids=tokenizer.encode('\n',add_special_tokens=False)
                if tokenizer.decode(ids)!='\n':raise ValueError('newline roundtrip')
                self.schedule.extend([[v] for v in ids])
            for domain in domains:
                tokens=[]
                for letter in ALPHABET[:len(domain)]:
                    ids=tokenizer.encode(letter,add_special_tokens=False)
                    if len(ids)!=1 or tokenizer.decode(ids)!=letter:raise ValueError('single symbol token required')
                    tokens.append(ids[0])
                if len(tokens)>1:self.choice_positions.append(len(self.schedule))
                self.schedule.append(tokens)
        self.schedule.append([tokenizer.eos_token_id])
        self.sha256=hashlib.sha256(json.dumps(self.schedule).encode()).hexdigest()
        if len(self.schedule)>1024:raise ValueError('output cap')
    allowed=BinaryJSONGrammar.allowed
    constraint=BinaryJSONGrammar.constraint
