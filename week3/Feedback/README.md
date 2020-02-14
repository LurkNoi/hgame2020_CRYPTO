### [题目信息]：

出题人: Lurkrul

考点: CFB mode

题目描述:

```
听说上周Classic_CrackMe的CBC很简单? 来耍个CFB试试 XD
```

### [题目writeup]：

解密三次后给出加密的 FLAG, 由于 IV, KEY 每次随机生成, 上一次的密文不能用, 但是明文是固定的.

```
记 msg = m1 || m2 || m3 , 则有
encrypt:
    plain  :    IV    m1            m2            m3
    cipher :    IV    c1            c2            c3
                      = E(IV)^m1    = E(c1)^m2    = E(c2)^m3
```

为了获取 `m1` 只需要提前知道 `E(IV)`, 则有 `m1 = c1 ^ E(IV)`

为了获取 `m2` 需要知道 `E(c1)`, 由于每次 KEY 在变, 无法提前知道 `c1`, 但是在已知 `m1` 的条件下, 可以提前算出 `c1`

`m3` 同理

```
decrypt:
    cipher :    IV    C1          C2
    plain  :    IV    E(IV)^C1    E(C1)^C2
```

观察解密的过程不难发现 `decrypt( x || ZeroBlock ) = E(IV)^x || E(X)`, 可以获得任意一 BLOCK 的 AES 密文

