### 无重复字符的最长子串
**难度: Medium**

```
给定一个字符串，找出不含有重复字符的最长子串的长度。
```
示例
```
输入: "abcabcbb"
输出: 3 
解释: 无重复字符的最长子串是 "abc"，其长度为 3。
```
```
输入: "bbbbb"
输出: 1
解释: 无重复字符的最长子串是 "b"，其长度为 1。
```
```
输入: "pwwkew"
输出: 3
解释: 无重复字符的最长子串是 "wke"，其长度为 3。
     请注意，答案必须是一个子串，"pwke" 是一个子序列 而不是子串。
```
答案
```python
class Solution:
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        max_len = 0
        if s is None or len(s) == 0:
            return max_len
        str_dic = {}
        start = 0
        one_max = 0
        for i in range(len(s)):
            if s[i] in str_dic and str_dic[s[i]] >= start:
                start = str_dic[s[i]] + 1
            one_max = i - start + 1
            str_dic[s[i]] = i
            max_len = max(one_max,max_len)
        return max_len
if __name__ == '__main__':
    sol = Solution()
    print(sol.lengthOfLongestSubstring("bbbbb"))
    print(sol.lengthOfLongestSubstring("pwwkeow"))
    print(sol.lengthOfLongestSubstring("abcabcbb"))
            
```