#!/usr/bin/python
#-*- coding:utf8 -*-
import sais
from nose.tools import eq_

def test_sais():
    S = 'mmiissiissiippii'
    res = [15, 14, 10, 6, 2, 11, 7, 3, 1, 0, 13, 12, 9, 5, 8, 4]
#    sa = sais.sa_is(S)
    sa = sais.make(S)
    eq_(list(sa), res)

    S = 'mmiissiippiissii'
    res = [15, 14, 6, 10, 2, 7, 11, 3, 1, 0, 9, 8, 13, 5, 12, 4]
#    sa = sais.sa_is(S)
    sa = sais.make(S)
    eq_(list(sa), res)

    S = 'abracadabra'
    res = [10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]
#    sa = sais.sa_is(S)
    sa = sais.make(S)
    eq_(list(sa), res)

    S = 'aeadacab'
    res = [6, 4, 2, 0, 7, 5, 3, 1]
#    sa = sais.sa_is(S)
    sa = sais.make(S)
    eq_(list(sa), res)

    S = 'abracadabra0AbRa4Cad14abra'
    res = [11, 20, 16, 21, 12, 17, 14, 25, 10, 15, 22, 7, 0, 3, 18, 5, 13, 23, 8, 1, 4, 19, 6, 24, 9, 2]
#    sa = sais.sa_is(S)
    sa = sais.make(S)
    eq_(list(sa), res)

