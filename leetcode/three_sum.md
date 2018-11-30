### 三数之和
**难度: Easy**

```
给定一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？找出所有满足条件且不重复的三元组。

注意：答案中不可以包含重复的三元组。
```
示例
```
例如, 给定数组 nums = [-1, 0, 1, 2, -1, -4]，

满足要求的三元组集合为：
[
  [-1, 0, 1],
  [-1, -1, 2]
]
```
答案
排序和去重之后还是超时
```python
class Solution:
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        length,res = len(nums),[]
        if length < 3:
            return res
        nums.sort()
        for i in range(length):
            for j in range(i+1,length):
                rest_num = 0 - nums[i] - nums[j]
                if rest_num in nums[j+1:]:
                    r = [nums[i],nums[j],rest_num]
                    if r not in res:
                        res.append(r)
        return res
```
在github上参考别人的思路

- 排序
- 固定左边，如果左边重复，继续
- 左右边界同时处理，去重，针对不同的左右边界情况处理

```python
class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        length, res = len(nums), []
        nums.sort()
        for i in range(length):
            if i > 0 and nums[i] == nums[i-1]: 
                continue
            l, r = i+1, length-1
            while l < r:
                tmp = nums[i] + nums[l] + nums[r]
                if tmp == 0:
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[l] == nums[l-1]: 
                        l += 1
                    while l < r and nums[r] == nums[r+1]: 
                        r -= 1
                elif tmp > 0:
                    r -= 1
                else:
                    l += 1
        return res
```