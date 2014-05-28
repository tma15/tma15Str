#!/usr/bin/python
#-*- coding:utf8 -*-
import numpy as np
import sys

import sais


def bwt_transform(S):
    sa = sais.make(S)
    S_b = ''
    for i in xrange(sa.shape[0]):
        if sa[i] == 0:
            S_b += S[-1]
        else:
            S_b += S[sa[i] - 1]
    return S_b

def insert(current_list, p, elem):
    new_list = current_list[:p]
    new_list.append(elem)
    new_list += current_list[p:]
    return new_list

def rank(ch, Tb, p):
    return Tb[:p].count(ch)
    
def bwt_incremental(S):
    num_char = len(S)
    p = 0
    Tb = []
    count = dict([(ch, 0) for ch in set(S)])
    suffixes = []
    suffix = ''

    for i in xrange(num_char):
        i += 1
        ch = S[num_char - i]
        suffix = "%s%s" % (ch, suffix)
        if Tb:
            prev_ch = Tb[p]
            Tb[p] = ch
            p = rank(ch, Tb, p) + sum([v for k, v in count.items() if k < ch])
            Tb = insert(Tb, p, prev_ch)
            suffixes = insert(suffixes, p, suffix)
        else: # i = 1
            Tb.append(ch)
            suffixes.append(suffix)
        count[ch] += 1
    return ''.join(Tb)

if __name__ == '__main__':
    T = 'abracadabra$'
    T = 'acadabra$'
#    T = 'cadabra$'
#    T = 'adabra$'
#    T = 'dabra$'
#    T = 'abra$'
#    T = 'bra$'
#    T = 'ra$'
#    T = 'a$'
#    print T
    tb = bwt_incremental(T)
    print tb
#    s_b = bwt_transform(T+"$")
#    print s_b
