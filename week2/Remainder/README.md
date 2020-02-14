### [题目信息]：

出题人: Lurkrul

考点: Chinese remainder theorem

题目描述:

```
烤个孙子
```

### [题目writeup]：

白给, 就是个孙子定理, 证明的话我还没 [wiki](https://en.wikipedia.org/wiki/Chinese_remainder_theorem) 上讲的好, 就不提了 ~~(就是懒得讲)~~

由于 `p,q,r` 已知, 可以直接一个 CRT 过去拿到 `pow(m, e, pqr)`, 然后解个 RSA

也可以分别解出 `m_p, m_q, m_r` (毕竟模是素数直接就能解), 然后再一个 CRT 上去还原出 `m`
