### [题目信息]：

出题人: Lurkrul

考点: RC4 PRGA reverse

题目描述:

```
Oo0o0 It's a reverse game!! 0Oo0o
```

### [题目writeup]：

看题目名字可以猜出是 [RC4](https://en.wikipedia.org/wiki/RC4), 已知密文和此时的 State (`S`).

为求得 keystream (`RC4.PRGA(length)`), 并不需要获得 key (`os.urandom(8)`), 即在此我们并不关心 KSA, 只需要让 State 倒回去, 回到 KSA 之后的状态.

```
i := 0
j := 0
while GeneratingOutput:
    i := (i + 1) mod 256
    j := (j + S[i]) mod 256
    swap values of S[i] and S[j]
    K := S[(S[i] + S[j]) mod 256]
    output K
endwhile
```

循环次数 (记为 `rounds_k`) 等于 cipher 的长度, 那么 k 次循环后 `i_k = rounds_k % 256`, 此时的 `j_k` 不知道, 只知道 `j` 的初始值为 0, 因此可以枚举 `j_k` 获得候选的 State.

> 注: 事实上 PRGA 最后一轮的输出已知 (`ord('}') ^ cipher[-1]`), 可以据此确定 `j_k`