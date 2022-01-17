import re

"""
We only need pattern: n at ns, at can be any synonyms in Chinese.
Combine continuous n or ns to get one long attribute value.
Specifically, for each sentence, only w(n) w(n+1) w(n+2) matches n pattern ns, we can get the triple.
"""
position_pattern = "位于"


# We may take n and ns as (), use stack to solve it. But here for convenience just take the most inside pair.
def position_patternmatch(seg_list, pos_list):
    """
    Input: sentence and its pos.
    Output: Triple if fits the pattern, or return None.
    """
    triples = []

    n_flag = 0
    n_pos = 0

    ns_pos = 0
    match = 0
    for i in range(len(seg_list)):
        if pos_list[i] == 'n' and n_flag == 0:
            n_flag = 1  # pos n matched
            n_pos = i
            continue

        if re.search(position_pattern, seg_list[i]):
            match = 1  # pattern matched
            continue
        else:
            n_flag = 0

        if pos_list[i] == 'ns' and n_flag == 1 and match == 1:
            n_flag = 0
            match = 0
            ns_pos = i
            triples.append(set(seg_list[n_pos], 'at', seg_list[ns_pos]))
            continue
        else:
            n_flag = 0
            match = 0

    return triples
