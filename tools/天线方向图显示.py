# # # import numpy as np
# # # import matplotlib.pyplot as plt

# # # # theta = np.arange(0, 2*np.pi, 0.02)
# # # # r=np.cos(theta)
# # # plt.subplot(111,polar=True)
# # # # plt.plot(theta, np.abs(np.cos(theta)))
# # # # plt.plot(theta, np.abs(np.sin(0.5*np.pi*np.cos(theta))), lw=2)

# # # # plt.subplot(122,polar=True)
# # # # plt.plot(theta, np.abs(np.sin(0.6*np.pi*np.cos(theta))), '--', lw=2)
# # # # plt.plot(theta, np.abs(np.sin(0.51*np.pi*np.cos(theta))), lw=2)
# # # # plt.rgrids(np.arange(0.5,2,0.5),angle=45)
# # # # plt.thetagrids([0,45,90])
# # # plt.show()
# # import numpy as np
# # import matplotlib.pyplot as plt
 
# # # 极坐标下需要的数据有极径和角度
# # r = np.arange(1,50,1)  # 极径
# # theta = [i for i in range(49)]  #角度
 
# # # 指定画图坐标为极坐标,projection='polar'
# # ax = plt.subplot(111, projection='polar')
# # ax.plot(theta,r,linewidth=3,color='r')
 
# # # 加网格
# # ax.grid(True)
 
# # # 显示图
# # plt.show()


# import numpy as np
# from matplotlib import pyplot as plt
# fig=plt.figure(figsize=(10,5))
# ax=fig.add_subplot(1,1,1,polar=True) #设置一个坐标轴为极坐标体系

# jingke={"推进":100,"战绩（KDA）":30,"生存":90,"团战":60,"发育":60,"输出":20} #创建英雄数据
# y=np.array([i for i in jingke.values()]).astype(int) #提取英雄的信息

# label=np.array([j for j in jingke.keys()]) #提取键作为标签

# x = np.linspace(0, 2*np.pi, 6, endpoint=False) #data1里有几个数据，就把整圆360°分成几份
# x1 = np.concatenate((x, [x[0]])) #将x的第一个值添加到原来的x组成第一个和最后一个元素一致的新列表，以实现x闭合
# y1 = np.concatenate((y, [y[0]])) #将y的第一个值添加到原来的y组成第一个和最后一个元素一致的新列表，以实现y闭合

# #绘制极坐标
# ax.set_thetagrids(angles*180/np.pi, label, fontproperties="Microsoft Yahei") #设置网格标签
# ax.plot(x1,y1,"o-")
# ax.set_theta_zero_location('E') #设置极坐标0°位置
# ax.set_rlim(0,100) #设置显示的极径范围
# ax.fill(x1,y1,facecolor='b', alpha=0.2) #填充颜色
# ax.set_rlabel_position(15)
# ax.set_title("荆轲",fontproperties="SimHei",fontsize=16) #设置标题
# plt.show()
import pandas as pd
mx=pd.read_csv('c:/Users/Administrator/Desktop/天线/天线/F天线.txt',encoding='gbk',sep='\t')

a = mx['Pattern'][0]

def fc(x):
    a = x['Pattern']
    b = a.split(' ')
    name_o=1
    go='第一次开始'
    use_list =[]
    use_dict =dict()
    st=0
    id_use = -1
    for nu,name in enumerate(b):
        if name =='':
            go='重新开始'
            st = 0
        if (str(name_o) =='0') and (str(name) == '360')and (go=='第一次开始'):
            st=1
        elif (str(name_o) =='0') and (str(name) == '360')and (go=='重新开始'):
            st=1
            id_use=-1
        if st==1:
            if nu%2==1:
                use_list.append(str(id_use)+'_'+str(name))
                id_use = id_use +1
        name_o = name
    return use_list

mx['fw_list']=mx.apply(fc,axis=1)

linshi = pd.DataFrame(mx['fw_list'][0])[0].str.split('_',expand=True)

linshi.columns=['角度','电平']

linshi2 = linshi.T

import matplotlib.pyplot as plt

data_use = linshi.iloc[1:361]

jiaodu = list(data_use['角度'])

dianping = list(data_use['电平'])
jiaodu2 = [int(x)/180.0*3.141593 for x in jiaodu]
import numpy as np
from matplotlib import pyplot as plt
fig=plt.figure(figsize=(10,13))
ax=fig.add_subplot(111,polar=True) #设置一个坐标轴为极坐标体系
ax.set_thetagrids(np.arange(0.0, 360.0, 10.0)) # 用于设置极坐标角度网格线显示

# jingke={"推进":100,"战绩（KDA）":30,"生存":90,"团战":60,"发育":60,"输出":20} #创建英雄数据
jiao=[100,  30,  90,  60,  60,  20,30]#提取英雄的信息
label=['推进', '战绩（KDA）', '生存', '团战', '发育', '输出','sad'] #提取键作为标签

x = np.linspace(0, 2*np.pi, 7, endpoint=False) #data1里有几个数据，就把整圆360°分成几份

# x1 = np.concatenate((x, [x[0]])) #将x的第一个值添加到原来的x组成第一个和最后一个元素一致的新列表，以实现x闭合
# y1 = np.concatenate((y, [y[0]])) #将y的第一个值添加到原来的y组成第一个和最后一个元素一致的新列表，以实现y闭合

#绘制极坐标
# ax.set_thetagrids(angles*180/np.pi, label, fontproperties="Microsoft Yahei") #设置网格标签
ax.plot(jiaodu2,[x%2 for x in jiaodu2],"o")
ax.set_theta_zero_location('N') #设置极坐标0°位置
ax.set_theta_direction(-1) # 用于设置极坐标的正方向，参数为-1时为顺时针方向；反之。
# ax.set_rlim(0,10) #设置显示的极径范围
# ax.fill(x1,y1,facecolor='b', alpha=0.2) #填充颜色
# ax.set_rlabel_position(15)
# ax.set_title("荆轲",fontproperties="SimHei",fontsize=16) #设置标题
plt.show()