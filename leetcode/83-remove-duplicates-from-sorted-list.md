###  删除排序链表中的重复元素
**难度: Easy**

给定一个排序链表，删除所有重复的元素，使得每个元素只出现一次。

示例 1:
```
输入: 1->1->2
输出: 1->2
示例 2:

输入: 1->1->2->3->3
输出: 1->2->3
```

答案
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        p = head
        if p is None:
            return p
        q = head.next
        while(q):
            if p.val == q.val:
                p.next = q.next
                q.next = None
                q = p.next
            else:
                p = p.next
                q = q.next
        return head
        
        
```

