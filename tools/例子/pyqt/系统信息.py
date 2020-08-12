import psutil
import time

# cpu_res = psutil.cpu_percent()
# print(cpu_res)

# 每一秒获取获取cpu的占有率 --->持久化保存
# 如何将时间和对应的cpu占有率去匹配

while True:
    # 获取当前时间和cpu的占有率
    t = time.localtime()
    cpu_time = '%d:%d:%d' %(t.tm_hour,t.tm_min,t.tm_sec)
    cpu_res = psutil.cpu_percent()
    print(cpu_res)

    # 保存在文件中
    with open('cpu.txt','a+') as f:
        f.write('%s %s \n' %(cpu_time,cpu_res))
    time.sleep(1)
