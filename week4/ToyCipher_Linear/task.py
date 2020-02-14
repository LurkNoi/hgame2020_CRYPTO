#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, binascii

from secret import flag

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


def encrypt(plaintext):
    '''ECB mode'''
    plaintext = pad(plaintext, BLOCKSIZE)
    ciphertext = b''
    for i in range( len(plaintext) // BLOCKSIZE ):
        block = plaintext[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
        block = int.from_bytes(block, byteorder='big')
        E_block = ToyCipher(block)
        ciphertext += E_block.to_bytes(BLOCKSIZE, byteorder='big')
    return ciphertext


def decrypt(ciphertext):
    '''ECB mode'''
    plaintext = b''
    for i in range( len(ciphertext) // BLOCKSIZE ):
        block = ciphertext[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
        block = int.from_bytes(block, byteorder='big')
        D_block = ToyCipher(block, 'dec')
        plaintext += D_block.to_bytes(BLOCKSIZE, byteorder='big')
    plaintext = unpad(plaintext, BLOCKSIZE)
    return plaintext


masterkey = os.urandom(8)
masterkey = int.from_bytes(masterkey, byteorder='big')
ROUNDKEYS = keySchedule(masterkey)
BLOCKSIZE = 4

cipher = encrypt(b'just a test')

print(cipher)
print(decrypt(cipher))
print(encrypt(flag))

# b'\x91a\xb1o\xed_\xb2\x8c\x00\x1b\xdfp'
# b'just a test'
# b'\xe6\xf9\xda\xf0\xe18\xbc\xb4[\xfb\xbe\xd1\xfe\xa2\t\x8d\xdft:\xee\x1f\x1d\xe2q\xe5\x92/$#DL\x00\x1dD5@\x01W?!7CQ\xc16V\xb0\x14q)\xaa2'