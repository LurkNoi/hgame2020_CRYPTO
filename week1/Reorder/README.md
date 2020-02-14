### [题目信息]：

出题人: Lurkrul

考点: Permutation

题目描述:

```
We found a secret oracle and it looks like it will encrypt your input...
```

### [题目writeup]：

就是个 Permutation, 多次尝试后发现每 16 个一组进行重排, 看源码还是很容易理解的.

比如输个 `0123456789abcdef` 和 `0123456789abcdef0123456789abcdef` 基本就能做出来了.