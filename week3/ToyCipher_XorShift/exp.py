#!/usr/bin/env python3
# -*- coding: utf-8 -*-

BLOCKSIZE = 8
BITSLENGTH = 8*BLOCKSIZE
MASK = (1 << BITSLENGTH) - 1

BLOCKS = lambda data: [ bytes(data[i*BLOCKSIZE:(i+1)*BLOCKSIZE]) for i in range(len(data)//BLOCKSIZE) ]
XOR = lambda s1, s2: bytes([x^y for x,y in zip(s1, s2)])

def f_inv(x, a, shr):
    x = x & MASK
    a = a % BITSLENGTH
    y = 0
    while x:
        y ^=x
        if shr:
            x >>= a
        else:
            x <<= a
        x &= MASK
    return y & MASK

def dec(block):
    block = int.from_bytes(block, byteorder='big')
    block = f_inv(block, 17, shr=False)
    block = f_inv(block,  7, shr=True )
    block = f_inv(block, 13, shr=False)
    return block.to_bytes(BLOCKSIZE, byteorder='big')


def decrypt(cipher, iv):
    assert len(cipher)%BLOCKSIZE == 0
    msg = b''
    mid = iv
    for block in BLOCKS(cipher):
        _block = dec(block)
        msg += XOR(mid, _block)
        mid = block
    return msg

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]


IV = b'c8C~M0d3'
enc_flag = bytes.fromhex('15eb80358fe6f89b1802a5f3eb5a6ec6c33dc4f35822fb6e97e0b22be860a28602b35e2930a93ac5')
flag = unpad( decrypt(enc_flag, IV) )

print(flag.decode())
