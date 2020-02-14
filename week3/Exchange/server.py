#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketserver
import os, sys, signal
import string, binascii, random
from hashlib import sha256

from Crypto.Util import number
import gmpy2

import logging
logging.basicConfig(format='[%(levelname)s] [%(asctime)s] [%(process)d] %(message)s',level=logging.DEBUG)

FLAG = b'hgame{Wow!+U_d0_tH3_m@N-1n~ThE+miDd!3_4TtAck~}'
FLAG1 = b'hgame{Wow!+U_d0_tH3_m@N'
FLAG2 = b'-1n~ThE+miDd!3_4TtAck~}'
m_a = int.from_bytes(FLAG1, 'big')
m_b = int.from_bytes(FLAG2, 'big')

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
            if newline: msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()

    def proof_of_work(self):
        random.seed( os.urandom(8) )
        proof = ''.join([ random.choice(string.ascii_letters+string.digits) for _ in range(20) ])
        _hexdigest = sha256(proof.encode()).hexdigest()
        self.send(str.encode( "sha256(XXXX+%s) == %s" % (proof[4:],_hexdigest) ))
        x = self.recv(prompt=b'Give me XXXX: ')
        if len(x) != 4 or sha256(x+proof[4:].encode()).hexdigest() != _hexdigest: 
            return False
        return True

    def my_exit(self):
        self.send(b"Rua!!!")
        self.request.close()
        return None

    def handle(self):
        signal.alarm(60)
        if not self.proof_of_work():
            return None

        signal.alarm(0)
        random.seed( os.urandom(128) )

        p = number.getStrongPrime(1024)
        g = number.getPrime(512)

        self.send(b"Bob: Hi Alice, I got the second half of the flag.")
        self.send(b"Alice: Really? I happen to have the first half of the flag.")
        self.send(b"Bob: So let's exchange flags, :-)")
        self.send(b"Alice: Ok, ")
        self.send(b"Alice: Ah, wait, maybe this channel is not secure, ")
        self.send(b"Alice: Let's do Key Exchange first.\n")

        self.recv(prompt=b'')

        self.send(b"[INFO] : ********** STEP.1 **********")
        self.send(b"[INFO] : Alice and Bob publicly agree to use a modulus `p` and base `g`\n")
        # Don't consider `g is a primitive root modulo p` for the time being
        self.send(str.encode( 'Alice: p = %d' % p) )
        self.send(str.encode( 'Alice: g = %d\n' % g) )
        
        self.recv(prompt=b'')

        self.send(b"[INFO] : ********** STEP.2 **********")
        self.send(b"[INFO] : Alice generates her private key `a` which is a random number from the set {2, 3, ... p-2}.")
        a = random.randint(2, p-2)
        self.send(b"[INFO] : Bob does exactly the same: he compute his private key `b` which is taken randomly from the same set of integers.")
        b = random.randint(2, p-2)
        self.send(b"[INFO] : Now, Alice computes her public key `A` which is simply `g` raises to the `a`s power modulo `p`, a.k.a, `A = pow(g, a, p)`.")
        A = pow(g, a, p)
        self.send(b"[INFO] : Bob does the same: Bob computes the `B = pow(g, b, p)`.\n")
        B = pow(g, b, p)

        self.recv(prompt=b'')

        self.send(b"[INFO] : ********** STEP.3 **********")
        self.send(b"[INFO] : Alice and Bob exchange their public key.")
        self.send(b"[WARNING] : You intercepted Alice's message, which is ")
        self.send(str.encode( "[WARNING] : A = %d" % A ))
        self.send(b"[WARNING] : Do you want to modify this message? (yes/no)")
        signal.alarm(10)
        y_or_n = self.recv()
        logging.info('Change A? '+ str(y_or_n))
        if y_or_n == b'yes':
            self.send(b"[WARNING] : Select a decimal number")
            try:
                signal.alarm(20)
                inp = self.recv()
                # logging.info('Change A to? ' + str(inp))
                AA = int( inp )
                if AA<2 or AA>=p or AA==g:
                    logging.warning('Invalid AA')
                    self.send(b"Invalid A")
                    self.my_exit()
            except:
                logging.warning('Incorrect AA format')
                self.send(b"Invalid format")
                self.my_exit()
        elif y_or_n == b'no':
            AA = A
        else:
            self.send(b"choose yes or no")
            logging.warning('Invalid y_or_n')
            self.my_exit()
        signal.alarm(0)

        self.send(b"")
        self.send(str.encode( "Alice: A = %d\n" % AA ))

        self.recv(prompt=b'')

        self.send(b"[WARNING] : Again, you intercepted Bob's message, which is")
        self.send(str.encode( "[WARNING] : B = %d" % B ))
        self.send(b"[WARNING] : Do you want to modify this message? (yes/no)")
        signal.alarm(10)
        y_or_n = self.recv()
        logging.info('Change B? '+ str(y_or_n))
        if y_or_n == b'yes':
            self.send(b"[WARNING] : Select a decimal number")
            try:
                signal.alarm(20)
                inp = self.recv()
                # logging.info('Change B to? ' + str(inp))
                BB = int( inp )
                if BB<2 or BB>=p or BB==g:
                    logging.warning('Invalid BB')
                    self.send(b"Invalid B")
                    self.my_exit()
            except:
                logging.warning('Incorrect BB format')
                self.send(b"Invalid format")
                self.my_exit()
        elif y_or_n == b'no':
            BB = B
        else:
            self.send(b"choose yes or no")
            logging.warning('Invalid y_or_n')
            self.my_exit()
        signal.alarm(0)

        self.send(b"")
        self.send(str.encode( "Bob: B = %d\n" % BB ))

        self.recv(prompt=b'')

        self.send(b"[INFO] : ********** STEP.4 **********")
        self.send(b"[INFO] : Alice takes public key of Bob (`B`), raises to, again, to the `a`s power modulo `p`, the she gets the secret value `S_a = pow(B, a, p)`.")
        S_a = pow(BB, a, p)
        self.send(b"[INFO] : Bob also gets the secret value `S_b = pow(A, b, p)`.")
        S_b = pow(AA, b, p)
        self.send(b"[INFO] : Right now, they have done the key exchange.")
        self.send(b"[WARNING] : hint: does Alice and Bob share the same key?\n")

        self.recv(prompt=b'')

        self.send(b"Alice: Now, we have securely shared the secret value.")
        self.send(b"Bob: Right, let's exchange the encrypted flag!\n")

        self.recv(prompt=b'')

        self.send(b"[INFO] : For the encryption, Alice compute `C_a = (m * S_a) % p`")
        C_a = (m_a * S_a) % p
        self.send(b"[INFO] : Bob does the same, `C_b = (m * S_b) % p`\n")
        C_b = (m_b * S_b) % p

        self.recv(prompt=b'')

        self.send(b"[WARNING] : Bob is trying to send a message to Alice, ")
        self.send(str.encode( "[WARNING] : C_b = %d" % C_b ))
        self.send(b"[WARNING] : Do you want to modify this message? (yes/no)")
        signal.alarm(10)
        y_or_n = self.recv()
        logging.info('Change C_b? '+ str(y_or_n))
        if y_or_n == b'yes':
            self.send(b"[WARNING] : Select a decimal number")
            try:
                signal.alarm(20)
                inp = self.recv()
                # logging.info('Change C_b to? ' + str(inp))
                C_bb = int( inp )
                if C_bb<=0 or C_bb>=p:
                    logging.warning('Invalid BB')
                    self.send(b"Invalid C_b")
                    self.my_exit()
            except:
                logging.warning('Incorrect C_bb format')
                self.send(b"Invalid format")
                self.my_exit()
        elif y_or_n == b'no':
            C_bb = C_b
        else:
            self.send(b"choose yes or no")
            logging.warning('Invalid y_or_n')
            self.my_exit()
        signal.alarm(0)

        m_bb = (C_bb * gmpy2.invert(S_a, p)) % p
        if m_bb != m_b:
            logging.warning('failed when forge m_bb')
            self.send(b"\nAlice: Are you messing with me? I submitted the flag, but the prompt says the flag is wrong!\n")
            self.send(b"[INFO] : Alice is offline")
            self.my_exit()
        else:
            logging.warning('should get the flag')
            self.send(b"Alice: Great, I get the flag.")
            self.send(str.encode( 'Alice: C_a = %d' % C_a ))

        self.recv(prompt=b'')

        m_aa = (C_a * gmpy2.invert(S_b, p)) % p
        if m_aa != m_a:
            self.send(b"\n[INFO] : Alice is offline\n")
            self.send(b"Bob: Damn it! She lied on me...")
        else:
            self.send(b"Happy cooperation. :)")

        self.request.close()


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 12345
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
