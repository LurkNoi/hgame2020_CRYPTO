#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def KSA(S, K):
    l = len(K)
    j = 0
    for i in range(256):
        j = ( j + S[i] + K[i % l] ) % 256
        S[i], S[j] = S[j], S[i]

def PRGA(S, length):
    O = []
    i = j = 0
    for _ in range(length):
        i = (i + 1) % 256
        j = ( j + S[i] ) % 256
        S[i], S[j] = S[j], S[i]
        t = ( S[i] + S[j] ) % 256
        O.append( S[t] )
    return O


def xor(s1, s2):
    return bytes(map( (lambda x: x[0]^x[1]), zip(s1, s2) ))

def PRGAreverse(rounds_k, state_k):
    State_candidates = []
    i_k = rounds_k % 256
    for j_k in range(256):
        i, j, S, k = i_k, j_k, state_k.copy(), rounds_k
        for _ in range(k):
            S[i], S[j] = S[j], S[i]
            j = (j - S[i]) % 256
            i = (i - 1) % 256
        if j==0:
            State_candidates.append(S)
    return State_candidates


def dec(state, cipher):
    State_candidates = PRGAreverse(len(cipher), state)
    for state_i in State_candidates:
        cip = PRGA( state_i, len(cipher) )
        msg = xor(cipher, cip)
        if msg.startswith(b'hgame{'):
            print(msg)


state = [57, 27, 62, 73, 192, 95, 54, 215, 58, 99, 173, 30, 184, 140, 121, 188, 135, 130, 122, 47, 106, 41, 218, 10, 117, 88, 8, 18, 39, 25, 164, 149, 219, 227, 208, 156, 9, 119, 71, 86, 253, 65, 179, 220, 61, 203, 177, 89, 132, 217, 15, 191, 82, 32, 207, 120, 136, 67, 104, 35, 163, 137, 6, 151, 24, 155, 168, 126, 69, 77, 81, 186, 38, 83, 93, 87, 34, 233, 159, 55, 211, 66, 102, 60, 249, 4, 21, 229, 49, 97, 76, 141, 169, 185, 80, 115, 79, 52, 111, 98, 210, 105, 206, 240, 193, 92, 209, 248, 145, 246, 74, 204, 238, 196, 114, 14, 182, 85, 53, 108, 226, 128, 197, 59, 152, 243, 154, 63, 90, 139, 150, 157, 31, 17, 103, 160, 201, 230, 112, 12, 176, 100, 221, 19, 247, 181, 131, 40, 51, 101, 234, 255, 118, 68, 216, 16, 26, 228, 142, 167, 110, 252, 198, 250, 171, 166, 45, 123, 125, 33, 199, 224, 213, 158, 44, 178, 174, 223, 113, 170, 232, 172, 127, 72, 1, 56, 146, 245, 22, 64, 37, 236, 50, 13, 11, 129, 241, 29, 2, 237, 109, 46, 190, 225, 70, 162, 20, 91, 75, 222, 244, 94, 144, 200, 254, 147, 214, 43, 116, 235, 78, 3, 195, 36, 161, 28, 48, 143, 202, 7, 194, 180, 187, 134, 239, 96, 183, 165, 251, 189, 148, 138, 205, 175, 42, 5, 242, 23, 84, 133, 0, 212, 153, 107, 231, 124]
cipher = b"\x0c\xfb-\xb7{Cxb\xf0\xec\x1d'\xcd\x99\x84\xa3h)o?nlMV\xe4\xc8\xa9J\xd4\xd8"

dec(state, cipher)