from itertools import chain, permutations
from graphviz import Digraph
from argparse import ArgumentParser


def F1(j1, j2, seq):
    j1_idx = seq.index(j1)
    if j1_idx == len(seq) - 1:
        seq.remove(j1)
        seq.insert(0, j1) 
    else:
        seq.remove(j1)
        seq.insert(j1_idx + 1, j1)
    return seq

def F01(j1, j2, seq):
    j1_idx = seq.index(j1)
    if j1_idx == len(seq) - 1:
        seq.remove(j1)
        seq.insert(1, j1) 
    else:
        seq.remove(j1)
        seq.insert(j1_idx + 1, j1)
    return seq

def F02(j1, j2, seq):
    j2_idx = seq.index(j2)
    if j2_idx == len(seq) - 1:
        seq.remove(j2)
        seq.insert(2, j2) 
    elif j2_idx + 2 == len(seq):
        seq.remove(j2)
        seq.insert(1, j2) 
    else:
        seq.remove(j2)
        seq.insert(j2_idx + 2, j2)
    return seq


def F2(j1, j2, seq):
    j2_idx = seq.index(j2)
    if j2_idx == len(seq) - 1:
        seq.remove(j2)
        seq.insert(0, j2) 
    elif j2_idx + 2 == len(seq):
        seq.remove(j2)
        seq.insert(1, j2) 
    else:
        seq.remove(j2)
        seq.insert(j2_idx + 2, j2)
    return seq

def F3(j1, j2, seq):
    j1_idx = seq.index(j1)
    j2_idx = seq.index(j2)
    if j1_idx < j2_idx:
        left_idx = j1_idx
        right_idx = j2_idx
    else:
        left_idx = j2_idx
        right_idx = j1_idx
    left = seq[0:left_idx] 
    right = seq[right_idx + 1:len(seq)]
    middle = seq[left_idx:right_idx + 1]
    return list((k for k in chain(right, middle, left)))

def F4(mapper, j1, j2, seq):
    if j1 == seq[-1] or j2 == seq[-1]:
        return seq
    sym = seq[-1]
    sym_num = mapper(sym)
    left = seq[0:sym_num]
    right = seq[sym_num: -1]
    return list((k for k in chain(right, left, (sym,))))



seq = ['0', '1', '2', '3']
sym_table = { '0' : 1, '1': 2, '2': 3, '3': 3 }
mapper = lambda x: sym_table[x]

j1 = '2'
j2 = '3'
f1 = lambda x: F1(j1, j2, x)
f2 = lambda x: F2(j1, j2, x) 
f3 = lambda x: F3(j1, j2, x)
f4 = lambda x: F4(mapper, j1, j2, x)
f01 = lambda x: F01(j1, j2, x)
f02 = lambda x: F02(j1, j2, x)
ops = { 'F1': f1, 'F2': f2, 'F3': f3, 'F4': f4, 'F01': f01, 'F02': f02 }
parser = ArgumentParser()
parser.add_argument('ops_seq',metavar='F...', nargs='+', type=str)
args, _ = parser.parse_known_args()
ops_chain = [ops[op] for op in args.ops_seq]
dot = Digraph(comment='ETO GRAPH')
nodes = set() 
for p in permutations(seq):
    node_begin_id = ''.join(p) 

    if not node_begin_id in nodes:
        nodes.add(node_begin_id)
        dot.node(node_begin_id)
    
    begin = p
    sequence = list(p)
    for i in range(0, len(ops_chain)):
        print(f'{sequence} ->', end = ' ')
        op = ops_chain[i]
        sequence = op(sequence)
    end = tuple(sequence)
    node_end_id = ''.join(end)
    print(sequence) 
    if not node_end_id in nodes:
        nodes.add(node_end_id)
        dot.node(node_end_id)
    dot.edge(node_begin_id, node_end_id) 

dot.render('out.gv', view=True)





