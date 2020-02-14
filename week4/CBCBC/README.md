### [题目信息]：

出题人: Lurkrul

考点: Padding Oracle Attack

题目描述:

```
CBC太简单了, 来试试我瞎编的CBCBC :P
```

### [题目writeup]：

感觉没啥好说的, 看得懂 CBC 的 [POA](https://en.wikipedia.org/wiki/Padding_oracle_attack) 的话, 对比一下本题加密的流程, 不难发现需要翻转的 block 由倒数第二个变为倒数第三个, 主要是为了防止有些选手不加理解的拿了脚本就上来打


