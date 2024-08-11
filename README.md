一个将txt文件渲染成400x300分辨率图片并通过网络传输到由微雪墨水屏驱动板驱动的4.2寸墨水屏的工具。
使用前提：
1.一个同时支持中英文点阵显示的字体，推荐Windows系统中的宋体(simsun.ttc)
2.刷好微雪墨水屏驱动的支持WiFi的MCU（如ESP32）
3.一块4.2英寸400x300分辨率的电子墨水屏

工作原理：
einkreader.py通过Python的pillow库，读取txt中的文件，使用指定的字体渲染成适合显示在墨水屏的白底黑字图片。使用点阵字体可以确保文字边缘清晰，不产生任何屏幕无法显示的中间灰色。
upload.py则重写自微雪WiFi墨水屏驱动中提供的上位HTML，向驱动请求EPDn_后在URL中以字符串的形式逐行上传图片数据。上传完毕后请求SHOW_进行屏幕刷新。

使用方法：
编辑einkreader.py文件中最后一行函数的参数，从左到右分别为 txt文件路径 输出文件夹路径 字体文件路径 段落间距。其中指定的输出文件夹路径如果不存在支持自动创建。编辑完毕之后执行一次可获得渲染好的bmp格式图片组。
upload.py则在运行时询问需要传输的图片路径和目标服务器IP地址。
