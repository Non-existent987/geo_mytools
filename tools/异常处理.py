# try:
#     a = input("输入一个数：")
#     #判断用户输入的是否为数字
#     if(not a.isdigit()):
#         raise ValueError("a 必须是数字")
# except ValueError as e:
#     print("引发异常：",repr(e))


import sys

try:
    a = 1
    b = 'sd'
    a == b+a
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError as vv:
    print("ValueError.",vv)
except TypeError as tt: ##################   Exception 全能
    print("TypeError",tt)
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
else:
    print('开始执行备用代码')


try:
    print('执行主程序')
    f=2
    1==1
    print(f)
except OSError as cuo:
    print('执行报告有错误:', cuo)
    print('提醒用户错误了')
else:
    print('------------如果没有错误执行备选方案--------')
finally:
    print('无论怎样我都会执行，下面会报异常')
    raise '值错误'
