from tkinter import ttk,HORIZONTAL,Button,Frame,Label,StringVar,Tk,filedialog,messagebox,Radiobutton,IntVar,Menu,colorchooser
from pandas import DataFrame,read_csv,read_excel
from qq import img   #导入base64格式的img
import base64
from os import remove
from time import strftime,localtime
from tkinter import ttk
from tkinter import *
class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground
class AppLication(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.grid()
        self.v = IntVar()
        self.createWidgets()
        self.data = DataFrame()
        self.file_name_zong = ''
        self.folder_name = ''
        self.data_yuan = DataFrame()
        self.data_moban = DataFrame()
        #居中设置
        self.root=master
        self.screen_width = self.root.winfo_screenwidth()#获得屏幕宽度
        self.screen_height = self.root.winfo_screenheight()  #获得屏幕高度
        self.root.resizable(False, False)#让高宽都固定
        self.root.update_idletasks()#刷新GUI
        self.root.withdraw() #暂时不显示窗口来移动位置
        self.root.geometry('%dx%d+%d+%d' % (self.root.winfo_width(), self.root.winfo_height() ,(self.screen_width - self.root.winfo_width()) / 2,(self.screen_height - self.root.winfo_height()) / 2))  # center window on desktop
        self.root.deiconify()        
    def createWidgets(self):
        try:
            remove("tmp.ico")
        except:
            pass
        # ttk.Style().configure("TButton", padding=15, relief="FLAT", background="#ccc")
        # self.btn = ttk.Button(self,text="Sample")
        # self.btn.grid(row=6,column=6)

        self.Button_1 = HoverButton(self,text='打开需拆分表',width=12,activebackground='#A9A9A9',bd=2,command=self.funcOpen_chai)
        self.Button_1.grid(row=1,column=1)
        self.Button_1 = HoverButton(self,text='拆分',width=12,activebackground='#A9A9A9',command=self.go_chai,bd=2,highlightcolor='red')
        self.Button_1.grid(row=1,column=5)

        self.separator_1 = ttk.Separator(self, orient = HORIZONTAL)
        self.separator_1.grid (row = 2, column = 1, sticky = "ew",columnspan=4)

        self.Button_2 = HoverButton(self,text='选择多个数据',width=12,activebackground='#A9A9A9',bd=2,command=self.funcOpen_paths)
        self.Button_2.grid(row=3,column=1,rowspan=2)
        self.Button_2 = HoverButton(self,text='合并',width=12,activebackground='#A9A9A9',bd=2,command=self.go_he)
        self.Button_2.grid(row=3,column=5,rowspan=2)

        
        self.v.set(2)
        self.Radiobutton_1 = Radiobutton(self,text='添加表名到新增列', variable=self.v,value=1)
        self.Radiobutton_2 = Radiobutton(self,text='不添加新列', variable=self.v,value=2)
        self.Radiobutton_1.grid(row=4,column=2)
        self.Radiobutton_2.grid(row=4,column=3)


        #下拉菜单
        self.label_1 = Label(self, text="按某列字段拆分").grid(row=1,column=2,sticky='w',padx=10,pady=5)
        self.columns_1 = StringVar()
        self.box_1 = ttk.Combobox(self, width=15, textvariable=self.columns_1)
        self.box_1.grid(row=1,column=3)  
        # self.box_1["values"]=('') 
        #下拉菜单2
        self.label_3 = Label(self, text="输出文件格式").grid(row=3,column=2,sticky='w',padx=10,pady=5)
        self.columns_3 = StringVar()
        self.box_3 = ttk.Combobox(self, width=15, textvariable=self.columns_3)
        self.box_3["values"]=(["excel","csv"]) 
        self.box_3.current(0)
        self.box_3.grid(row=3,column=3)

        self.separator_2 = ttk.Separator(self, orient = HORIZONTAL)
        self.separator_2.grid (row = 5, column = 1, sticky = "ew",columnspan=4)

        self.Button_6 = HoverButton(self,text='打开待处理的表',width=12,activebackground='#A9A9A9',bd=2,command=self.yuan)
        self.Button_6.grid(row=6,column=1)
        self.Button_6_2 = HoverButton(self,text='模版',width=12,activebackground='#A9A9A9',bd=2,command=self.moban)
        self.Button_6_2.grid(row=6,column=3)#,columnspan=3
        self.Button_6_3 = HoverButton(self,text='处理',width=12,activebackground='#A9A9A9',bd=2,command=self.run_moban)
        self.Button_6_3.grid(row=6,column=5)
        self.label_t_2 = Label(self, text="按照模版取部分列").grid(row=6,column=2,sticky='w',padx=10,pady=4)

        # 创建一个菜单项，类似于导航栏，顶层菜单
        # self.menubar=Menu(self) 
        # self.fmenu2=Menu(self)
        # self.fmenu2.add_command(label='颜色',command=self.funcColor)
        # self.fmenu2.add_command(label='退出',command=self.funcColor)
        # self.menubar.add_cascade(label="菜单",menu=self.fmenu2)

    def funcOpen_paths(self):
        print('选择多个文件开始')
        self.folder_name=filedialog.askopenfilenames(filetypes=[("表格excel",[".xlsx",'.xls','.csv'])])
        print(self.folder_name)
    def dataOpen(self,fname=''):   #定义事件处理函数，打开文件
        a = fname.split('.')[-1]
        print(a)
        if a.lower() == 'csv':
            try:
                if self.is_contain_chinese(fname):
                    data_t=read_csv(open(fname,encoding='gbk'))
                else:
                    data_t=read_csv(fname,encoding='gbk')
            except:
                if self.is_contain_chinese(fname):
                    data_t=read_csv(open(fname,encoding='utf-8'))
                else:
                    data_t=read_csv(fname,encoding='utf-8')
        elif (a.lower() == 'xlsx') | (a.lower() == 'xls'):
            try:
                data_t=read_excel(fname,encoding='gbk')
            except:
                sdata_t=read_excel(fname,encoding='utf-8')
        else:
            pass
        print('读取{}文件成功'.format(fname))
        return data_t
    def funcOpen(self):   #定义事件处理函数，打开文件
        # self.textEdit.delete(1.0,END)    #清空text组件内的内容
        fname=filedialog.askopenfilename(filetypes=[("表格excel",[".xlsx",'.xls','.csv']),('EXE', '*.exe'), ('All Files', '*')])
        print(fname,1)
        if len(fname)<1:
            print(fname,'<1')
            pass
        else:
            self.file_name_zong=fname
            a = fname.split('.')[-1]
            print(a)
            if a.lower() == 'csv':
                try:
                    if self.is_contain_chinese(fname):
                        self.data=read_csv(open(fname,encoding='gbk'))
                    else:
                        self.data=read_csv(fname,encoding='gbk')
                except:
                    if self.is_contain_chinese(fname):
                        self.data=read_csv(open(fname,encoding='utf-8'))
                    else:
                        self.data=read_csv(fname,encoding='utf-8')
            elif (a.lower() == 'xlsx') | (a.lower() == 'xls'):
                try:
                    self.data=read_excel(fname,encoding='gbk')
                except:
                    self.data=read_excel(fname,encoding='utf-8')
            else:
                assert 0
            messagebox.showinfo('提示','选择数据成功,数据格式为{}'.format(a))
            print(self.data.shape)
        return fname

    def Open_f(self):   #定义事件处理函数，打开文件
        # self.textEdit.delete(1.0,END)    #清空text组件内的内容
        print('开始打开文件')
        data = DataFrame()
        print('新建了data')
        fname=filedialog.askopenfilename(filetypes=[("表格excel",[".xlsx",'.xls','.csv']),('EXE', '*.exe'), ('All Files', '*')])
        
        print(fname,1)
        if len(fname)<1:
            print(fname,'<1')
            pass
        else:
            print('开始打开')
            
            self.file_name_zong=fname
            a = fname.split('.')[-1]
            print(a)
            if a.lower() == 'csv':
                try:
                    if self.is_contain_chinese(fname):
                        data=read_csv(open(fname,encoding='gbk'))
                    else:
                        data=read_csv(fname,encoding='gbk')
                except:
                    if self.is_contain_chinese(fname):
                        data=read_csv(open(fname,encoding='utf-8'))
                    else:
                        data=read_csv(fname,encoding='utf-8')
            elif (a.lower() == 'xlsx') | (a.lower() == 'xls'):
                try:
                    data=read_excel(fname,encoding='gbk')
                except:
                    data=read_excel(fname,encoding='utf-8')
            else:
                assert 0
            messagebox.showinfo('提示','选择数据成功,数据格式为{}'.format(a))
            print(data.shape)
        return data,fname  
    def yuan(self):
        try:
            print('开始')
            self.data_yuan , name_youxiao = self.Open_f()
            print(self.data_yuan.shape,name_youxiao)
            if len(name_youxiao)<1:
                pass
            else:
                print('打开文件成功')
        except:
            messagebox.showinfo('提示','选择数据有误，请检查文件是否正常，支持csv、excel格式文件。')    
    def moban(self):
        try:
            self.data_moban , name_youxiao = self.Open_f()
            if len(name_youxiao)<1:
                pass
            else:
                print('打开文件成功')
        except:
            messagebox.showinfo('提示','选择数据有误，请检查文件是否正常，支持csv、excel格式文件。')  
    def run_moban(self):
        name_1 = self.file_name_zong.split('.')[:-1]
        if self.data_yuan.shape[0]<1:
            pass
        else:
            try:
                data_res = self.data_yuan[list(self.data_moban.columns)]
                data_res.to_excel(''.join(name_1)+'_'+'结果.xlsx',encoding='gbk',index=False)
                messagebox.showinfo('提示','处理完成，结果在和文件同目录下')
            except:
                messagebox.showinfo('提示','模版中有列名在源数据中不存在，请检查数据')  
    def funcOpen_chai(self):
        try:
            name_youxiao = self.funcOpen()
            if len(name_youxiao)<1:
                pass
            else:
                print(list(self.data.columns))
                self.box_1["values"]=list(self.data.columns)
                self.box_1.current(0)
                print('打开文件成功')
        except:
            messagebox.showinfo('提示','选择数据有误，请检查文件是否正常，支持csv、excel格式文件。')
    def go_chai(self):
        if self.data.shape[0]<1:
            pass
        else:
            name_1 = self.file_name_zong.split('.')[:-1]
            name_2 = self.file_name_zong.split('.')[-1]
            x = self.box_1.get()
            self.data[str(x)] = self.data[str(x)].fillna('__空__')
            data_chai_g = self.data.groupby(str(x))
            mu=0
            for name , data_t in data_chai_g:
                if name_2.lower() =='csv':
                    data_t.to_csv(''.join(name_1)+'_'+name+'.csv',encoding='gbk',index=False)
                else:
                    data_t.to_excel(''.join(name_1)+'_'+name+'.xlsx',encoding='gbk',index=False)
                mu = mu+1
            print('结束')
            messagebox.showinfo('提示','数据拆分完成，拆分后共计{}个文件。'.format(mu))
    def is_contain_chinese(self,check_str):
        """
        判断字符串中是否包含中文
        :param check_str: {str} 需要检测的字符串
        :return: {bool} 包含返回True， 不包含返回False
        """
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False
    def go_he(self): 
        box_3_name = self.box_3.get()
        f = self.folder_name
        data_z = DataFrame()
        ss = 0
        for name in f:
            print(name)
            try:
                data_t = self.dataOpen(name)
            except:
                messagebox.showinfo('提示','数据{}读取失败。'.format(name))
                assert 0
            if self.v.get()==1:
                data_t['新增列_表名'] = name.split('/')[-1]
                data_z = data_z.append(data_t)
            else:
                data_z = data_z.append(data_t)
            ss = ss+1
        if data_z.shape[0]<1:
            pass
        else:
            a = strftime("%Y%m%d_%H%M", localtime())
            if box_3_name  =='csv':
                data_z.to_csv('/'.join(name.split('/')[:-1])+'/数据汇总{}.csv'.format(a),encoding='gbk',index=False)
            else:
                data_z.to_excel('/'.join(name.split('/')[:-1])+'/数据汇总{}.xlsx'.format(a),encoding='gbk',index=False)
            messagebox.showinfo('提示','数据合并完成，共计合并了{}个文件。'.format(ss))
    def funcColor(self):   #定义事件处理函数，设置颜色
        t,c=colorchooser.askcolor(title="设置颜色")
        self.config(bg=c)

        


if __name__ == '__main__':
    root = Tk()
    root.title('表拆分合并工具')
    # root.resizable(0,0) #阻止Python GUI的大小调整


    tmp = open("tmp.ico","wb+")  
    tmp.write(base64.b64decode(img))#写入到临时文件中
    tmp.close()
    root.iconbitmap("tmp.ico") #设置图标
    remove("tmp.ico") 

    app=AppLication(master=root)
    # root.config(menu = app.menubar)
    app.mainloop()
    # root.config(menu = app.menubar)
    try:
        remove("tmp.ico")
    except:
        pass