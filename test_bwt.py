#!/usr/bin/python
#-*- coding:utf8 -*-
import bwt
from nose.tools import eq_

def test_bwt():
    S = 'acadabra$'
    res = 'ard$caaab'
    tb = bwt.bwt_incremental(S)
    eq_(tb, res)

    S = 'acadabra$'
    res = 'ard$caaab'
    tb = bwt.bwt_incremental(S)
    eq_(tb, res)
