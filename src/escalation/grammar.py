"""Token-position syntax constraints. All optimization choices remain model logits."""
import hashlib,json

class BinaryJSONGrammar:
    def __init__(self,tokenizer,domains):
        if not domains or any(not d or any(v not in (0,1) for v in d) for d in domains):
            raise ValueError('grammar supports complete binary domains only')
        self.schedule=[];self.choice_positions=[]
        def literal(text):
            ids=tokenizer.encode(text,add_special_tokens=False)
            if tokenizer.decode(ids)!=text:raise ValueError('literal round trip failed')
            self.schedule.extend([[i] for i in ids])
        literal('{"candidates":[')
        for row in range(2):
            literal('[' if row==0 else ',[')
            for j,domain in enumerate(domains):
                if j:literal(',')
                choices=[]
                for value in sorted(set(domain)):
                    ids=tokenizer.encode(str(int(value)),add_special_tokens=False)
                    if len(ids)!=1 or tokenizer.decode(ids)!=str(int(value)):raise ValueError('binary value must be one token')
                    choices.append(ids[0])
                self.choice_positions.append(len(self.schedule));self.schedule.append(choices)
            literal(']')
        literal(']}');self.schedule.append([tokenizer.eos_token_id])
        self.sha256=hashlib.sha256(json.dumps(self.schedule).encode()).hexdigest()
        if len(self.schedule)>1024:raise ValueError('grammar exceeds output cap')
    def allowed(self,position):
        if not 0<=position<len(self.schedule):raise ValueError('out of grammar bounds')
        return self.schedule[position]
    def constraint(self,prompt_length):
        def allowed_tokens(batch_id,ids):
            return self.allowed(len(ids)-prompt_length)
        return allowed_tokens

class BinaryLinesGrammar:
    """Five rows of binary coordinate tokens; only newline/EOS are syntax."""
    def __init__(self,tokenizer,domains,count=5):
        if count!=5 or not domains or any(not d or any(v not in (0,1) for v in d) for d in domains):raise ValueError('expected five rows of binary domains')
        self.schedule=[];self.choice_positions=[]
        for row in range(count):
            if row:self.schedule.extend([[v] for v in tokenizer.encode('\n',add_special_tokens=False)])
            for domain in domains:
                choices=[]
                for value in sorted(set(domain)):
                    ids=tokenizer.encode(str(int(value)),add_special_tokens=False)
                    if len(ids)!=1 or tokenizer.decode(ids)!=str(int(value)):raise ValueError('binary single token required')
                    choices.append(ids[0])
                self.choice_positions.append(len(self.schedule));self.schedule.append(choices)
        self.schedule.append([tokenizer.eos_token_id]);self.sha256=hashlib.sha256(json.dumps(self.schedule).encode()).hexdigest()
        if len(self.schedule)>1024:raise ValueError('output cap')
    allowed=BinaryJSONGrammar.allowed
    constraint=BinaryJSONGrammar.constraint
