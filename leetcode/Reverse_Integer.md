### 反转整数
**难度: Easy**

```
给定一个 32 位有符号整数，将整数中的数字进行反转。

```
示例
```
输入: 123
输出: 321
```
```
输入: -123
输出: -321
```
```
输入: 120
输出: 21
```
答案
```python
class Solution:
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        x = -int(str(x)[::-1][:-1]) if x < 0 else int(str(x)[::-1])
        x = 0 if abs(x) > 0x7FFFFFFF else x
        return x
```