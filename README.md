【文件目录说明】
1. venv 虚拟环境目录（因为安装了selenium，怕直接运行时出现webdriver等版本问题）
2. setup.up 一些条件依赖的安装
3. silent_install.py 自动运行框架，主运行程序
4. URL目录下：每个txt文件包含属于其中一个类别的Firefox扩展安装链接列表，文件名称即
类别名称
5. FIN目录下：最终输出目录，每次silent_install遍历完成一个类别，该目录下即生成一个
相同明明的输出txt文件
6. honey：原搭建的honeysite项目

【运行步骤】
1. root权限运行setup.sh 安装依赖
2. cd ./venv/ && source bin/activate 启动虚拟环境
3. 修改silent_install.py中的变量，具体内容如下方【注】所示
4. python运行 silent_install.py 即可
#可能显示存在部分安装包需要pip安装


【注】
分别修改silent_install.py中的以下环境变量
1. source_path 目标输入文件的地址（41行）
2. dst_path  测试输出结果存放地址（42行）
3. url_to_honeysite = honeysite项目中index.html的目录（43行
