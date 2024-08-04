# eink-txt-reader
将纯文字txt转换成4.2英寸eink屏幕（分辨率400x300）可以显示的模式<br />
Convert plain text TXT to a mode that can be displayed on a 4.2-inch e-ink screen (resolution 400x300).<br />
Note: Translated by Microsoft Copilot<br />
在淘宝经常可以购买到价格相当便宜的电子墨水屏价格标签，尺寸通常从1寸到8寸不等。我在购买了两块4.2英寸黑白400x300墨水屏之后决定将其做成一种掌上阅读器。使用合适的硬件进行点亮之后接下来就是软件的制作了。<br />
On AliExpress, you can often buy electronic ink screen price tags at quite affordable prices, with sizes ranging from 1 inch to 8 inches. After purchasing two 4.2-inch black and white 400x300 e-ink screens, I decided to turn them into a kind of handheld reader. After lighting them up with suitable hardware, the next step is to create the software.<br />
![img](https://github.com/user-attachments/assets/b391d99c-4f36-451a-957e-ff9433956640)

目前已经实现的功能:<br />
Feature:<br />
1.读取一份纯文本txt中的内容，将其用指定的字体，字号，行数进行渲染（带有自动换行和自动分页），将结果输出为BMP图片格式。此图片格式可通过另一个Arduino项目传输到屏幕。<br />
1.Read the contents of a plain text TXT file, render it using a specified font, font size, and number of lines (with automatic line breaks and pagination), and output the result in BMP image format. This image format can be transmitted to the screen through another Arduino project.<br />
正在编写的功能：<br />
TODO:<br />
1.寻找一种合适的方法将渲染后的图片自动传输并按需换页显示。<br />
1.Find a suitable method to automatically transfer the rendered images and display them with page-turning as needed.<br />
