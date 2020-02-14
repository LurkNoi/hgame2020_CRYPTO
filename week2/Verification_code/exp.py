#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, string
from hashlib import sha256
from pwn import *
from pwnlib.util.iters import mbruteforce


r = remote('127.0.0.1', 25003)

PoW = r.recvline().decode()
suffix, target_hexdigest  = re.search(r'\(XXXX\+(\w{16})\) == (\w{64})', PoW).groups()

proof = mbruteforce(lambda x: sha256( (x+suffix).encode() ).hexdigest()==target_hexdigest, string.ascii_letters+string.digits, length = 4, method = 'fixed')
r.sendlineafter('Give me XXXX: ', proof)

r.sendlineafter('> ', 'I like playing Hgame')
print( r.recvregex('hgame{.+}').decode() )

r.close()
