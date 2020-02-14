#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import binascii


from secret import FLAG


BLOCKSIZE = 8
BITSLENGTH = 8*BLOCKSIZE
MASK = (1 << BITSLENGTH) - 1

BLOCKS = lambda data: [ bytes(data[i*BLOCKSIZE:(i+1)*BLOCKSIZE]) for i in range(len(data)//BLOCKSIZE) ]
XOR = lambda s1, s2: bytes([x^y for x,y in zip(s1, s2)])


def pad(data):
    pad_len = BLOCKSIZE - (len(data) % BLOCKSIZE)
    return data + bytes( [pad_len] * pad_len )


def f(x, a, shr=True):
    x = x & MASK
    a = a % BITSLENGTH
    if shr:
        x ^= x >> a
    else:
        x ^= x << a
    return x & MASK


def enc(block):
    block = int.from_bytes(block, byteorder='big')
    block = f(block, 13, shr=False)
    block = f(block,  7, shr=True )
    block = f(block, 17, shr=False)
    return block.to_bytes(BLOCKSIZE, byteorder='big')


def encrypt(msg, iv):
    msg = pad(msg)
    mid = iv
    cipher = b''
    for block in BLOCKS(msg):
        mid = enc( XOR(mid, block) )
        cipher += mid
    return cipher


def decrypt(cipher, iv, unpad=False):
    assert len(cipher)%BLOCKSIZE == 0
    pass

IV = b'c8C~M0d3'
ciphertext = encrypt(FLAG, IV)
print( ciphertext.hex() )

# 15eb80358fe6f89b1802a5f3eb5a6ec6c33dc4f35822fb6e97e0b22be860a28602b35e2930a93ac5
