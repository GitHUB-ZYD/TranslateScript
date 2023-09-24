import tkinter as tk
from pynput import mouse, keyboard
import pyperclip
from flask import Flask, render_template, request, jsonify
import requests
import hashlib
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


def show_hidden_window(chinese,english):
    hidden_window = tk.Toplevel()
    hidden_window.title("翻译结果")
    label1 = tk.Label(hidden_window, text="中文：" + chinese, wraplength=150)
    label1.pack(padx=20, pady=10)
    label2 = tk.Label(hidden_window, text="英文：" + english,wraplength=150)
    label2.pack(padx=40, pady=20)

    

def on_button_click():
    chinese = pyperclip.paste()
    print("翻以前",chinese)
    (english,chinese) = _translate(chinese)
    print('chinese',chinese)
    print("english",english)
    
    show_hidden_window(chinese,english)

# 创建主窗口
root = tk.Tk()
window_width = 250
window_height = 50
window_size = f"{window_width}x{window_height}"
root.geometry(window_size)
root.title("百度翻译api")
# 设置窗口在最顶层
root.attributes('-topmost', True)

# 创建一个按钮，点击按钮时显示隐藏窗口
button = tk.Button(root, text="点击我翻译", command=on_button_click)
button.pack(padx=20, pady=10)

# 启动主循环
root.mainloop()


