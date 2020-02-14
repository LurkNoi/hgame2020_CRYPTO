from Crypto.Util.number import *
import gmpy2
from flag import flag

p = getPrime(256)
q = getPrime(256)
r = getPrime(512)
e = 2
m = bytes_to_long(flag)

n = p * q + r
c = pow(m, e, n)

with open('task', 'w') as f:
    f.write("c =  {}\n".format(str(c)))
    f.write("e =  {}\n".format(str(e)))
    f.write("q =  {}\n".format(str(q)))
    f.write("n =  {}\n".format(str(n)))

