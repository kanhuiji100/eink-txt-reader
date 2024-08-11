import requests
from PIL import Image
import time

pxInd = 0
stInd = 0
dispW = 0
dispH = 0
dispX = 0
rqPrf = ''
rqMsg = ''

def byte_to_str(v):
    return chr((v & 0xF) + 97) + chr(((v >> 4) & 0xF) + 97)

def word_to_str(v):
    return byte_to_str(v & 0xFF) + byte_to_str((v >> 8) & 0xFF)

def u_send(cmd, next_step):
    global stInd
    url = rqPrf + cmd
    try:
        response = requests.post(url, data=rqMsg + 'iodaLOAD_', timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        time.sleep(1)  # 加一个短暂的延迟，然后重试
        response = requests.post(url, data=rqMsg + 'iodaLOAD_')
    
    if next_step:
        stInd += 1
    return response

def u_next():
    global pxInd
    pxInd = 0
    u_send('NEXT_', True)

def u_done():
    print('Complete!')
    return u_send('SHOW_', True)

def u_show(a, k1, k2):
    global pxInd, rqMsg
    x = str(k1 + k2 * pxInd / len(a))
    if len(x) > 5:
        x = x[:5]
    print(f'Progress: {x}%')

    # 检查并发送最后一个数据块
    if pxInd >= len(a):
        u_send(rqMsg, False)
        return u_done()
    else:
        return u_send(rqMsg, pxInd >= len(a))

def u_data(a, c, k1, k2):
    global rqMsg, pxInd
    rqMsg = ''
    while len(rqMsg) < 1000 and pxInd < len(a):  # 确保数据块长度固定为1000字节
        v = 0
        if c == -1:
            for i in range(0, 16, 2):
                if pxInd < len(a):
                    v |= (a[pxInd] << i)
                    pxInd += 1
        elif c == -2:
            for i in range(0, 16, 4):
                if pxInd < len(a):
                    v |= (a[pxInd] << i)
                    pxInd += 1
        else:
            for i in range(8):
                if pxInd < len(a) and a[pxInd] != c:
                    v |= (128 >> i)
                pxInd += 1
        rqMsg += word_to_str(v) if c < 0 else byte_to_str(v)
    
    return u_show(a, k1, k2)

def u_line(a, c, k1, k2):
    global rqMsg, pxInd
    rqMsg = ''
    while len(rqMsg) < 1000 and pxInd < len(a):  # 确保数据块长度固定为1000字节
        x = 0
        while x < 122 and pxInd < len(a):
            v = 0
            for i in range(8):
                if x < 122:
                    if pxInd < len(a) and a[pxInd] != c:
                        v |= (128 >> i)
                    x += 1
                    pxInd += 1
            rqMsg += byte_to_str(v)
    
    return u_show(a, k1, k2)

def upload_image(file_path):
    global dispW, dispH, pxInd, stInd, rqPrf
    img = Image.open(file_path)
    dispW, dispH = img.size
    pixels = list(img.getdata())
    a = [get_val(pixel) for pixel in pixels]
    dispX = 0
    pxInd = 0
    stInd = 0
    rqPrf = 'http://' + input('Enter IP address: ') + '/'
    
    epdInd = 0

    # 发送固定的初始化请求 EPDn_
    try:
        response = requests.post(rqPrf + 'EPDn_', timeout=10)
        response.raise_for_status()
        print(f"Initialization command EPDn_ sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Initialization failed: {e}")
        return

    def process():
        while pxInd < len(a):
            if epdInd == 25 or epdInd == 37:
                if stInd == 0:
                    u_data(a, -2, 0, 100)
                if stInd == 1:
                    u_done()
            else:
                if stInd == 0 and epdInd == 23:
                    u_data(a, 0, 0, 100)
                if stInd == 0:
                    u_data(a, -1 if epdInd == 1 or epdInd == 12 else 0, 0, 50)
                if stInd == 1:
                    u_next()
                if stInd == 2:
                    u_data(a, 3, 50, 50)
                if stInd == 3:
                    u_done()

    process()

def get_val(pixel):
    r, g, b = pixel[:3]
    return int(0.299 * r + 0.587 * g + 0.114 * b)

if __name__ == "__main__":
    file_path = input('Enter Image File Name :')
    upload_image(file_path)
