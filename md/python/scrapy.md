#### 数据提取器
```html
<html>
 <head>
  <base href='http://example.com/' />
  <title>Example website</title>
 </head>
 <body>
  <div id='images'>
   <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
   <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
   <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
   <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
   <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
  </div>
 </body>
</html>

```
[smaple](https://doc.scrapy.org/en/latest/_static/selectors-sample1.html)

##### CSS Selector
顾名思义，css selector 就是 css 的语法来定位标签。例如要提取例子网页中 ID 为 images 的 div 下所有 a 标签的文本，使用 css 语法可以这样写：
```shell
>>> response.css('div#images a::text').extract()
['Name: My image 1 ', 'Name: My image 2 ', 'Name: My image 3 ', 'Name: My image 4 ', 'Name: My image 5 ']
```

div#images 表示 id 为 images 的 div，如果是类名为 images，这里就是 div.images。div a 表示该 div 下所有 a 标签，::text 表示提取文本，extract 函数执行提取操作，返回一个列表。

如果只想要列表中第一个 a 标签下的文本，可以使用 extract_first 函数：

```
>>> response.css('div#images a::text').extract_first()
'Name: My image 1 '
extract_first() 方法支持对没有匹配到的元素提供一个默认值：

>>> response.css('div#images p::text').extract_first(default='默认值')
'默认值'
```

获取a标签的href属性
```
response.css('div#images a::attr(href)').extract()
```
获取a标签下图片的地址
```
response.css('div#images a img::attr(href)').extract()
```




##### XPATH
```
//*[@id="images"]/a[1]

  'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d*)[^\d]*')
```

#### scrapy创建爬虫项目
##### scrapy创建爬虫项目
```
scrapy startproject shiyanlou
```
初始化爬虫模版
```
scrapy genspider courses shiyanlou.com
```