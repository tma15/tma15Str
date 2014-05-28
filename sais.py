#!/usr/bin/python
#-*- coding:utf8 -*-
import numpy as np

def classify_chartype(T):
    """ Classify charactor to L/S type: S = 1, L = 0

        Returns
        -------
        :list types: list of 0 and 1
        :list lms_ids: list of Left Most S-type
    """
    num_char = len(T)
    types = np.ones(num_char, dtype=np.int) ### S = 1, L = 0
    lms_ids = []
    for i in reversed(xrange(num_char - 1)):
        if T[i] > T[i + 1]: # T[i] is L-type
            types[i] = 0
            if types[i] == 0 and types[i + 1] == 1:
                lms_ids.insert(0, i + 1) ### position of Left Most S-charactor (LMS)
        elif T[i] == T[i + 1]:
            types[i] = types[i + 1]
    return types, lms_ids

def induced_sort(string, buckets, types, lms_ids):
    """ Step 2 """
#    print "Step 2:"
    begin_of_bucket = dict([(k, 0) for k in set(string)])
    for k, v in sorted(buckets.items(), key=lambda x:x[0]):
        for elem in v: ### from left to right
            if elem == -1: continue ### ignore initialize value
            if types[elem - 1] == 0: ### if the left character is L-type
                buckets[string[elem - 1]][begin_of_bucket[string[elem - 1]]] = elem - 1
                begin_of_bucket[string[elem - 1]] += 1 ### forward current end
#                print string[elem - 1], buckets[string[elem - 1]]
#    print
#    print "Step 3:"
    end_of_bucket = dict([(k, buckets[k].size - 1) for k in set(string)])
    for k, v in sorted(buckets.items(), key=lambda x:x[0], reverse=True):
        for elem in reversed(v): ### from right to left
            if elem == -1: continue
            if types[elem - 1] == 1 and string[elem - 1] != '$': ### if the left character is S-type
                buckets[string[elem - 1]][end_of_bucket[string[elem - 1]]] = elem - 1
                end_of_bucket[string[elem - 1]] -= 1 ### backward current end
#                print string[elem - 1], buckets[string[elem - 1]]
#    print
    return buckets


def sa_is(S):
    """
    Arguments
    =========
    :str string: the input string

    Parameters
    ==========
    :list types (t): array [0..n - 1] of boolean
    :int n_1: size of S1
    :list lms_ids (P1): array [0..n_1 - 1] of integer
        P1 is an array containing the pointers for all the LMS-substrings in S
        with their original positionaol order being preserved.
    :list S1: array [0..n_1 - 1] of integer
    :sigma_s: alphabet of S
    :list buckets (B): array [0..||sigma_s|| - 1] of integer

    Notations
    =========
    :suf(S, i): the suffix in S starting at S[i] and running to the sentinel.
    """

    """ Scan S once to classify all the characters as L- or S-type into t
    AND
    Scan t once to find all the LMS-substrings in S into P1 """
    types, lms_ids = classify_chartype(S) ### types = t, lms_ids = p1

    """ Induced sort all the LMS-substrings using P1 and B.
    1) Initialize each item of SA as -1. Find the end of each bucket in SA for all the suffixes in S
    into their buckets in SA, from the end of the head in each bucket. This is done by scanning S once
    from left to right (or right to left) and performing the following operations in O(1) time for each
    scanned LMS suffix: put the suffix's index to the current end of its bucket in SA and forward that
    bucket's end one item to the left.

    2) The same as 2) in the below.

    3) The same as 3) in the below.
    """
    counts = {} ### 何回もS.count(s)を呼ぶとO(cn)になりそうなので使わない。cはアルファベットの数
    for s in S:
        if not s in counts: counts[s] = 0
        counts[s] += 1

    buckets = {}
    for s, count in sorted(counts.items(), key=lambda x:x[0]):
        buckets[s] = -np.ones(count, dtype=np.int) ### initialize as -1

    end_of_bucket = dict([(s, -1) for s in buckets.keys()])
    for lmsid in lms_ids: ### 1)
        pre = S[lmsid] ### prefix of S[lms_ids:]
        buckets[pre][end_of_bucket[pre]] = lmsid
        end_of_bucket[pre] -= 1 ### forward current end

#    for s, bucket in sorted(buckets.items(), key=lambda x:x[0]):
#        print s, bucket

    buckets = induced_sort(S, buckets, types, lms_ids) ### 2) and 3)
#    print
#    for k, v in sorted(buckets.items(), key=lambda x:x[0]):
#        print k, v

    lms_substr = []
    for i in xrange(len(lms_ids) - 1): ### extract all LMS-substrings
        lms_substr.append(S[lms_ids[i]: lms_ids[i + 1] + 1]) ### A LMS-substring includes next LMS
    lms_substr.append(S[-1])
#    print 'LMS-substrings', lms_substr

    """ Name each LMS-substrings in S by its bucket index to get a new shortend string S1 """
    num_name = 0
    number_string = {} ### prefix id and its number name
    d = dict([(i, s) for i, s in zip(lms_ids, lms_substr)]) ### LMS and its original position
    sorted_lms_substr = []
    for _, bucket in sorted(buckets.items(), key=lambda x:x[0]):
        for pos in bucket: ### find LMS
            if pos in lms_ids:
                sorted_lms_substr.append(d[pos]) ### add LMS-substring with lexicographical order
                if num_name > 1 and sorted_lms_substr[num_name] == sorted_lms_substr[num_name - 1]:
                    num_name -= 1 ### the same LMSs have the same num_name
                number_string[pos] = num_name
                num_name += 1

    s1 = ''.join([str(v) for k, v in sorted(number_string.items(), key=lambda x:x[0])]) + "$"

#    print number_string
#    print 'LMS-substrings', lms_substr
#    print 'S', S
#    print "S1", s1
    is_unique = len(number_string.values()) == len(np.unique(number_string.values()))

    """ If each character in S1 is unique, then directly compute SA1 from S1
        else sa_is(S1, SA1)
    """
    if is_unique:
        SA1 = -np.ones(len(s1[:-1]), dtype=np.int)
        for i, pos in enumerate(s1[:-1]):
            SA1[int(pos)] = i
    else:
        SA1 = sa_is(s1)

    """ Induce SA from SA1 
    1) Initialize each item of SA as -1. Find the end of each bucket in SA for all the suffixes in S.
    Scan SA1 once from right to left, put P1[SA1[i]] to the current end of the bucket for suf(S, P1[SA1[i]])
    in SA and forward the bucket's end one item to the left.

    2) Find the head of each bucket in SA for all the suffixes in S. Scan SA from left to right, for each
    non-negative item in SA[i], if S[SA[i] - 1] is L-type, then put SA[i] - 1] to the current head of the
    bucket for suf(S, SA[i] - 1) and forward that bucket's head one item to the right.

    3) Find the end of each bucket i SA for all the suffixes in S. Scan SA from right to left, for each
    non-negative item SA[i], if S[SA[i] - 1] is S-type, then put SA[i] - 1 to the current end of the bucket
    for suf(S, SA[i] - 1) and forward that bucket's end one item to the left.
    """
    for s, count in sorted(counts.items(), key=lambda x:x[0]):
        buckets[s] = -np.ones(count, dtype=np.int)
    end_of_bucket = dict([(s, -1) for s in buckets.keys()])
    for i in reversed(SA1): ### 1)
        pre = S[lms_ids[i]] ### prefix of S[lms_ids:]
#        print 'i:%d  prefix:%s' % (lms_ids[i], pre)
#        print 'bucktet:%s' % pre, buckets[pre]
        buckets[pre][end_of_bucket[pre]] = lms_ids[i]
        end_of_bucket[pre] -= 1

    buckets = induced_sort(S, buckets, types, lms_ids) ### 2) and 3)

    SA1 = -np.ones(sum([len(bucket) for bucket in buckets.values()]), dtype=np.int) ### initialize
    i = 0
    for _, bucket in sorted(buckets.items(), key=lambda x:x[0]):
        for pos in bucket:
            SA1[i] = pos
            i += 1
    return SA1[1:]

def make(S):
    S += '$'
    return sa_is(S)

if __name__ == '__main__':
    S = 'abracadabra'
#    S = 'mmiissiissiippii'
#    S = 'mmiissiippiissii'
#    S = 'aeadacab'
#    S = 'abracadabra0AbRa4Cad14abra'
    sa = make(S)
    print sa
