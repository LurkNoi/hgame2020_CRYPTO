#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, random
import string, binascii
import signal
import socketserver
from hashlib import sha256
from Crypto.Cipher import AES

from secret import MESSAGE
assert len(MESSAGE) == 48


class Task(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kargs):
        self.KEY = b""
        self.IV = b""
        super().__init__(*args, **kargs)

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

    def encrypt(self, data):
        assert len(data) % 16 == 0
        aes = AES.new(self.KEY, AES.MODE_CFB, self.IV, segment_size=128)
        return aes.encrypt(data)

    def decrypt(self, data):
        assert len(data) % 16 == 0
        aes = AES.new(self.KEY, AES.MODE_CFB, self.IV, segment_size=128)
        return aes.decrypt(data)

    def handle(self):
        signal.alarm(60)
        self.KEY = os.urandom(32)
        self.IV = os.urandom(16)

        self.send(b"You have only 3 times to decrypt sth, then I'll give u the FLAG.")
        try:
            for _ in range(3):
                self.send(b"Give me sth(hex) to decrypt")
                hex_input = self.recv()
                if not hex_input:
                    break
                ciphertext = binascii.unhexlify(hex_input)
                plaintext = self.decrypt(ciphertext)
                self.send( binascii.hexlify(plaintext) )
        except:
            self.send(b"Rua!!!")
            self.request.close()

        enc_msg = self.encrypt(MESSAGE)
        self.send(b"Here is your encrypted FLAG(hex): ", newline=False)
        self.send( binascii.hexlify(enc_msg) )
        self.request.close()


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 1234
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()