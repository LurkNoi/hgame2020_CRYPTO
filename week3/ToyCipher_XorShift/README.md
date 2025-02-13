### [题目信息]：

出题人: Lurkrul

考点: 逆算法

题目描述:

```
出题人加密了FLAG, 但懒得写解密函数, 你能帮帮它吗 :-)
```

### [题目writeup]：

IV 白给, 可以自己实现 `decrypt()` (*task.py* 里故意不给出), 主要难点在于逆 `y = f(x, a)`

当 `shr=True` 时, 即 *x* 与自己右移 *a bits* 后相异或, 

把每 *a bits* 当作一组(不足 *a bits* 也算一组, 不影响结果), 那么有 

```
y[0] = x[0]
y[1] = x[0] ^ x[1]
y[2] = x[1] ^ x[2]
...
```

逆回去就是

```
x[0] = y[0]
x[1] = x[0] ^ y[1] = y[0] ^ y[1]
x[2] = x[1] ^ y[2] = y[0] ^ y[1] ^ y[2]
...
```

```python
def f_inv(x, a, shr):
    x = x & MASK
    a = a % BITSLENGTH
    y = 0
    while x:
        y ^=x
        if shr:
            x >>= a
        else:
            x <<= a
        x &= MASK
    return y & MASK
```

实际上相当于在 `GF(2)` 上的矩阵运算

```
将 a 转换成 bits 每 4 个一行写成矩阵

[1 0 1 0]
[1 1 0 0]
...
[0 1 X X] (不足一行可以补 X, 反正不影响)

那么 a ^= a >> 4 相当于左乘这么一个矩阵

[1 0 0 0]
[1 1 0 0]
[0 1 1 0]
[0 0 1 1]
```

CBC 应该都不是问题