### [题目信息]：

出题人: Lurkrul

考点: Man-in-the-middle attack

题目描述:

```
Our admin hijacked a secret channel and it looks like there are two teams doing some unspeakable transactions.
```

### [题目writeup]：

简单的 [MITM attack](https://en.wikipedia.org/wiki/Man-in-the-middle_attack), Alice 和 Bob 各有部分 flag.

Alice, Bob 采用 [Diffie–Hellman key exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange), 大概扯一下

1. Alice,Bob 确定公共的参数 p, g
2. 分别计算各自的公钥私钥, (A, a), (B, b)
3. 交换公钥, 计算出共同的 `s = pow(A, b, p) = pow(B, a, p) = pow(g, ab, p)`, 从而在不泄露 `s` 的情况下共享这一参数

现存在中间人攻击, C 可以先生成自己的公私钥 (C, c), 然后替换 A, B

那么 Alice 计算出的 `S_a = pow(fake_B, a, p) = pow(C, a, p) = pow(g, ac, p)`

Bob 得到 `S_b = pow(g, bc, p)`, 可以看作 C 站在 A,B 中间进行传话

加密过程简单的求个逆就好了, 最后注意需要伪造正确的密文来通过 Alice 的验证, ~~(也没增加多少难度)~~


