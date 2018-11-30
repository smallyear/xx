#### 获取数据
1.从表格导入

		df=pd.DataFrame(pd.read_csv('name.csv',header=1))
		df=pd.DataFrame(pd.read_excel('name.xlsx'))
2.创建数据表
		
```
df = pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006], 

                   "date":pd.date_range('20130102', periods=6),

                   "city":['Beijing ', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],

                   "age":[23,44,54,32,34,32],

                   "category":['100-A','100-B','110-A','110-C','210-A','130-F'],

                   "price":[1200,np.nan,2133,5433,np.nan,4432]},

                   columns =['id','date','city','category','age','price'])
```
```
     id       date         city category  age   price
0  1001 2013-01-02     Beijing     100-A   23  1200.0
1  1002 2013-01-03           SH    100-B   44     NaN
2  1003 2013-01-04   guangzhou     110-A   54  2133.0
3  1004 2013-01-05     Shenzhen    110-C   32  5433.0
4  1005 2013-01-06     shanghai    210-A   34     NaN
5  1006 2013-01-07     BEIJING     130-F   32  4432.0
```

#### 数据检查
获取数据维度

```
>>> df.shape
(6, 6)
```

get dataframe info
```
>>> df.info()
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 6 entries, 0 to 5
Data columns (total 6 columns):
id          6 non-null int64
date        6 non-null datetime64[ns]
city        6 non-null object
category    6 non-null object
age         6 non-null int64
price       4 non-null float64
dtypes: datetime64[ns](1), float64(1), int64(2), object(2)
memory usage: 280.0+ bytes
```
get data type
```
>>> df.dtypes
id                   int64
date        datetime64[ns]
city                object
category            object
age                  int64
price              float64
dtype: object
>>> df['age'].dtypes
dtype('int64')
```

check whether data is null
```
>>> df.isnull()
      id   date   city  category    age  price
0  False  False  False     False  False  False
1  False  False  False     False  False   True
2  False  False  False     False  False  False
3  False  False  False     False  False  False
4  False  False  False     False  False   True
5  False  False  False     False  False  False
>>> df['price'].isnull()
0    False
1     True
2    False
3    False
4     True
5    False
Name: price, dtype: bool
```
check unique
```
>>> df['age'].unique()
array([23, 44, 54, 32, 34], dtype=int64)
```
```
>>> df.values
array([[1001, Timestamp('2013-01-02 00:00:00'), 'Beijing ', '100-A', 23,
        1200.0],
       [1002, Timestamp('2013-01-03 00:00:00'), 'SH', '100-B', 44, nan],
       [1003, Timestamp('2013-01-04 00:00:00'), ' guangzhou ', '110-A',
        54, 2133.0],
       [1004, Timestamp('2013-01-05 00:00:00'), 'Shenzhen', '110-C', 32,
        5433.0],
       [1005, Timestamp('2013-01-06 00:00:00'), 'shanghai', '210-A', 34,
        nan],
       [1006, Timestamp('2013-01-07 00:00:00'), 'BEIJING ', '130-F', 32,
        4432.0]], dtype=object)
>>> df['age'].values
array([23, 44, 54, 32, 34, 32], dtype=int64)
>>> df.columns
Index(['id', 'date', 'city', 'category', 'age', 'price'], dtype='object')
```
```
>>> df.head()
     id       date         city category  age   price
0  1001 2013-01-02     Beijing     100-A   23  1200.0
1  1002 2013-01-03           SH    100-B   44     NaN
2  1003 2013-01-04   guangzhou     110-A   54  2133.0
3  1004 2013-01-05     Shenzhen    110-C   32  5433.0
4  1005 2013-01-06     shanghai    210-A   34     NaN
>>> df.head(3)
     id       date         city category  age   price
0  1001 2013-01-02     Beijing     100-A   23  1200.0
1  1002 2013-01-03           SH    100-B   44     NaN
2  1003 2013-01-04   guangzhou     110-A   54  2133.0
>>> df.tail()
     id       date         city category  age   price
1  1002 2013-01-03           SH    100-B   44     NaN
2  1003 2013-01-04   guangzhou     110-A   54  2133.0
3  1004 2013-01-05     Shenzhen    110-C   32  5433.0
4  1005 2013-01-06     shanghai    210-A   34     NaN
5  1006 2013-01-07     BEIJING     130-F   32  4432.0
>>> df.tail(2)
     id       date      city category  age   price
4  1005 2013-01-06  shanghai    210-A   34     NaN
5  1006 2013-01-07  BEIJING     130-F   32  4432.0
```
#### 数据清洗
delete columns what is nan
```
>>> df.dropna(how='any')
     id       date         city category  age   price
0  1001 2013-01-02     Beijing     100-A   23  1200.0
2  1003 2013-01-04   guangzhou     110-A   54  2133.0
3  1004 2013-01-05     Shenzhen    110-C   32  5433.0
5  1006 2013-01-07     BEIJING     130-F   32  4432.0
```
update df set na=0
```
>>> df.fillna(value=0)
     id       date         city category  age   price
0  1001 2013-01-02     Beijing     100-A   23  1200.0
1  1002 2013-01-03           SH    100-B   44     0.0
2  1003 2013-01-04   guangzhou     110-A   54  2133.0
3  1004 2013-01-05     Shenzhen    110-C   32  5433.0
4  1005 2013-01-06     shanghai    210-A   34     0.0
5  1006 2013-01-07     BEIJING     130-F   32  4432.0
```
update columns set it\`s mean
```
>>> df['price'].fillna(df['price'].mean())
0    1200.0
1    3299.5
2    2133.0
3    5433.0
4    3299.5
5    4432.0
Name: price, dtype: float64
```

```
>>> df['city']=df['city'].map(str.strip)
>>> df
     id       date       city category  age   price
0  1001 2013-01-02    Beijing    100-A   23  1200.0
1  1002 2013-01-03         SH    100-B   44     NaN
2  1003 2013-01-04  guangzhou    110-A   54  2133.0
3  1004 2013-01-05   Shenzhen    110-C   32  5433.0
4  1005 2013-01-06   shanghai    210-A   34     NaN
5  1006 2013-01-07    BEIJING    130-F   32  4432.0

>>> df['city']=df['city'].str.lower()
>>> df
     id       date       city category  age   price
0  1001 2013-01-02    beijing    100-A   23  1200.0
1  1002 2013-01-03         sh    100-B   44  3299.5
2  1003 2013-01-04  guangzhou    110-A   54  2133.0
3  1004 2013-01-05   shenzhen    110-C   32  5433.0
4  1005 2013-01-06   shanghai    210-A   34  3299.5
5  1006 2013-01-07    beijing    130-F   32  4432.0
```
```
>>> df['price'].astype('int')
0    1200
1    3299
2    2133
3    5433
4    3299
5    4432
Name: price, dtype: int32
```

```
>>> df.rename(columns={'category':'category-size'})
     id       date       city category-size  age   price
0  1001 2013-01-02    beijing         100-A   23  1200.0
1  1002 2013-01-03         sh         100-B   44  3299.5
2  1003 2013-01-04  guangzhou         110-A   54  2133.0
3  1004 2013-01-05   shenzhen         110-C   32  5433.0
4  1005 2013-01-06   shanghai         210-A   34  3299.5
5  1006 2013-01-07    beijing         130-F   32  4432.0

```
delete duplicate value
```
>>> df['city'].drop_duplicates()
0      beijing
1           sh
2    guangzhou
3     shenzhen
4     shanghai
Name: city, dtype: object
>>> df['city'].drop_duplicates(keep='last')
1           sh
2    guangzhou
3     shenzhen
4     shanghai
5      beijing
Name: city, dtype: object
```
data replace
```
>>> df['city'].replace('sh','shanghai')
0      beijing
1     shanghai
2    guangzhou
3     shenzhen
4     shanghai
5      beijing
Name: city, dtype: object
```
#### data preprocessing
```
#创建df1数据表

df1=pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006,1007,1008], 

"gender":['male','female','male','female','male','female','male','female'],

"pay":['Y','N','Y','Y','N','Y','N','Y',],

"m-point":[10,12,20,40,40,40,30,20]})
```
df merge
```
>>> df1
     id  gender pay  m-point
0  1001    male   Y       10
1  1002  female   N       12
2  1003    male   Y       20
3  1004  female   Y       40
4  1005    male   N       40
5  1006  female   Y       40
6  1007    male   N       30
7  1008  female   Y       20
>>> df_inner=pd.merge(df,df1,how='inner')
>>> df_inner
     id       date       city category  age   price  gender pay  m-point
0  1001 2013-01-02    beijing    100-A   23  1200.0    male   Y       10
1  1002 2013-01-03         sh    100-B   44  3299.5  female   N       12
2  1003 2013-01-04  guangzhou    110-A   54  2133.0    male   Y       20
3  1004 2013-01-05   shenzhen    110-C   32  5433.0  female   Y       40
4  1005 2013-01-06   shanghai    210-A   34  3299.5    male   N       40
5  1006 2013-01-07    beijing    130-F   32  4432.0  female   Y       40

#其他数据表匹配模式

df_left=pd.merge(df,df1,how='left')

df_right=pd.merge(df,df1,how='right')

df_outer=pd.merge(df,df1,how='outer')
```
set index
```
>>> df_inner.set_index('id')
```
sort by some cloumns
```
>>> df_inner.sort_values(by=['age'])
     id       date       city category  age   price  gender pay  m-point
0  1001 2013-01-02    beijing    100-A   23  1200.0    male   Y       10
3  1004 2013-01-05   shenzhen    110-C   32  5433.0  female   Y       40
5  1006 2013-01-07    beijing    130-F   32  4432.0  female   Y       40
4  1005 2013-01-06   shanghai    210-A   34  3299.5    male   N       40
1  1002 2013-01-03         sh    100-B   44  3299.5  female   N       12
2  1003 2013-01-04  guangzhou    110-A   54  2133.0    male   Y       20
```
sort by index
```
>>> df_inner.sort_index()
     id       date       city category  age   price  gender pay  m-point
0  1001 2013-01-02    beijing    100-A   23  1200.0    male   Y       10
1  1002 2013-01-03         sh    100-B   44  3299.5  female   N       12
2  1003 2013-01-04  guangzhou    110-A   54  2133.0    male   Y       20
3  1004 2013-01-05   shenzhen    110-C   32  5433.0  female   Y       40
4  1005 2013-01-06   shanghai    210-A   34  3299.5    male   N       40
5  1006 2013-01-07    beijing    130-F   32  4432.0  female   Y       40
```
对复合多个条件的数据进行分组标记
```
>>> df_inner.loc[(df_inner['city']=='beijing')& (df_inner['price']>=4000),'sign']=1
>>> df_inner
     id       date       city category  age   price  gender pay  m-point group  sign
0  1001 2013-01-02    beijing    100-A   23  1200.0    male   Y       10   low   NaN
1  1002 2013-01-03         sh    100-B   44  3299.5  female   N       12  high   NaN
2  1003 2013-01-04  guangzhou    110-A   54  2133.0    male   Y       20   low   NaN
3  1004 2013-01-05   shenzhen    110-C   32  5433.0  female   Y       40  high   NaN
4  1005 2013-01-06   shanghai    210-A   34  3299.5    male   N       40  high   NaN
5  1006 2013-01-07    beijing    130-F   32  4432.0  female   Y       40  high   1.0
```
数据分列
```
>>> pd.DataFrame((x.split('-') for x in df_inner['category']),index=df_inner.index,columns=['category','size'])
  category size
0      100    A
1      100    B
2      110    A
3      110    C
4      210    A
5      130    F

>>> split = pd.DataFrame((x.split('-') for x in df_inner['category']),index=df_inner.index,columns=['category','size'])
>>> split
  category size
0      100    A
1      100    B
2      110    A
3      110    C
4      210    A
5      130    F
>>> df_inner = pd.merge(df_inner,split,right_index=True,left_index=True)
>>> df_inner
     id       date       city category_x  age   price  gender pay  m-point group  sign category_y size
0  1001 2013-01-02    beijing      100-A   23  1200.0    male   Y       10   low   NaN        100    A
1  1002 2013-01-03         sh      100-B   44  3299.5  female   N       12  high   NaN        100    B
2  1003 2013-01-04  guangzhou      110-A   54  2133.0    male   Y       20   low   NaN        110    A
3  1004 2013-01-05   shenzhen      110-C   32  5433.0  female   Y       40  high   NaN        110    C
4  1005 2013-01-06   shanghai      210-A   34  3299.5    male   N       40  high   NaN        210    A
5  1006 2013-01-07    beijing      130-F   32  4432.0  female   Y       40  high   1.0        130    F
```
#### 数据提取

#####　按标签提取(loc)
```
Loc函数按数据表的索引标签进行提取，下面的代码中提取了索引列为3的单条数据。

>>> df_inner.loc[3]
id                           1004
date          2013-01-05 00:00:00
city                     shenzhen
category_x                  110-C
age                            32
price                        5433
gender                     female
pay                             Y
m-point                        40
group                        high
sign                          NaN
category_y                    110
size                            C
Name: 3, dtype: object

>>> df_inner.loc[3:5]
     id       date      city category_x  age   price  gender pay  m-point group  sign category_y size
3  1004 2013-01-05  shenzhen      110-C   32  5433.0  female   Y       40  high   NaN        110    C
4  1005 2013-01-06  shanghai      210-A   34  3299.5    male   N       40  high   NaN        210    A
5  1006 2013-01-07   beijing      130-F   32  4432.0  female   Y       40  high   1.0        130    F
```
Reset_index函数用于恢复索引，这里我们重新将date字段的日期设置为数据表的索引，并按日期进行数据提取。



重设索引
```
df_inner.reset_index()

>>>df_inner=df_inner.set_index('date')
>>> df_inner[:'2013-01-05']
              id       city category_x  age   price  gender pay  m-point group  sign category_y size
date
2013-01-02  1001    beijing      100-A   23  1200.0    male   Y       10   low   NaN        100    A
2013-01-03  1002         sh      100-B   44  3299.5  female   N       12  high   NaN        100    B
2013-01-04  1003  guangzhou      110-A   54  2133.0    male   Y       20   low   NaN        110    A
2013-01-05  1004   shenzhen      110-C   32  5433.0  female   Y       40  high   NaN        110    C
```
##### 按位置提取(iloc)

使用iloc函数按位置对数据表中的数据进行提取，这里冒号前后的数字不再是索引的标签名称，而是数据所在的位置，从0开始
```
>>> df_inner.iloc[:2,:3]
              id     city category_x
date
2013-01-02  1001  beijing      100-A
2013-01-03  1002       sh      100-B

>>> df_inner.iloc[[1,2,5],[2,3]]
           category_x  age
date
2013-01-03      100-B   44
2013-01-04      110-A   54
2013-01-07      130-F   32
```
##### 按标签和位置提取（ix）

ix是loc和iloc的混合，既能按索引标签提取，也能按位置进行数据提取。下面代码中行的位置按索引日期设置，列按位置设置。
```
>>> df_inner.ix[:'2013-01-04',2:4]
           category_x  age
date
2013-01-02      100-A   23
2013-01-03      100-B   44
2013-01-04      110-A   54

>>> df_inner['city'].isin(['beijing'])
date
2013-01-02     True
2013-01-03    False
2013-01-04    False
2013-01-05    False
2013-01-06    False
2013-01-07     True
Name: city, dtype: bool

>>> df_inner.loc[df_inner['city'].isin(['beijing','shanghai'])]
              id      city category_x  age   price  gender pay  m-point group  sign category_y size
date
2013-01-02  1001   beijing      100-A   23  1200.0    male   Y       10   low   NaN        100    A
2013-01-06  1005  shanghai      210-A   34  3299.5    male   N       40  high   NaN        210    A
2013-01-07  1006   beijing      130-F   32  4432.0  female   Y       40  high   1.0        130    F


>>> category=df_inner['category_x']
>>> category
date
2013-01-02    100-A
2013-01-03    100-B
2013-01-04    110-A
2013-01-05    110-C
2013-01-06    210-A
2013-01-07    130-F
Name: category_x, dtype: object
>>> pd.DataFrame(category.str[:3])
           category_x
date
2013-01-02        100
2013-01-03        100
2013-01-04        110
2013-01-05        110
2013-01-06        210
2013-01-07        130
```
#### 数据筛选
```
#使用“与”条件进行筛选

>>> df_inner.loc[(df_inner['age']>20)& (df_inner['city']=='beijing'),['id','city','age','category_x','gender']]
     id     city  age category_x  gender
0  1001  beijing   23      100-A    male
5  1006  beijing   32      130-F  female


#对筛选后的数据按sum字段进行求和

>>> df_inner.loc[(df_inner['age']>20) | (df_inner['city']=='beijing'),['id','city','age','category_x','gender']].age.sum()
219

计数
>>> df_inner.loc[(df_inner['age']>20) | (df_inner['city']=='beijing'),['id','city','age','category_x','gender']].age.count()
6

```

#### 数据汇总

对所有列进行计数汇总
```
>>> df_inner.groupby('city')
<pandas.core.groupby.groupby.DataFrameGroupBy object at 0x03B89050>
>>> df_inner.groupby('city').count()
           id  date  category_x  age  price  gender  pay  m-point  category_y  size
city
beijing     2     2           2    2      2       2    2        2           2     2
guangzhou   1     1           1    1      1       1    1        1           1     1
sh          1     1           1    1      1       1    1        1           1     1
shanghai    1     1           1    1      1       1    1        1           1     1
shenzhen    1     1           1    1      1       1    1        1           1     1

>>> df_inner.groupby('city')['id'].count()
city
beijing      2
guangzhou    1
sh           1
shanghai     1
shenzhen     1
Name: id, dtype: int64
```
对两个字段进行汇总计数
```
>>> df_inner.groupby(['city','size'])['id'].count()
city       size
beijing    A       1
           F       1
guangzhou  A       1
sh         B       1
shanghai   A       1
shenzhen   C       1
Name: id, dtype: int64

```
对city字段进行汇总并计算price的合计和均值
```
>>> df_inner.groupby('city')['price'].agg([len,np.sum,np.mean])
           len     sum    mean
city
beijing    2.0  5632.0  2816.0
guangzhou  1.0  2133.0  2133.0
sh         1.0  3299.5  3299.5
shanghai   1.0  3299.5  3299.5
shenzhen   1.0  5433.0  5433.0
```
数据透视表
```
>>> pd.pivot_table(df_inner,index=["city"],values=["price"],columns=["size"],aggfunc=[len,np.sum],fill_value=0,margins=True)
            len                   sum
          price                 price
size          A  B  C  F  All       A       B     C     F      All
city
beijing       1  0  0  1  2.0  1200.0     0.0     0  4432   5632.0
guangzhou     1  0  0  0  1.0  2133.0     0.0     0     0   2133.0
sh            0  1  0  0  1.0     0.0  3299.5     0     0   3299.5
shanghai      1  0  0  0  1.0  3299.5     0.0     0     0   3299.5
shenzhen      0  0  1  0  1.0     0.0     0.0  5433     0   5433.0
All           3  1  1  1  6.0  6632.5  3299.5  5433  4432  19797.0
```

#### 数据统计
```
>>> df_inner.sample(n=3)
              id      city category_x  age   price  gender pay  m-point category_y size
date
2013-01-02  1001   beijing      100-A   23  1200.0    male   Y       10        100    A
2013-01-05  1004  shenzhen      110-C   32  5433.0  female   Y       40        110    C
2013-01-06  1005  shanghai      210-A   34  3299.5    male   N       40        210    A


weights = [0, 0, 0, 0, 0.5, 0.5]
>>> df_inner.sample(n=2, weights=weights)
              id      city category_x  age   price  gender pay  m-point category_y size
date
2013-01-07  1006   beijing      130-F   32  4432.0  female   Y       40        130    F
2013-01-06  1005  shanghai      210-A   34  3299.5    male   N       40        210    A
```
采样后放回
```
>>> df_inner.sample(n=6, replace=True)
              id       city category_x  age   price  gender pay  m-point category_y size
date
2013-01-03  1002         sh      100-B   44  3299.5  female   N       12        100    B
2013-01-06  1005   shanghai      210-A   34  3299.5    male   N       40        210    A
2013-01-04  1003  guangzhou      110-A   54  2133.0    male   Y       20        110    A
2013-01-07  1006    beijing      130-F   32  4432.0  female   Y       40        130    F
2013-01-06  1005   shanghai      210-A   34  3299.5    male   N       40        210    A
2013-01-07  1006    beijing      130-F   32  4432.0  female   Y       40        130    F
```
采样后不放回
```
>>> df_inner.sample(n=6, replace=False)
              id       city category_x  age   price  gender pay  m-point category_y size
date
2013-01-05  1004   shenzhen      110-C   32  5433.0  female   Y       40        110    C
2013-01-02  1001    beijing      100-A   23  1200.0    male   Y       10        100    A
2013-01-06  1005   shanghai      210-A   34  3299.5    male   N       40        210    A
2013-01-07  1006    beijing      130-F   32  4432.0  female   Y       40        130    F
2013-01-04  1003  guangzhou      110-A   54  2133.0    male   Y       20        110    A
2013-01-03  1002         sh      100-B   44  3299.5  female   N       12        100    B
```
数据表描述性统计
```
>>> df_inner.describe().round(2)
            id    age    price  m-point
count     6.00   6.00     6.00     6.00
mean   1003.50  36.50  3299.50    27.00
std       1.87  10.88  1523.35    14.63
min    1001.00  23.00  1200.00    10.00
25%    1002.25  32.00  2424.62    14.00
50%    1003.50  33.00  3299.50    30.00
75%    1004.75  41.50  4148.88    40.00
max    1006.00  54.00  5433.00    40.00
>>> df_inner.describe().round(2).T
         count    mean      std     min      25%     50%      75%     max
id         6.0  1003.5     1.87  1001.0  1002.25  1003.5  1004.75  1006.0
age        6.0    36.5    10.88    23.0    32.00    33.0    41.50    54.0
price      6.0  3299.5  1523.35  1200.0  2424.62  3299.5  4148.88  5433.0
m-point    6.0    27.0    14.63    10.0    14.00    30.0    40.00    40.0
```
标准差
```
>>> df_inner['price'].std()
1523.3516337339847
```
协方差
```
>>> df_inner['price'].cov(df_inner['m-point'])
17263.0
>>> df_inner.cov()
             id     age      price  m-point
id          3.5    -0.7     1946.0     25.4
age        -0.7   118.3    -1353.5    -31.0
price    1946.0 -1353.5  2320600.2  17263.0
m-point    25.4   -31.0    17263.0    214.0
```
相关性分析
```
>>> df_inner['price'].corr(df_inner['m-point'])
0.7746565925361043
>>> df_inner.corr()
               id       age     price   m-point
id       1.000000 -0.034401  0.682824  0.928096
age     -0.034401  1.000000 -0.081689 -0.194833
price    0.682824 -0.081689  1.000000  0.774657
m-point  0.928096 -0.194833  0.774657  1.000000
```

#### 数据输出
```
>>> df_inner.to_csv('excel_to_python.csv')
>>> df_inner.to_excel('excel_to_python.xlsx', sheet_name='bluewhale_cc')


>>> def table_info(x):
...     shape=x.shape
...     types=x.dtypes
...     colums=x.columns
...     print("数据维度(行，列):\n",shape)
...     print("数据格式:\n",types)
...     print("列名称:\n",colums)
...
>>> table_info(df_inner)
数据维度(行，列):
 (6, 10)
数据格式:
 id              int64
city           object
category_x     object
age             int64
price         float64
gender         object
pay            object
m-point         int64
category_y     object
size           object
dtype: object
列名称:
 Index(['id', 'city', 'category_x', 'age', 'price', 'gender', 'pay', 'm-point',
       'category_y', 'size'],
      dtype='object')
 ```


```
pd.get_dummies(df,colums = ['xx'])
```
