import requests
import hashlib
import win32api
import win32con
from pynput import mouse
import time
import pyperclip
def _getparams(q):
    _from="en"
    to="zh"
    appid='************'
    salt = '************'
    secretKey = "************"
    str1 = appid+q+salt+secretKey
    sign = hashlib.md5(str1.encode()).hexdigest()
    return {'q':q,'from':_from,'to':to,'appid':appid,'salt':salt,'sign':sign}

def _translate(q):
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    res = requests.get(url=url,params=_getparams(q))   
    result = res.json()
    english=""
    chinese=""
    for i in result['trans_result']:
        english+=i['src']
        chinese+=i['dst']
    return (english,chinese)

def getTranslateResult(chinese,english):
    win32api.MessageBox(0,'中文:'+chinese+"\n\n"+"英文:"+english,"翻译结果",win32con.MB_OK)

last_click_time = 0
click_count = 0

def on_click(x, y, button, pressed):
    global last_click_time, click_count

    if pressed:
        current_time = time.time()
        time_since_last_click = current_time - last_click_time
        last_click_time = current_time

        if time_since_last_click < 0.5:  # 判断是否为三击事件
            click_count += 1
            if click_count == 3 :
                english,chinese=_translate(pyperclip.paste())
                getTranslateResult(chinese,english)
                click_count = 0
        else:
            click_count = 1

# 创建鼠标监听器
mouse_listener = mouse.Listener(on_click=on_click)

# 启动监听器
mouse_listener.start()

# 运行监听器，直到按下键盘上的任意键退出
mouse_listener.join()



