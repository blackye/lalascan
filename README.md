What's lalascan?
===================================  
Web vulnerability scanner framework

Basic usage
===================================  

```
	
Usage: lalascan.py [Auth] [Options] [Targets]

[Auth]
	-s --server: web server地址，为域名或ip
	-t --token: token，在用户－设置界面可用找到并更新
[Options]
	-u --update-plugins: 更新本地插件至web，可用指定本地插件目录
	-v --verbose: 输出内容更加详细，默认输出内容为info，－v则为debug
	   --threads: 进程数量，默认为cpu核数
	   --auto-proxy: 启用自动代理
	-h : 输出帮助信息
[Targets]
	-T --target: 目标，可以为ip、host、url或ip范围,当使用－p模式时还可以是文件
	   --no-gather: 不使用信息收集模块，也可以用下面的--gather-depth=0实现
	   --gather-depth: 信息收集深度，默认为1
	   --conf-file: 配置文件，默认为conf/basic.conf
	-p --plugin: 单独跑一个插件
	   --plugin-arg: 插件参数，格式为"port=20;name='hammer';"
	-l --listen: 监听模式，在WEB上进行任务分配
	   --max-size: listen模式的最大线程池
	--console: 控制台模式
[Examples]
	hammer.py -s www.hammer.org -t 3r75... --update-plugins plugins/Info_Collect/
	hammer.py -s www.hammer.org -t 3r75... --console
	hammer.py -T http://testphp.vulnweb.com
	hammer.py --conf-file conf/basic.conf
	hammer.py -T vulnweb.com --conf-file conf/basic.conf
	hammer.py -p plugins/System/dnszone.py -T vulnweb.com
	hammer.py -l
```