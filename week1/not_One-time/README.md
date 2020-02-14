### [题目信息]：

出题人: Lurkrul

考点: OTP, reduced key space

题目描述:

```
Just XOR ;P
```

### [题目writeup]：

注意到本题与 OTP 不同的是更小密钥空间 (`string.ascii_letters+string.digits`)

因此可以多次连接, 获取多个密文, 然后将所有可能的明文取交集 (exp经测试, 大概需要50-100组)