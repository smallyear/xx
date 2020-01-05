###  对称二叉树
**难度: Easy**

给定一个二叉树，检查它是否是镜像对称的。

例如，二叉树 [1,2,2,3,4,4,3] 是对称的。
```

    1
   / \
  2   2
 / \ / \
3  4 4  3
```
```
但是下面这个 [1,2,2,null,3,null,3] 则不是镜像对称的:

    1
   / \
  2   2
   \   \
   3    3
```

答案
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        if root is None:
            return True
        return self.s(root.right, root.left)
        
    def s(self, right, left):
        if not right and not left:
            return True
        if right and left and right.val == left.val:
            return self.s(right.left, left.right) and self.s(right.right, left.left)
        else:
            return False

        
```

