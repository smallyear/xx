### 离线安装vscode插件
#### 进入插件官网
[https://marketplace.visualstudio.com/vscode](https://marketplace.visualstudio.com/vscode)
#### 搜索需要安装的插件并下载
该网站上提供了插件下载地址的拼接方式

	https://code.visualstudio.com/docs/editor/extension-gallery?pub=HookyQR&ext=beautify#_common-questions
	

##### 获取下载链接

###### 下载链接的模板为
```
https://${publisher}.gallery.vsassets.io/_apis/public/gallery/publisher/${publisher}/extension/${extension name}/${version}/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage
```
###### 以python插件为例
在插件官网进入python插件的页面
网址为

	https://marketplace.visualstudio.com/items?itemName=ms-python.python
	从这个url中获取
	${publisher}的值为ms-python
	${extension name}的值为python
	${version}的值在界面右侧的More Info获取(当前版本是2018.2.1)
修改之后的下载链接为

	https://ms-python.gallery.vsassets.io/_apis/public/gallery/publisher/ms-python/extension/python/2018.2.1/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage

#### 下载之后安装
下载之后的文件名是
	
	Microsoft.VisualStudio.Services.VSIXPackage

修改文件名为

	python.vsix(文件名随意修改，后缀必须为vsix)

打开vscode，点击扩展右侧的三个点，选择`从VSIX安装`，之后选择文件安装，之后重启即可

#### 几个插件的下载地址
注意版本号切换为最新的
```
python for vscode.vsix
tht13.python
0.2.3
https://tht13.gallery.vsassets.io/_apis/public/gallery/publisher/tht13/extension/python/0.2.3/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage

python.vsix
ms-python.python
2018.2.1
https://ms-python.gallery.vsassets.io/_apis/public/gallery/publisher/ms-python/extension/python/2018.2.1/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage

Markdown All in One.vsix
yzhang.markdown-all-in-one
1.1.0
https://yzhang.gallery.vsassets.io/_apis/public/gallery/publisher/yzhang/extension/markdown-all-in-one/1.1.0/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage

Markdown Preview Enhanced.vsix
shd101wyy.markdown-preview-enhanced
0.3.3
https://shd101wyy.gallery.vsassets.io/_apis/public/gallery/publisher/shd101wyy/extension/markdown-preview-enhanced/0.3.3/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage

Markdown PDF.vsix
yzane.markdown-pdf
0.1.7
https://yzane.gallery.vsassets.io/_apis/public/gallery/publisher/yzane/extension/markdown-pdf/0.1.7/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage

Debugger for Chrome.vsix
msjsdiag.debugger-for-chrome
4.2.0
https://msjsdiag.gallery.vsassets.io/_apis/public/gallery/publisher/msjsdiag/extension/debugger-for-chrome/4.2.0/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage


```