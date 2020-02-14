### [题目信息]：

出题人: Lurkrul

考点: Sbox, Extended Euclidean algorithm

题目描述:

```
Does python "bytes" object have inverse?
```

### [题目writeup]：

注意到 `Mul( Mul(A, B), C) == Mul( A, Mul(B, C) )`, 存在单位元 `E = bytes(range(256))`, 存在逆元,

故可以将 256 字节长的不重复字串 和 运算 `Mul` 视为一个群 [Group](https://en.wikipedia.org/wiki/Group_(mathematics)), 逆元很好求, `S.find`

记 `Pow(s, k)` 为 `s_k`, 已知 `s595, s739`, 要求 `s_(-1)` 即 `Inv(s)`

根据扩展欧几里得算法得到 `-1 = 595*272 + (-739)*219`

因此, `s_inv = Mul( Pow(s595, 272), Pow(Inv(s739), 219) )`