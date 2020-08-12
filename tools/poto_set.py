import urllib.request
import requests
import os.path
import ctypes
import time
import win32api, win32con, win32gui
from PIL import Image
# 第一、获取图片地址  这个函数主要通过requests模块，根据必应的网页地址，获取到当日图片的最终img地址。
# 请求网页，跳转到最终 img 地址 
def get_img_url(raw_img_url="https://area.sinaapp.com/bingImg/"):
    r = requests.get(raw_img_url)
    img_url = r.url  # 得到图片文件的网址
    print('img_url:', img_url)
    return img_url


#  第二、保存图片到本地 这个函数的作用就是把图片保存到你自己设置的一个目录下，并返回当前目录的绝对地址。
def save_img(img_url, dirname):
    # 保存图片到磁盘文件夹dirname中
    try:
        if not os.path.exists(dirname):
            print('文件夹', dirname, '不存在，重新建立')
            # os.mkdir(dirname)
            os.makedirs(dirname)
        # 获得图片文件名，包括后缀
        basename = "bing.jpg"
        # 拼接目录与文件名，得到图片路径
        filepath = os.path.join(dirname, basename)
        # 下载图片，并保存到文件夹中
        urllib.request.urlretrieve(img_url, filepath)
        name = str(time.strftime('%Y-%m-%d' ,time.localtime(time.time())))
        urllib.request.urlretrieve(img_url, 'D:/图片/bing/'+ name + '.jpg')
    except IOError as e:
        print('文件操作失败', e)
    except Exception as e:
        print('错误 ：', e)
    print("Save", filepath, "successfully!")
 
    return filepath


#  第三、设置该绝对路径所指向的图片为壁纸 
#  通过之前获得的图片所在的绝对路径，把该图片设置为桌面壁纸。
def set_img_as_wallpaper(filepath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 3)
    print('设置完成')

#  第四、运行代码的main函数 
def main():
    dirname = "C:/poto/"  # 图片要被保存在的位置
    img_url = get_img_url()
    filepath = save_img(img_url, dirname)  # 图片文件的路径
    print(filepath)
    set_img_as_wallpaper(filepath)


def setWallPaperBMP(imagePath):
    bmpImage = Image.open(imagePath)
    newPath = imagePath.replace('.jpg', '.bmp')
    bmpImage.save(newPath, "BMP")

def set_wallpaper(img_path):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_path, win32con.SPIF_SENDWININICHANGE)
#注意这里路径使用的是/而不是\


if __name__ == '__main__':
    main()
    setWallPaperBMP('C:/poto/bing.jpg')
    set_wallpaper('C:/poto/bing.BMP')
# @echo off
# del g:\bingImg\*.jpg
# python SetBingImgAsWallpaper.py
#  