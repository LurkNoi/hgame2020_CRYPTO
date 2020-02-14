#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def rotL(x, nbits, lbits):
    mask = 2**nbits - 1
    return (x << lbits%nbits) & mask | ( (x & mask) >> (-lbits % nbits) )


def rotR(x, nbits, rbits):
    return rotL(x, nbits, -rbits%nbits)


def keySchedule(masterkey):
    roundKeys = [ ( rotR(masterkey, 64, 16*i) % 2**16 ) for i in range(12) ]
    return roundKeys


def f(x, roundkey):
    return rotL(x, 16, 7) ^ rotL(x, 16, 2) ^ roundkey


def ToyCipher(block, mode='enc'):
    '''Feistel networks'''
    roundKeys_ = ROUNDKEYS
    if mode == 'dec':
        roundKeys_ = roundKeys_[::-1]

    L, R = (block >> 16), (block % 2**16)
    for i in range(12):
        _R = R
        R = L ^ f( R, roundKeys_[i] )
        L = _R

    return (R << 16) | L


def pad(data, blocksize):
    pad_len = blocksize - (len(data) % blocksize)
    return data + bytes( [pad_len] * pad_len )


def unpad(data, blocksize):
    pad_len = data[-1]
    _data = data[:-pad_len]
    assert pad(_data, blocksize)==data, "Invalid padding."
    return _data


c = b'\xe6\xf9\xda\xf0\xe18\xbc\xb4[\xfb\xbe\xd1\xfe\xa2\t\x8d\xdft:\xee\x1f\x1d\xe2q\xe5\x92/$#DL\x00\x1dD5@\x01W?!7CQ\xc16V\xb0\x14q)\xaa2'
c = [ c[i*4:(i+1)*4] for i in range(len(c)//4) ]
m0 = b'just'
m0 = int.from_bytes(m0, 'big')
c0 = b'\x91a\xb1o\xed_\xb2\x8c\x00\x1b\xdfp'[:4]
c0 = int.from_bytes(c0, 'big')

masterkey = 0
ROUNDKEYS = keySchedule(masterkey)
BLOCKSIZE = 4

def dec(cipher):
    c = int.from_bytes(cipher, 'big')
    m = m0 ^ ToyCipher(c0^c, 'dec')
    return m.to_bytes(4, 'big')

print( unpad(b''.join(map(dec,c)), BLOCKSIZE) )