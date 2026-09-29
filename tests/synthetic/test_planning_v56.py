import numpy as np
import pytest
from escalation.classical_planning_v56 import grid, options, encode

def test_grid_unique_commands_and_equal_categorical_distance():
    g=grid();x=encode(g)
    assert len(g)==48 and len({tuple(options(c)) for c in g})==48
    assert x.shape==(48,11)
    assert len(set(np.abs(x[0]-x[[1,3,6,24]]).sum(axis=1)))==1
    for c in g:
        command=options(c)[-1]
        assert 'reopen_closed=true' in command and 'unsafe_pruning=false' in command
    with pytest.raises(ValueError):options(('fake','null','true','fifo'))
