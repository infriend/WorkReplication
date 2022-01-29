import re

"""
We only need pattern: n at ns, at can be any synonyms in Chinese.
Combine continuous n or ns to get one long attribute value.
Specifically, for each sentence, only w(n) w(n+1) w(n+2) matches n pattern ns, we can get the triple.
"""

# We may take n and ns as (), use stack to solve it. But here for convenience just take the most inside pair.
def position_patternmatch(seg_list, pos_list):
    """
    Input: sentence and its pos.
    Output: Triple if fits the pattern, or return None.
    """
    with open("./data/triggers_filtered.txt", 'r') as f:
        position_pattern = f.read()
        position_pattern = position_pattern.split('\n')

    triples = []

    n_flag = 0
    n_pos = 0

    ns_pos = 0
    match = 0
    for sid in range(len(seg_list)):
        for i in range(len(seg_list[sid])):
            if (pos_list[sid][i] == 'n' or pos_list[sid][i] == 'ns') and n_flag == 0:
                n_flag = 1  # pos n matched
                n_pos = i
                i += 1
            else:
                continue

            if i < len(seg_list[sid]) and match == 0:
                for p in position_pattern:
                    if re.search(p, seg_list[sid][i]):
                        match = 1  # pattern matched

                if match == 0:
                    continue
                else:
                    i += 1

            if i < len(seg_list[sid]):
                if (pos_list[sid][i] == 'n' or pos_list[sid][i] == 'ns') and n_flag == 1 and match == 1:
                    n_flag = 0
                    match = 0
                    ns_pos = i
                    e1 = seg_list[sid][n_pos].replace('↑', '')
                    e2 = seg_list[sid][i].replace('↑', '')
                    triples.append((e1, 'at', e2))
                    continue
                else:
                    n_flag = 0
                    match = 0

    return triples
