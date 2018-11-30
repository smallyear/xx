```python
import numpy as np
# 一维数据不用赘言

data_1d = np.array([0, 1, 2, 3])

# 二维数据作为 m 行 n 列的表格，例如 2 行 3 列

data_2d = np.arange(6).reshape(2, 3)

# 三维数据作为 k 层 m 行 n 列 的积木块， 例如 2 层 3 行 4 列

data_3d = np.arange(24).reshape(2, 3, 4)
```
