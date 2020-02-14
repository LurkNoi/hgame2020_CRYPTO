### [题目信息]：

出题人: Lurkrul

考点: rsa

题目描述:

```
真*签到题
p = 681782737450022065655472455411; q = 675274897132088253519831953441; e = 13; c = pow(m,e,p*q) = 275698465082361070145173688411496311542172902608559859019841
```

### [题目writeup]：

典型的 [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)), p,q白给

```python
import gmpy2
from Crypto.Util import number

d = gmpy2.invert(e, (p-1)*(q-1))
m = pow(c, d, p*q)
print( number.long_to_bytes(m) )
```