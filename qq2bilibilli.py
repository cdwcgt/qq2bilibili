# -*-coding:utf-8 -*-
import json
import re
import os
import socket
import urllib.request as urllib2
from threading import Timer
from bilibili_api.dynamic import DrawDynamic, TextDynamic, InstantDynamic, UploadImages, ScheduleDynamic
from bilibili_api import Verify
from cqhttp import CQHttp, Error

# 设置超时时间为30s
socket.setdefaulttimeout(30)

#临时图片文件夹创建
folder = os.path.exists("./imgs")
if folder == False:
    os.makedirs("./imgs")

# 验证类
verify = Verify(sessdata="", csrf="")

# 上传图片路径列表
img_path = []
'''
Python 数组
https://www.w3school.com.cn/python/python_arrays.asp
'''
bot = CQHttp(api_root='http://127.0.0.1:5700/',
             access_token='',
             secret='')

# 计时器重置
timer1 = None
timer2 = None
suo1 = False
suo2 = False
suo3 = False
temp3 = ""
temp4 = 0
admin = 0
mubiao={'user_id': admin}
#print(timer)
#print(suo1)
# 计时结束


def suo():
    global suo1
    suo1 = False
    bot.send(mubiao, 'CD结束')
    print("CD结束")


def suox():
    global suo2
    global suo3
    suo2 = False
    suo3 = False
    bot.send(mubiao, '超时取消')
    print("超时取消`")


def findpic(string):  # 提取图片url
    # findall() 查找匹配正则表达式的字符串
    #url = re.findall('url=([^\]]+)', string)
    url = re.findall(r'url=([^\]]+)', string)
    return url


def downloadpic(shuzu):  # 下载图片
    # findall() 查找匹配正则表达式的字符串
    #url = re.findall('url=([^\]]+)', string)
    if len(shuzu) == 0:
        return 0
    i = 0
    while i < len(shuzu):
        print('downloading with urllib2', i)
        # 解决下载不完全问题且避免陷入死循环
        try:
            urllib2.urlretrieve(shuzu[i], "./imgs/"+str(i)+".jpg")
        except socket.timeout:
            count = 1
            while count <= 3:
                try:
                    urllib2.urlretrieve(shuzu[i], "./imgs/"+str(i)+".jpg")
                    break
                except socket.timeout:
                    err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                    print(err_info)
                    count += 1
            if count > 3:
                print("图片下载失败")
                return -1
        #print(urllib2.urlretrieve(shuzu[i], "./imgs/"+str(i)+".jpg"))
        img_path.append("./imgs/"+str(i)+".jpg")
        i = i+1
    return len(shuzu)  # 返回数组长度


'''
Python爬虫——解决urlretrieve下载不完整问题且避免用时过长_Python_山阴少年-CSDN博客
https://blog.csdn.net/jclian91/article/details/77513289
'''


def findtext(string):  # 提取文本
    if string.find("[CQ:image,") == -1:
        print("未检测到图片链接")
        bot.send(mubiao, '未检测到图片链接')
        return string
    i = 0
    str_end = ""
    for i in string.split("[CQ:image"):
        print(i)
        if i.find(']')>=0:
            str_end=str_end+i[i.find(']')+1:]
        else :
            str_end=str_end+i
    return str_end


@bot.on_message
def handle_msg(event):
    global suo1
    global suo2
    global suo3
    global temp3
    global temp4
    global timer1
    global timer2
    if event['user_id'] == admin and event['message_type'] == 'private':
        # print(event)
        message = event['message']
        if message == "":  # 大概没用，因为QQ发不出空消息
            return
        # print(message)
        if suo3 == True:
            print(temp3)
            if message != "ok":
                bot.send(mubiao, '已停止发送动态')
                suo1 = False
                suo2 = False
                suo3 = False
                suo3 = False
                temp3 = None
                temp4 = None
                timer1.cancel()
                return
            if temp4 > 0:
                print('发送图文')
                # 上传图片类
                upload = UploadImages(images_path=img_path, verify=verify)
                draw = DrawDynamic(text=temp3,upload_images=upload,verify=verify)
                instant = InstantDynamic(draw)
            elif temp4 == 0:
                print('发送文字')
                text = TextDynamic(text=temp3, verify=verify)
                instant = InstantDynamic(text)
            print(instant.send())
            bot.send(mubiao, '发送动态成功')
            print('发送动态成功')
            suo1 = True
            suo2 = False
            suo3 = False
            temp3 = None
            temp4 = None
            timer1.cancel()
            timer2 = Timer(60, suo)  # 冻结60秒计时
            timer2.start()
            print("一分钟计时开始")
            return
        if suo2 == True:
            if message == "取消":
                suo2 == False
                print('已取消')
                bot.send(mubiao, '已取消')
                return
            try:
                temp2 = findpic(message)
                print(temp2)  # 返回图片url数组
                if len(temp2) >= 9:
                    suo2 == False
                    print('图片大于9张')
                    bot.send(mubiao, '图片大于9张')
                    return
                temp3 = findtext(message)
                print(temp3)  # 返回字符串
                temp4 = downloadpic(temp2)  # 下载图片
                if temp4 == -1:
                    print("下载图片失败")
                    bot.send(mubiao, '下载图片失败')
                    suo1 = False
                    suo2 = False
                    suo3 = False
                    suo3 = False
                    temp3 = None
                    temp4 = None
                    timer1.cancel()
                    return
                suo3 = True
                print("拆出的文字："+temp3)
                bot.send(mubiao, "拆出的文字："+temp3)
                print('是否确定要发送？确定输入ok，否则输入任何字符或等待超时取消')
                bot.send(mubiao, '是否确定要发送？确定输入ok，否则输入任何字符或等待超时取消')

            except Exception as err:  # FileExistsError or OSError:
                print(str(err))
                suo1 = False
                suo2 = False
                suo3 = False
                suo3 = False
                temp3 = None
                temp4 = None
                timer1.cancel()
                bot.send(mubiao, '发b站动态出错:'+str(err))
        #pair = message.startswith("发送内容")
        if message == "发送内容" and suo1 == False:
            suo2 = True
            bot.send(mubiao, '请在120秒内输入消息')
            timer1 = Timer(120, suox)
            timer1.start()
            return

if __name__ == '__main__':
    '''
    wenjianjia='./imgs/'
    try:
        os.makedirs(wenjianjia)#自动创建目录，发现目录
    except Exception as err:  # FileExistsError or OSError:
        print(str(err))
    '''
    bot.run(host='127.0.0.1', port=8887)

#未严格测试！！！！！！！！！！！！！！！！！！！！！！！

