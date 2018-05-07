# MyETC

#### 项目介绍
由于票根网(txffp.com)功能各种不全，超级难用，罄竹难书。只好自己写一个软件自动申请开票，下载发票，合并PDF
功能介绍：
1. 从ETC按结算日期下载所有车辆的通行结算详情。
2. 从票根网下载上月、上上月的通行记录。
3. 比对结算记录和票根的通行记录，申请开票。
4. 下载当前月申请开票的发票记录
5. 解压缩下载的发票
6. 合并PDF文件。一个文件包含一部车通行记录、发票。方便打印

#### 软件架构
软件架构说明
1. com:python程序公用的代码，可以用到其他项目上。
2. build：pyinstaller生成exe程序时的编译文件，可删除。
3. dist：pyinstaller生产exe程序时的目标文件夹。
4. cookie.txt:是票根网登陆后，保存cookie的文件。
5. etcOperateSeek.py：etc网站的操作文件。
6. main.py：主程序。分为6步骤，完成。
7. main.spec：pyinstaller生成exe的配置文件。
8. requirements.txt：程序依赖的包列表。
9. txffpOperate.py：票根网的操作文件。


#### 安装教程

1. install python3.6.5
2. pip install requirements.txt
3. xxxx

#### 使用说明

1. 根目录下建一个cookie.txt
2. 运行main.exe，按操作提示运行。
3. main.spec是pyinstaller的配置文件，生产exe文件时，用pyinstaller main.spec指令，生成的文件在dist目录下。
4. 11.ico是windows系统下，exe程序的图标。可自行修改。

#### 参与贡献

1. Fork 本项目
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request