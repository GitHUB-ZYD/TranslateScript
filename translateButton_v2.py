import tkinter as tk
import tkinter.font as tkFont
import pyperclip
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
    fontExample = tkFont.Font(family="微软雅黑", size=16, weight="bold")
    hidden_window = tk.Toplevel(width=80,height=60)
    hidden_window.title("翻译结果")
    text1 = tk.Text(hidden_window,wrap=tk.WORD,height=5,width=20)
    text1.insert(tk.END,chinese)
    # text1.pack(padx=20, pady=20)
    text1.grid(row=0,column=0,columnspan=3,rowspan=1,sticky="nwse")
    text2 = tk.Text(hidden_window,wrap=tk.WORD,height=5,width=20)
    text2.insert(tk.END,english)
    text2.grid(row=1,column=0,columnspan=3,rowspan=1,sticky="nwse")
    # text2.pack(padx=20,pady=20)
    text1.configure(font=fontExample)
    text2.configure(font=fontExample)
    def afterEdit():
        (english,chinese) = _translate(text2.get('1.0',tk.END))
        text1.delete('1.0',tk.END)
        text2.delete('1.0',tk.END)
        text1.insert(tk.END,chinese)
        text2.insert(tk.END,english)
    def afterSelect():
        (english,chinese) = _translate(text2.get(tk.SEL_FIRST, tk.SEL_LAST))
        text1.delete('1.0',tk.END)
        text2.delete('1.0',tk.END)
        text1.insert(tk.END,chinese)
        text2.insert(tk.END,english)
    def clipBoard():
        (english,chinese) = _translate(pyperclip.paste())
        text1.delete('1.0',tk.END)
        text2.delete('1.0',tk.END)
        text1.insert(tk.END,chinese)
        text2.insert(tk.END,english)
    button1 = tk.Button(hidden_window,text="选中后翻译",command=afterSelect)
    # button1.pack(padx=5,pady=20,side=tk.BOTTOM)
    button1.grid(row=2,column=0,columnspan=1,pady=5)
    button2 = tk.Button(hidden_window,text="系统剪切板翻译",command=clipBoard)
    # button2.pack(padx=5,pady=20,side=tk.BOTTOM)
    button2.grid(row=2,column=1,columnspan=1,pady=5)
    button3 = tk.Button(hidden_window,text="编辑后翻译",command=afterEdit)
    # button3.pack(padx=5,pady=20,side=tk.BOTTOM)
    button3.grid(row=2,column=2,columnspan=1,pady=5)
    
def on_button_click():
    english = pyperclip.paste()
    try:
        (english,chinese) = _translate(english)
        print('chinese',chinese)
        print("english",english)
        show_hidden_window(chinese,english)
    except Exception as e:
        print(e)
        show_hidden_window("剪切板内容为空","Clipboard is NULL")
        
         

# 创建主窗口
root = tk.Tk()
stringVar = tk.StringVar()


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


