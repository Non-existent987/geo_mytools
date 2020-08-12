#!/usr/bin/env python
# coding: utf-8

# In[6]:


############本工具实现输入地市区县编码，自动化抓取兴趣点地理信息表及谷歌earth图层###############

############下面模块实现导入此次工具所需的模块###############################################
import os
import requests
import pandas as pd
import json
import numpy as np
import time
import math

# 各下级行政区的代码，若是嫌逐个复制麻烦可以通过读取文件的方式实现，此处不进行讲解
# 示例arr=['420201','420202','420203','420204','420205','420222','420281']，注意arr是字符串列表

print("程序运行中，请耐心等待结果" )
##############下面模块实现读取D盘区县编码表中编码的功能#######################################
path = 'D:/D盘区县编码表'  # 设置装有adcode_citycode的excel表所在文件夹
files = os.listdir(path)  # 获取文件夹下所有文件名
df1 = pd.read_excel(path + '/' + files[0], encoding='gbk')  # 读取首个excel文件，保存到df1中

for file in files[1:]:
    df2 = pd.read_excel(path + '/' + file, encoding='gbk')  # 打开excel文件，注意编码问题，保存到df2中
    df1 = pd.concat([df1, df2], axis=0, ignore_index=True)

citycode = df1  # 不同城市，需要更新此表作为输入的adcode_citycode
citycode2 = citycode['adcode'].astype(str)
arr = citycode2.values.tolist()

###############下面模块为核心模块，实现输入地理检索关键字，自动化抓取兴趣点地理信息功能############
# 中心经纬度接口网址为"https://restapi.amap.com/v3/place/text?keywords=美食或其他场景关键字&city=420202&output=JSON&offset=20&key=d5c989d607e93436384de956b87708a0&extensions=all&page="
keywords = input("请输入兴趣点关键字（比如医院、美食、超市）：")
wangzhi1 = "https://restapi.amap.com/v3/place/text?keywords=" + keywords + "&city="  # 不同场景需要更新场景标识，比如美食、商场、居民区
wangzhi2 = "&output=JSON&offset=20&key=d5c989d607e93436384de956b87708a0&extensions=all&page="
# 检索AOI的URL
# aoiUrl="https://ditu.amap.com/detail/get/detail?id=" 老接口已经失效！！！！
aoiUrl = "https://www.amap.com/detail/get/detail?id="
# 用于储存POI数据
x = []
# 用于储存AOI数据
y = []
# 计数
num = 0
# 逐页POI检索，注意API限制
for i in range(0, len(arr)):
    # 当前行政区
    city = arr[i]
    # 因为官方对API检索进行了45页限制，所以只要检索到45页即可
    for page in range(1, 51):
        # 若该下级行政区的POI数量达到了限制，则警告使用者，之后考虑进行POI类型切分
        if page == 50:
            print("警告！！POI检索可能受到限制！！")
        # 构造URL
        thisUrl1 = wangzhi1 + city + wangzhi2 + str(page)
        # 获取POI数据
        data1 = requests.get(thisUrl1)
        # 转为JSON格式
        s = data1.json()
        # 解析JSON
        aa = s["pois"]
        # 若解析的JSON为空，即当前行政区的数据不够45页（即没有达到限制），返回
        if len(aa) == 0:
            break
        # 对每条POI进行存储
        for k in range(0, len(aa)):
            s1 = aa[k]["name"]
            s2 = aa[k]["type"]
            s3 = aa[k]["address"]
            s4 = aa[k]["cityname"]
            s5 = aa[k]["adname"]
            s6 = aa[k]["location"].split(",")
            s7 = aa[k]["id"]
            x.append([s1, s2, s3, s4, s5, float(s6[0]), float(s6[1]), s7])
            num += 1
            print("爬取了 " + str(num) + " 条POI数据")
c1 = pd.DataFrame(x)
c1.rename(columns={0: "name", 1: "type", 2: "address", 3: "cityname", 4: "adname", 5: "高德lon", 6: "高德lat", 7: "id"},
          inplace=True)


###############下面模块实现将高德系统经纬转换 为 常我们常用的谷歌WG84系统地理经纬度################
def GCJ2WGS(lon, lat):
    lon = float(lon)
    lat = float(lat)
    a = 6378245.0  # 克拉索夫斯基椭球参数长半轴a
    ee = 0.00669342162296594323  # 克拉索夫斯基椭球参数第一偏心率平方
    PI = 3.14159265358979324  # 圆周率
    # 以下为转换公式
    x = lon - 105.0
    y = lat - 35.0
    # 经度
    dLon = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x));
    dLon += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLon += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0;
    dLon += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0;
    # 纬度
    dLat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x));
    dLat += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLat += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0;
    dLat += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0;
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI);
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI);
    wgsLon = lon - dLon
    wgsLat = lat - dLat
    return (wgsLon, wgsLat)


tuple_wgs = c1.apply(lambda x: GCJ2WGS(x["高德lon"], x["高德lat"]), axis=1)
b = []
b = pd.DataFrame(b)
for i in range(len(c1)):
    b[i] = tuple_wgs[i]
b2 = b.T
b2.rename(columns={0: "谷歌Lon", 1: "谷歌Lat"}, inplace=True)
d = pd.concat([c1, b2], axis=1)
d.drop_duplicates(subset='id',inplace=True)
d.to_csv("D:/爬取" + keywords + "兴趣点poi地理位置坐标表.csv", encoding='gbk', index=False)

#############下面模块实现将《兴趣点poi地理位置坐标表》转换为《兴趣点poi地理位置谷歌地图文件》#############
import simplekml

d['address'] = d['address'].map(lambda x: str(x))  # 将地址列中不规范的[]内容转换为字符串便于下面进行description字符串连接
kml = simplekml.Kml()
d.apply(lambda row: kml.newpoint(name=row[0],
                                 description=row[1] + "," + row[2] + "," + row[3] + "," + row[4],
                                 coords=[(row[8], row[9])]), axis=1)

kml.save("D:/爬取" + keywords + "兴趣点poi地理位置谷歌地图文件.kml")
num_result=str(d['id'].count())
print("程序运行结束，共爬取到"+num_result+"条有效信息" )
# In[ ]:




