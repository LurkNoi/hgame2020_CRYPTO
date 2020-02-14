#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketserver
import os, sys, signal
import string, binascii
from hashlib import sha256

from secret import FLAG

from Crypto.Cipher import AES
from Crypto.Random import random, atfork

BLOCKS = lambda data: [data[16*i:16*(i+1)] for i in range(len(data)//16)]
XOR = lambda s1, s2: bytes([x^y for x,y in zip(s1, s2)])

class Task(socketserver.BaseRequestHandler):

    BLOCKSIZE = 16
    KEY = None
    IV = None

    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline: msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()

    def proof_of_work(self):
        proof = ''.join([ random.choice(string.ascii_letters+string.digits) for _ in range(20) ])
        _hexdigest = sha256(proof.encode()).hexdigest()
        self.send(str.encode( "sha256(XXXX+%s) == %s" % (proof[4:],_hexdigest) ))
        x = self.recv(prompt=b'Give me XXXX: ')
        if len(x) != 4 or sha256(x+proof[4:].encode()).hexdigest() != _hexdigest: 
            return False
        return True

    def pad(self, data):
        pad_len = self.BLOCKSIZE - (len(data) % self.BLOCKSIZE)
        return data + bytes( [pad_len] * pad_len )
    
    def unpad(self, data):
        pad_len = data[-1]
        _data = data[:-pad_len]
        if self.pad(_data) != data:
            raise ValueError('Padding is incorrect.')
        return _data

    def enc(self, block):
        aes = AES.new(self.KEY, AES.MODE_ECB)
        return aes.encrypt(block)

    def dec(self, block):
        aes = AES.new(self.KEY, AES.MODE_ECB)
        return aes.decrypt(block)

    def encrypt(self, data):
        assert len(data) > 2*self.BLOCKSIZE
        data = self.pad(data)
        iv_1, iv_2 = BLOCKS(data)[0], BLOCKS(data)[1]
        mid_1, mid_2 = iv_1, iv_2
        cipher = b''
        for block in BLOCKS(data)[2:]:
            block = XOR(block, mid_1)
            block = self.enc(block)
            mid_1 = block
            block = XOR(block, mid_2)
            block = self.enc(block)
            mid_2 = block
            cipher += block
        return iv_1 + iv_2 + cipher

    def decrypt(self, data):
        assert len(data) > 2*self.BLOCKSIZE
        assert len(data) % self.BLOCKSIZE == 0
        iv_1, iv_2 = BLOCKS(data)[0], BLOCKS(data)[1]
        mid_1, mid_2 = iv_1, iv_2
        plain = b''
        for block in BLOCKS(data)[2:]:
            mid_2_n = block
            block = self.dec(block)
            block = XOR(block, mid_2)
            mid_1_n = block
            block = self.dec(block)
            block = XOR(block, mid_1)
            mid_1, mid_2 = mid_1_n, mid_2_n
            plain += block
        return self.unpad(iv_1 + iv_2 + plain)

    def timeout_handler(self, signum, frame):
        self.send(b"\n\nSorry, time out.\n")
        raise TimeoutError

    def handle(self):
        atfork()

        self.KEY = os.urandom(32)
        self.IV = os.urandom(2*self.BLOCKSIZE)

        try:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(300)

            if not self.proof_of_work():
                return

            enc_flag = self.encrypt(self.IV + FLAG)
            self.send(b'Your encrypted FLAG (in hex) is ', newline=False)
            self.send( binascii.hexlify(enc_flag) )
    
            self.send(b'Now, I can decrypt sth for you.')
            while True:
                try:
                    self.send(b'Give me sth (in hex)')
                    hex_inp = self.recv()
                    if not hex_inp:
                        break
                    inp = binascii.unhexlify(hex_inp)
                    self.decrypt(inp)
                    self.send(b'decryption done')

                except TimeoutError:
                    exit(1)

                except:
                    self.send(b'sth must be wrong')

            signal.alarm(0)

            self.send(b'Bye~~')
            self.request.close()

        except:
            pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 1234
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
