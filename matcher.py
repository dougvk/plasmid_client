import glob
from pickle import dumps
import re
from string import maketrans
from collections import defaultdict

from suffix_tree import GeneralisedSuffixTree

#@click.command()
#@click.option('--sequence', '-s', help='target search sequence', type=str)
def match_seq():
    with open('args') as f:
        sequence = str(f.read()).strip()
    SOLUTION_DICT = defaultdict(set)

    trans_table = maketrans('acgt', 'tgca')
    search_seq = str(sequence.lower()) * 2
    search_seq_comp = search_seq.translate(trans_table)[::-1]

    chunk_dict = match_seq_helper(0, len(search_seq), search_seq,
                                  search_seq_comp)
    merge_chunks(chunk_dict, SOLUTION_DICT)

    seq, solution, offset = get_solution_blocks(SOLUTION_DICT,
                                                len(search_seq) / 2, search_seq)
    print dumps({'results': solution, 'offset': offset, 'sequence': seq})

def get_solution_blocks(SOLUTION_DICT, max_length, search_seq):
    chunk_list = [eval(item) for item in dict(SOLUTION_DICT).keys()]
    min_idx = min([min(x) for x in chunk_list])
    max_idx = max([max(x) for x in chunk_list])
    shifted_seq = search_seq[min_idx:max_idx]
    shifted_solution_dict = (lambda x=min_idx:
                             {str((eval(k)[0] - x, eval(k)[1] - x)): list(v)
                              for k, v in SOLUTION_DICT.iteritems()})()

    return (shifted_seq, shifted_solution_dict, min_idx)

def merge_chunks(chunk_dict, SOLUTION_DICT):
    for k, v in chunk_dict.iteritems():
        v = (v[0], v[1])
        SOLUTION_DICT[str(v)].add(k)

#@profile
def match_seq_helper(start, end, search_seq, search_seq_comp):
    chunk_dict = {}
    extract_dna = re.compile(r'[actg]{40,}')
    plasmid_dict = {}
    for fn in glob.glob('sequence_files/*.sbd'):
        with open(fn) as f:
            dirty_seq = f.readline().lower()
            seq = extract_dna.findall(dirty_seq)[0] * 2
            plasmid_dict[fn] = seq
    for fn, seq in plasmid_dict.iteritems():
        sequences = [seq, search_seq]
        stree = GeneralisedSuffixTree(sequences)
        biggest = 0
        for shared in stree.sharedSubstrings():
            for seq, start, stop in shared:
                if seq == 1:
                    if stop - start > biggest:
                        biggest = stop - start
        if biggest > 200:
            for shared in stree.sharedSubstrings(biggest):
                for seq, start, stop in shared:
                    if seq == 1:
                        if fn in chunk_dict:
                            chunk_idx = chunk_dict[fn]
                            if biggest > chunk_idx[1] - chunk_idx[0]:
                                chunk_dict[fn] = (start, stop)
                        else:
                            chunk_dict[fn] = (start, stop)
    for fn, seq in plasmid_dict.iteritems():
        sequences = [seq, search_seq_comp]
        stree = GeneralisedSuffixTree(sequences)
        biggest = 0
        for shared in stree.sharedSubstrings():
            for seq, start, stop in shared:
                if seq == 1:
                    if stop - start > biggest:
                        biggest = stop - start
        if biggest > 200:
            for shared in stree.sharedSubstrings(biggest):
                for seq, start, stop in shared:
                    if seq == 1:
                        if fn in chunk_dict:
                            chunk_idx = chunk_dict[fn]
                            if biggest > chunk_idx[1] - chunk_idx[0]:
                                chunk_dict[fn] = (start, stop)
                        else:
                            chunk_dict[fn] = (start, stop)
    return chunk_dict

if __name__ == '__main__':
    match_seq()
