![image](https://github.com/blackye/lalascan/blob/master/logo.png)
What's lalascan?
===================================  
Web vulnerability scanner framework

Basic usage
===================================  

```
 _          _
| |    __ _| | __ _ ___  ___ __ _ _ __
| |   / _` | |/ _` / __|/ __/ _` | '_ \
| |__| (_| | | (_| \__ \ (_| (_| | | | |
|_____\__,_|_|\__,_|___/\___\__,_|_| |_|

LalaScan WebApplication vul scanner!
usage:

optional arguments:
  -h, --help            Show help message and exit
  --version             Show program's version number and exit

[ Targets ]:
  -u URL, --url URL     Target URL (e.g. "http://www.lalascan.com/")
  -t PROCESS_NUM, --threads PROCESS_NUM
                        max number of process, default cpu number

[ Resource Found ]:
  -S, --spider          Enable user Spider

[ Plugin Option ]:
  -e PLUGIN, --enable-plugin PLUGIN
                        enable a plugin

[ Request Option ]:
  --data POST DATA      HTTP Post data
  --cookie COOKIE       HTTP Cookie header value
  --referer REFERER     HTTP Referer header value
  --user-agent AGENT    HTTP User-Agent header value
  --random-agent        Use randomly selected HTTP User-Agent header value
  --proxy PROXY         Use a proxy to connect to the target URL
  --timeout TIMEOUT     Seconds to wait before timeout connection (default 30)
  --retry RETRY         Time out retrials times.

```

###正在开发中........

