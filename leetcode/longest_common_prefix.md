### 搜索插入位置
**难度: Easy**

```
编写一个函数来查找字符串数组中的最长公共前缀。

如果不存在公共前缀，返回空字符串 ""。

```
示例
```
输入: ["flower","flow","flight"]
输出: "fl"
```
```
输入: ["dog","racecar","car"]
输出: ""
解释: 输入不存在公共前缀。

```
答案
```python
class Solution:
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ""
        for i in range(len(strs[0])):
            for str in strs:
                if len(str) <= i or strs[0][i] != str[i]:
                    return strs[0][:i]
        return strs[0]
```
```python
class Solution:
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        return os.path.commonprefix(strs)

```
