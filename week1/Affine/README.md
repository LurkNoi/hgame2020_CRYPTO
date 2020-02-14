### [题目信息]：

出题人: Lurkrul

考点: 简单模运算

题目描述:

```
Some basic modular arithmetic...
```

### [题目writeup]：

已知部分明文, 则有

$$
A * INDEX('h') + B \equiv INDEX('A') \pmod MOD \
A * INDEX('g') + B \equiv INDEX('8') \pmod MOD
$$

两式相减, 得

$$
A * (INDEX('h') - INDEX('g')) \equiv (INDEX('A') - INDEX('8')) \pmod MOD
$$

两边乘以 `(INDEX('h') - INDEX('g'))` 关于 `MOD` 的逆元, 即可解出 `A`, 进而获得 `B`