#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import string, binascii, base64
from socket import socket

keySpace = string.ascii_letters + string.digits

count = 0
def enc():
    global count
    count += 1
    sock = socket()
    sock.connect(('127.0.0.1', 1234))
    return base64.b64decode( sock.recv(1024) )


LEN = len(enc())

flag = [set(b'h'), set(b'g'), set(b'a'), set(b'm'), set(b'e'), set(b'{'), \
    *([set(string.printable.encode()) for _ in range(LEN-7)]), \
    set(b'}')]


def check():
    return sum(map(len, flag))==LEN


def guess(cipher):
    return bytes([ cipher^k for k in keySpace.encode() ])


def update(index, s):
    global flag
    flag[index] = flag[index] & set(s)


while check()!=True:
    cipher = enc()
    for i in range(LEN):
        m_i = guess(cipher[i])
        update(i, m_i)

print( count, 'flag:', ''.join( map(lambda x: chr(next(iter(x))), flag) ) )