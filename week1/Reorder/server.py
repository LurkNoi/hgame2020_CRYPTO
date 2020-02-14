#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import string
import socketserver


flag = b'hgame{jU$t+5ImpL3_PeRmuTATi0n!!}'


class Task(socketserver.BaseRequestHandler):

    BLOCKSIZE = 16
    PAD_CHAR = b' '

    def __init__(self, *args, **kargs):
        self.PBOX = list(range(self.BLOCKSIZE))
        random.seed(os.urandom(8))
        random.shuffle(self.PBOX)
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
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()

    def blocks(self, data):
        size = self.BLOCKSIZE
        return [data[i*size : (i+1)*size] 
                for i in range(len(data)//size)]

    def pad(self, data):
        size = self.BLOCKSIZE
        pad_len = size - (len(data) % size)
        return data + self.PAD_CHAR*pad_len

    def _enc(self, block):
        return bytes([ block[p] for p in self.PBOX ])

    def enc(self, data):
        data = self.pad(data)
        cipher = b''
        for block in self.blocks(data):
            cipher += self._enc(block)
        return cipher

    def handle(self):
        for _ in range(10):
            try:
                inp = self.recv()
                if not inp:
                    break
                cip = self.enc(inp)
                self.send(cip)
            except:
                self.send(b'Rua!!!')
                self.request.close()

        self.send(b'Rua!!!')
        enc_flag = self.enc(flag)
        self.send(enc_flag)
        self.request.close()


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 25002
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
