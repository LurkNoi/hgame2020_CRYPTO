### [题目信息]：

出题人: Lurkrul

考点: Rotational cryptanalysis

题目描述:

```
Why encryption based on XOR and Rotation is easy to break?
```

### [题目writeup]：

rotation 并未改变 xor 的 bit 位置, 且 roundkeys 也由移位来生成

```
ToyCipher(0,key)^ToyCipher(plain,0) == ToyCipher(plain,key)
ToyCipher(ToyCipher(0,key)^cipher,0,'dec') == ToyCipher(cipher,key,'dec')
```

由于 rotation, xor 均可当作线性操作(这里主要就分配律,结合律), 密文可以分解为 `(plain各种移位相异或) 异或上 (key各种移位相异或)`, 根据异或的特性, `plain` 或 `key` 为 0 时可以得到另一部分. 

~~当作一线性时不变系统, 零输入响应 ToyCipher(0,key), 零状态响应 ToyCipher(plain,0)~~

更一般的, 有

```
 ToyCipher(a, k1, 'enc/dec') ^ ToyCipher(b, k2, 'enc/dec') == ToyCipher(a^b, k1^k2, 'enc/dec')
```

这东西也不好描述, 可以想象两个加密过程, 它们对应的比特位相异或, 恰组成了一个新的加密.

