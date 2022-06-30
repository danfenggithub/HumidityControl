如果放在Linux后台用python 命令符运行
首先要在ubuntu下添加PYTHONPATH方法，否则会报找不到模块的错误

在用户主目录下有一个 .bashrc 隐藏文件，可以在此文件中加入 PATH 的设置如下：

$ gedit ~/.bashrc
加入：
export PATH=<你的要加入的路径>:$PATH
如果要加入多个路径，只要：
export PATH=<你要加入的路径1>:<你要加入的路径2>: ...... :$PATH
当中每个路径要以冒号分隔。
这样每次登录都会生效
添加PYTHONPATH的方法也是这样，在.bashrc中添加

export PYTHONPATH=/home/ldfu/Roomlinux:$PYTHONPATH
其中，Roomlinux是项目根路径

保存后在终端输入 $ source ~/.bashrc 使环境变量立即生效

在ubuntu下添加PYTHONPATH [ 纯命令 ]
1. gedit ~/.bashrc
2. 在.bashrc文本最后添加（其中，Roomlinux是项目根路径）
    export PYTHONPATH=/home/ldfu/Roomlinux:$PYTHONPATH
    export PYTHONPATH=/home/bupt/Room:$PYTHONPATH
3. source ~/.bashrc

查看显卡程序
watch -n 1 nvidia-smi