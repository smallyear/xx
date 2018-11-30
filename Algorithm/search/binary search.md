### 

```python
def search1(L,e):
    """假设L是列表，其中元素按升序排列。
        ascending order. 如果e是L中的元素，
        则返回True，否则返回False"""
    
    def binarySearch(L,e,low,high):
        
        # 递归终止的条件
        if low == high:
            return L[low] == e
        
        mid = (low + high) // 2
        if L[mid] == e:
            return True
        elif L[mid] > e:
            if low == mid:
                return False
            else:
                return binarySearch(L,e,low,mid-1)
        else:
            return binarySearch(L,e,mid+1,high)
    if len(L) == 0:
        return False
    else:
        return binarySearch(L,e,0,len(L)-1)
```