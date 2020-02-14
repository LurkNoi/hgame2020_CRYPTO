#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
import binascii

BLOCKS = lambda data: [data[16*i:16*(i+1)] for i in range(len(data)//16)]
XOR = lambda s1, s2: bytes([x^y for x,y in zip(s1, s2)])

r = None
count = 0
ciphers = []

def connect():
    global r, count, ciphers
    r = remote('127.0.0.1', 1234)
    count = 3
    ciphers = []

def dec(cipher_list):
    global count
    count -= 1
    cipher = b"".join(cipher_list)
    cipher_hex = binascii.hexlify(cipher)
    r.sendlineafter('> ', cipher_hex)
    plain_hex = r.recvuntil('\n').strip()
    plain = binascii.unhexlify(plain_hex)
    plain_list = BLOCKS(plain)
    return plain_list

def getFlag():
    if count: 
        r.sendlineafter('> ', '', timeout=0.1)
    r.recvuntil('FLAG(hex): ')
    enc_hex = r.recvuntil('\n').strip()
    r.close()
    enc_flag = binascii.unhexlify(enc_hex)
    return BLOCKS(enc_flag)

ZEROS = b"\x00" * 16
msg = []

while len(msg) < 3:
    connect()
    E_IV = dec([ZEROS])[0]
    ciphers.append(E_IV)
    for m_i in msg:
        c_i = XOR(ciphers[-1], m_i)
        E_c_i = dec([c_i, ZEROS])[-1]
        ciphers.append(E_c_i)
    c = getFlag()[len(msg)]
    m = XOR(ciphers[-1], c)
    msg.append(m)
    
msg = b"".join(msg)
print( msg.decode() )

'''

connect()
E_IV = dec([ZEROS])[0]
c1 = getFlag()[0]
m1 = XOR(E_IV, c1)
print(m1)

connect()
E_IV = dec([ZEROS])[0]
c1 = XOR(E_IV, m1)
E_c1 = dec([c1, ZEROS])[-1]
c2 = getFlag()[1]
m2 = XOR(E_c1, c2)
print(m2)


connect()
E_IV = dec([ZEROS])[0]
c1 = XOR(E_IV, m1)
E_c1 = dec([c1, ZEROS])[-1]
c2 = XOR(E_c1, m2)
E_c2 = dec([c2, ZEROS])[-1]
c3 = getFlag()[2]
m3 = XOR(E_c2, c3)
print(m3)

'''