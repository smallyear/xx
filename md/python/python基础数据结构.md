#### Python中基本数据结构的操作

|      | 元组                   | 列表                   | 字典                                       | 集合                              |
| ---- | -------------------- | -------------------- | ---------------------------------------- | ------------------------------- |
| 定义   | letter=("a","b","c") | letters = ['a', 'b'] | letterdict = {1:'a', 2:'b'} /dict_from_tuple = dict(((1,'a'), (2,'b'))) | letters=set()/letters={"a","b"} |
| 新增   | 无                    | append/insert        | letterdict[3]="d"                        | letters.add("d")/letters.update("a","b") |
| 删除   | 无                    | letters.remove("a")/del letters[-1]  | del  letterdict[1]                       | letters.remove("c")/letters.discard() |
|其他操作|| letters.count('a')|letterdict.values()|letters.union()|
|||letters.reverse()|letterdict.keys()|letters.union()|
|||letters.extand()||letters.intersection()|
|||letters.sorts()||letters.difference()|
|||letters.pop(1)||letters.symmetric_difference()|
