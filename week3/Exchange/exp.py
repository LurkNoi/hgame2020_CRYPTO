#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, string
from hashlib import sha256
from pwn import *
from pwnlib.util.iters import mbruteforce

from Crypto.Util import number
import gmpy2, random

# context.log_level = 'debug'

r = remote('127.0.0.1', 12345)

PoW = r.recvline().decode()
suffix, target_hexdigest  = re.search(r'\(XXXX\+(\w{16})\) == (\w{64})', PoW).groups()

proof = mbruteforce(lambda x: sha256( (x+suffix).encode() ).hexdigest()==target_hexdigest, string.ascii_letters+string.digits, length = 4, method = 'fixed')
r.sendlineafter('Give me XXXX: ', proof)

r.sendlineafter('Key Exchange first.\n\n', '')

pubParm = r.recvregex(r'g = (\d+)\n\n').decode()
p, g = map(int, re.search(r'p = (\d+)\nAlice: g = (\d+)\n', pubParm).groups())

log.info('p: '+str(p))
log.info('g: '+str(g))

r.sendline('')
r.sendline('')

c = random.randint(2, p-2)
C = pow(g, c, p)

A_str = r.recvuntil('(yes/no)').decode()
A = int( re.search(r'A = (\d+)\n', A_str).groups()[0] )
log.info('A: '+str(A))
r.sendlineafter('> ', 'yes')
r.sendlineafter('> ', str(C))

S_a = pow(A, c, p)

r.sendline('')

B_str = r.recvuntil('(yes/no)').decode()
B = int( re.search(r'B = (\d+)\n', B_str).groups()[0] )
log.info('B: '+str(B))
r.sendlineafter('> ', 'yes')
r.sendlineafter('> ', str(C))

S_b = pow(B, c, p)

for _ in range(4):
    r.sendlineafter('\n\n', '')

C_b_str = r.recvuntil('(yes/no)').decode()
C_b = int( re.search(r'C_b = (\d+)\n', C_b_str).groups()[0] )
log.info('C_b: '+str(C_b))
m_b = (C_b * gmpy2.invert(S_b, p)) % p
print( number.long_to_bytes(m_b) )
C_bb = (m_b * S_a) % p
r.sendlineafter('> ', 'yes')
r.sendlineafter('> ', str(C_bb))

C_a_str = r.recvregex(r'C_a = (\d+)\n').decode()
C_a = int( re.search(r'C_a = (\d+)\n', C_a_str).groups()[0] )
log.info('C_a: '+str(C_a))
m_a = (C_a * gmpy2.invert(S_a, p)) % p
print( number.long_to_bytes(m_a) )

log.info('flag: ' + number.long_to_bytes(m_a).decode() + number.long_to_bytes(m_b).decode())

# r.interactive()

r.close()
