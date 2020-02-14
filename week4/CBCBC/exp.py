#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import string, binascii
import re
from hashlib import sha256
from pwn import *
from pwnlib.util.iters import mbruteforce


BLOCKS = lambda data: [data[16*i:16*(i+1)] for i in range(len(data)//16)]


def proof_of_work():
    PoW = r.recvline().decode()
    suffix, target_hexdigest  = re.search(r'\(XXXX\+(\w{16})\) == (\w{64})', PoW).groups()
    proof = mbruteforce(lambda x: sha256( (x+suffix).encode() ).hexdigest()==target_hexdigest, string.ascii_letters+string.digits, length=4, method='fixed')
    r.sendlineafter('Give me XXXX: ', proof)


count = 0
def check_padding(data_list):
    global count
    count += 1
    data = b''.join(data_list)
    data_hex = binascii.hexlify(data)
    r.sendlineafter('> ', data_hex)
    response = r.recvuntil('\n')
    if b'done' in response:
        return True
    elif b'wrong' in response:
        return False


def byte_flip(ctrl_block, i_pos, plain, target):
    ctrl_block = list(ctrl_block)
    for i in range(1, i_pos+1):
        ctrl_block[-i] = ctrl_block[-i] ^ plain[-i] ^ target[-i]
    return bytes(ctrl_block)


PLAIN_SPACE = b'\x04_{}' + (string.digits+string.ascii_letters+string.punctuation).encode()


def decrypt_block(blocks):
    plain = b''
    while len(plain) < 16:
        for i in PLAIN_SPACE:
            pad_len = len(plain) + 1
            flip_data = byte_flip(blocks[-3], pad_len, bytes([i])+plain, bytes([pad_len]*pad_len))
            new_data = blocks[:-3] + [flip_data] + blocks[-2:]
            if check_padding(new_data):
                plain = bytes([i])+plain
                print(len(plain), plain)
                break
        else:
            raise ValueError("Not Found")
    return plain


def decrypt(data):
    msg = b''
    blocks = BLOCKS(data)
    while len(blocks) >= 3:
        plain = decrypt_block(blocks[-4:])
        msg = plain + msg
        blocks = blocks[:-1]
    return msg


def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]


if __name__ == "__main__":
    r = remote('47.98.192.231', 25300)
    proof_of_work()
    
    r.recvuntil('(in hex) is ')
    enc_flag = binascii.unhexlify( r.recvuntil('\n').strip() )
    
    print( unpad(decrypt(enc_flag)).decode() )
    print(count)
    
    r.close()