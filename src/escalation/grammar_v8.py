"""Ten distinct candidate IDs; real model logits choose among remaining IDs."""
from .grammar_v6 import FiniteSymbolsGrammar
from .io import digest

class CandidateIDGrammar(FiniteSymbolsGrammar):
    def __init__(self, tokenizer):
        super().__init__(tokenizer, [list(range(20))])
        self.choice_set = set(self.choice_positions)
        self.sha256 = digest({'schedule': self.schedule, 'rule': 'ten_distinct_candidate_ids_v8'})

    def allowed_after(self, generated):
        position = len(generated)
        allowed = self.allowed(position)
        if position in self.choice_set:
            used = {generated[i] for i in self.choice_positions if i < position}
            allowed = [token for token in allowed if token not in used]
        return allowed

    def constraint(self, prompt_length):
        return lambda batch, ids: self.allowed_after(ids[prompt_length:].tolist())

    def replay(self, generated):
        if len(generated) != len(self.schedule):
            raise ValueError('incomplete ID grammar')
        trace = []
        for position, token in enumerate(generated):
            options = self.allowed_after(generated[:position])
            if token not in options:
                raise ValueError('invalid or duplicate candidate token')
            if position in self.choice_set:
                trace.append({'position': position, 'allowed': options, 'chosen': token})
        return trace
