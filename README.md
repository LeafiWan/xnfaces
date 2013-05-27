# Xiangnan Facemash

## 安装
推荐使用 Unix/Linux，Windows 用户请先安装 Python 2.7。

在终端执行以下命令：

    $ cd ~ 
    $ git clone git@github.com:psjay/xnfaces.git
    $ cd xnfaces
    $ python bootstrap.py 
    $ bin/buildout 

至此安装完毕，这样来跑它：

    $ bin/run_web

用浏览器打开 `http://127.0.0.1:5000` 看看效果吧~

Happy hacking!

## TroubleShooting

**Mac OS X 下，编译 gevent 出错。**

先安装 libevent: `$ brew install libevent`.
