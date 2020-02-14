#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import string
import base64
import socketserver

# from secret import flag
flag = b'hgame{r3us1nG+M3$5age-&&~rEduC3d_k3Y-5P4Ce}'
assert flag.startswith(b'hgame{') and flag.endswith(b'}')

flag_len = len(flag)

def xor(s1, s2):
    return bytes([x^y for x,y in zip(s1,s2)])

class Task(socketserver.BaseRequestHandler):

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

    def enc(self):
        random.seed(os.urandom(8))
        keystream = ''.join([
            random.choice(
                string.ascii_letters + string.digits
                ) 
            for _ in range(flag_len) 
            ])
        keystream = keystream.encode()
        return base64.b64encode(xor(flag, keystream))

    def handle(self):
        cipher = self.enc()
        self.send(cipher)
        self.request.close()


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 25001
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
