### 两数相加
**难度: Medium**

```
给定两个非空链表来表示两个非负整数。位数按照逆序方式存储，它们的每个节点只存储单个数字。将两数相加返回一个新的链表。

你可以假设除了数字 0 之外，这两个数字都不会以零开头。
```
示例
```
输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
输出：7 -> 0 -> 8
原因：342 + 465 = 807
```
答案
```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        if l1 == None:
            return l2
        if l2 == None:
            return l1
        res = l1.val + l2.val
        
        if res < 10:
            res_listNode = ListNode(res)
            res_listNode.next = self.addTwoNumbers(l1.next,l2.next)
        else:
            res_listNode = ListNode(res - 10)
            tmp = ListNode(1)
            tmp.next = None
            res_listNode.next = self.addTwoNumbers(l1.next,self.addTwoNumbers(l2.next,tmp))
        return res_listNode
            
```