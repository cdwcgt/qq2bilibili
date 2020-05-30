# qq2bilibili
~~***目前还有图片文字拆分问题，请不要使用图文发送!!!***~~
此项目用于在qq中发送bilibili动态
使用了requests和[cqhttp](https://github.com/cqmoe/python-cqhttp)第三方库，使用前请配置环境
```sh
pip install requests
```
```sh
pip install cqhttp
```
使用了以下存储库(已集成无需下载)
[bilibili_api](https://github.com/Passkou/bilibili_api)
# 用法:
修改bilibili.py中的admin变量
```sh
admin = 0
```
改为
```sh
admin = 你的QQ号
```
# httpapi修改
在bilibiliqq.py中找到这段
```sh
bot = CQHttp(api_root='http://127.0.0.1:5700/',
             access_token='须于httpapi插件配置一致',
             secret='须于httpapi插件配置一致')
```
按说明修改
# 获取b站验证信息
通过这个[专栏](https://www.bilibili.com/read/cv4495682)获取sessdata与csrf
在bilibili.py中找到这段

```sh
# 验证类
verify = Verify(sessdata="填写获取到的sessdata", csrf="填写获取到的csrf	")
```
按说明填写

# 修改http插件配置
在httpapi插件目录中找到配置文件(一般为"config/机器人qq号.json")
将 "post_url"改为"http://127.0.0.1:8887"
以下是我的配置，若无特殊需要可以直接复制(使用此配置时无需修改[bilibiliqq.py中的"access_token"与"secret"](https://github.com/cdwcgt/bilibiliqq/blob/master/README.md#httpapi修改))
```sh
{
    "host": "",
    "port": 5700,
    "use_http": true,
    "ws_host": "",
    "ws_port": 6700,
    "use_ws": false,
    "ws_reverse_url": "",
    "ws_reverse_api_url": "",
    "ws_reverse_event_url": "",
    "ws_reverse_reconnect_interval": 3000,
    "ws_reverse_reconnect_on_code_1000": true,
    "use_ws_reverse": false,
    "post_url": "http://127.0.0.1:8887",
    "access_token": "",
    "secret": "",
    "post_message_format": "string",
    "serve_data_files": true,
    "update_source": "github",
    "update_channel": "stable",
    "auto_check_update": false,
    "auto_perform_update": false,
    "show_log_console": true,
    "log_level": "info"
}
```
使用配置完环境的python启动bilibiliqq.py
私聊自己的机器人，发送"发送内容"
你会有120s的时间发送文字及图片(图文须同时发送，即一个消息中包含图片与文字)
