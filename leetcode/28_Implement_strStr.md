### 实现strStr()
**难度: Easy**

```
实现 strStr() 函数。

给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回  -1。

```
示例
```
输入: haystack = "hello", needle = "ll"
输出: 2
```
```
输入: haystack = "aaaaa", needle = "bba"
输出: -1
```
答案
```python
class Solution:
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        index  = 0
        if needle != '':
            if needle in haystack:
                index = haystack.index(needle)
            else:
                index = -1
        return index
```
一行解法
```python
class Solution(object):
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        return haystack.find(needle)
```