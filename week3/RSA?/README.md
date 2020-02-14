### [题目信息]：

出题人: Alias

考点: 二次剩余

题目描述:

```
It's just a little difficult RSA?
```

### [题目writeup]：

心细一点可以发现这题就不是一个RSA，因为n是一个素数

代码并不复杂很容易得到：$m^2 \equiv c \pmod n$，其实就是求解二次剩余，用Tonelli–Shanks算法可解



