# import tkinter as tk      #导入tkinter模块
##import tkinter.scrolledtext as tst
from tkinter import filedialog, dialog,colorchooser,Button,Frame,Tk,END,StringVar,ttk,Label,messagebox
from pandas import read_csv,DataFrame
from geopandas import GeoDataFrame
from shapely.geometry import Point
from numpy import sin,radians,cos,arcsin,sqrt
##import ctypes

class Application(Frame):   #定义GUI类，派生于Frame类
    def __init__(self,master=None):    
        Frame.__init__(self,master)    #调用父类的构造函数
        self.grid()    #调用组件的pack方法，调整其显示位置和大小
        self.createWidgets()   #对象方法声明
        self.data_x = DataFrame()
        self.data_y = DataFrame()
        self.lon_x = ''
        self.lat_x = ''
        self.lon_y = ''
        self.lat_y = ''
        self.data_x_lie =[]
        self.data_y_lie =[]
    #框架1 -----------------------------DLL load fa----以下是窗体-----------------------------------------------
    def createWidgets(self):    #对象方法定义
        #text文本框
        # self.textEdit=tst.ScrolledText(self,width=80,height=20)   #创建text组件
        # self.textEdit.grid(row=0,column=0,rowspan=6)
        #打开按钮
        self.btnOpen=Button(self,text="表A",width=12,height=1,command=self.funcOpen_x)  #创建打开按钮
        self.btnOpen.grid(row=1,column=1)
        self.btnOpen=Button(self,text="表B",width=12,height=1,command=self.funcOpen_y)  #创建打开按钮
        self.btnOpen.grid(row=1,column=5)
        #下拉菜单
        self.label_lon_x = Label(self, text="A经度").grid(row=2,sticky='w',padx=10,pady=5)
        self.lon_x = StringVar()
        self.lon_box_x = ttk.Combobox(self, width=12, textvariable=self.lon_x)
        self.lon_box_x["values"]=("1","2","3","4") 
        self.lon_box_x.current(0)
        self.lon_box_x.grid(row=2,column=1)  
        # self.lon_box_x.bind("<<ComboboxSelected>>",self.funcOpen)  #绑定事件,(下拉列表框被选中时，绑定go()函数) 
        self.label_lat_x = Label(self, text="A纬度").grid(row=3,sticky='w',padx=10,pady=5)
        self.lat_x = StringVar()
        self.lat_box_x = ttk.Combobox(self, width=12, textvariable=self.lat_x)
        self.lat_box_x["values"]=("11","12","13","14") 
        self.lat_box_x.current(0)
        self.lat_box_x.grid(row=3,column=1) 

        self.label_lon_y = Label(self, text="B经度").grid(row=2,column=4,sticky='w',padx=10,pady=5)
        self.lon_y = StringVar()
        self.lon_box_y = ttk.Combobox(self, width=12, textvariable=self.lon_y)
        self.lon_box_y["values"]=("1","2","3","4") 
        self.lon_box_y.current(0)
        self.lon_box_y.grid(row=2,column=5)  
        # self.lon_box_x.bind("<<ComboboxSelected>>",self.funcOpen)  #绑定事件,(下拉列表框被选中时，绑定go()函数)  
        self.label_lat_y = Label(self, text="B纬度").grid(row=3,column=4,sticky='w',padx=10,pady=5)
        self.lat_y = StringVar()
        self.lat_box_y = ttk.Combobox(self, width=12, textvariable=self.lat_y)
        self.lat_box_y["values"]=("11","12","13","14") 
        self.lat_box_y.current(0)
        self.lat_box_y.grid(row=3,column=5) 

        #保存按钮
        self.btnSave=Button(self,width=6,height=2,text="GO！",command=self.go_run)  #创建保存按钮
        self.btnSave.grid(row=2,column=2,rowspan=2,padx=10,pady=5)
        #颜色按钮
        self.btnColor=Button(self,width=12,height=1,text="颜色",command=self.funcColor)  #创建颜色选择按钮
        self.btnColor.grid(row=5,column=1)
        #退出按钮
        self.btnQuit=Button(self,width=12,height=1,text="退出",command=self.funcQuit)  #创建退出按钮
        self.btnQuit.grid(row=5,column=5)
    #框架1 ---------------------------------以上是窗体-----------------------------------------------
    #框架2 ---------------------------------以下是函数-----------------------------------------------
    def add_points(self,df,
            lon='lon',
            lat='lat',
            pnt_col='geometry'
            ):
        '''add_points(df,lon='lon',lat='lat',pnt_col='geometry'):'''
        df = df.copy()
        df[pnt_col] = [Point(x) for x in zip(df[lon], df[lat])]
        df = GeoDataFrame(df, crs={"init": "epsg:4326"}, geometry='geometry') 
        return df
    def distancea_df(self,df,
                        lon_1, 
                        lat_1, 
                        lon_2, 
                        lat_2,
                        columns_name='距离'
                        ):
        lon1, lat1, lon2, lat2 = map(radians, [df[lon_1], df[lat_1], df[lon_2], df[lat_2]])
        a = sin((lat2 - lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2 - lon1)/2)**2
        df[columns_name] = 2*arcsin(sqrt(a))*6371*1000
        return df
    def min_one(self,data_x,data_y,lon_x='经度',lat_x='纬度',lon_y='经度y',lat_y='纬度y'):
        '''
        求距离A数据(df格式)中每一条数据最近的一个数据（来自B数据）
        其中两组数据的经纬度不要一样
        示例：res = min_one(data,zhan,'经度','纬度','衔接经度','衔接纬度')

        data_x:需要计算距离的A数据（df格式）
        data_y:计算距离所需要使用的B数据（df格式）
        lon_x：lat_x：data_x表中的经纬度列名
        lon_y：lat_y：data_y表中的经纬度列名
        '''
                #生成点gdf
        data_x_p = self.add_points(data_x,lon_x,lat_x)
        data_y_p = self.add_points(data_y,lon_y,lat_y)

        #匹配距离最近的数据
        data_y_p_index = data_y_p.sindex
        data_x_p['minimum_index'] = data_x_p['geometry'].apply(lambda x: list(data_y_p_index.nearest(x.bounds,num_results=1))[0])
        data_x_p = data_x_p.drop(columns='geometry')
        data_y_p = data_y_p.drop(columns='geometry')
        res = data_x_p.merge(data_y_p,how='left',left_on='minimum_index',right_index = True)
        #添加距离
        res1 = self.distancea_df(res,lon_x,lat_x,lon_y,lat_y)
        return res1

    def funcOpen_x(self):   #定义事件处理函数，打开文件
        # self.textEdit.delete(1.0,END)    #清空text组件内的内容
        fname=filedialog.askopenfilename(filetypes=[("csv",".csv")])
        self.data_x = read_csv(fname,encoding='gbk')
        self.lon_box_x["values"]=list(self.data_x.columns)
        self.lat_box_x["values"]=list(self.data_x.columns)
    def funcOpen_y(self):   #定义事件处理函数，打开文件
        fname=filedialog.askopenfilename(filetypes=[("csv",".csv")])
        self.data_y = read_csv(fname,encoding='gbk')
        self.lon_box_y["values"]=list(self.data_y.columns)
        self.lat_box_y["values"]=list(self.data_y.columns)

    def go_run(self):

        self.lon_x=self.lon_box_x.get()
        self.lat_x=self.lat_box_x.get()
        self.lon_y=self.lon_box_y.get()
        self.lat_y=self.lat_box_y.get()
        print(self.lon_x,self.lat_x,self.lon_y,self.lat_y)
        print(self.data_x.shape,self.data_y.shape)
        res = self.min_one(self.data_x,self.data_y,lon_x=self.lon_x,lat_x=self.lat_x,lon_y=self.lon_y,lat_y=self.lat_y)
        res.to_csv('结果.csv',encoding='gbk',index=False)
        print('已完成，结果在程序根目录下面')
        messagebox.showinfo('已完成','结果在程序根目录下面')

    def funcSave(self):   #定义事件处理函数，保存文件
        str1=self.textEdit.get(1.0,END)
        fname=filedialog.asksaveasfilename(filetypes=[("Python源文件",".py")])
        with open(fname,'w',encoding="utf-8") as f1:  #打开文件
            f1.write(str1)
 
    def funcColor(self):   #定义事件处理函数，设置颜色
        t,c=colorchooser.askcolor(title="设置颜色")
        self.config(bg=c)
    def funcQuit(self):   #定义事件处理函数，退出程序
        root.destroy()
    #框架2 ---------------------------------以上是函数-----------------------------------------------
root=Tk()   #创建一个Tk跟窗口组件root
root.title("min_one")
root.iconbitmap('ico/tmp.ico')
app=Application(master=root)   #创建Application的对象实例
app.mainloop()   #调用组件mainloop方法，进入事件循环
