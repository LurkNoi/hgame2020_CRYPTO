#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gmpy2 import invert

TABLE = 'zxcvbnmasdfghjklqwertyuiop1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
MOD = len(TABLE)
cipher = 'A8I5z{xr1A_J7ha_vG_TpH410}'

C2I = TABLE.find
A = (C2I('A') - C2I('8')) * invert(C2I('h')-C2I('g'), MOD) % MOD
B = (C2I('A') - A*C2I('h')) % MOD
A_inv = invert(A, MOD)

flag = ''
for c in cipher:
    ii = TABLE.find(c)
    if ii == -1:
        flag += c
    else:
        i = (ii - B) * A_inv % MOD
        flag += TABLE[i]

print('flag:', flag)