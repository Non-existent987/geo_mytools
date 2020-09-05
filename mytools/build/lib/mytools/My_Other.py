import os,sys,pickle
import tkinter as tk
from tkinter import filedialog
import numpy as np
class MyTools_other(object):
    # def __init__(self):
        # print('other类的初始化执行了',os.getcwd())
    '''git——改名字'''

    def str_is_chinese(self,check_str):
        """
        判断字符串中是否包含中文
        :param check_str: {str} 需要检测的字符串
        :return: {bool} 包含返回True， 不包含返回False
        """
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False
    def pickle_save(self,a,path='C:/Users/Administrator/Desktop/aaa.data'):
        f = open(path, 'wb')
        pickle.dump(a, f)
        f.close()
    def pickle_read(self,path='C:/Users/Administrator/Desktop/aaa.data'):
        f = open(path, 'rb')
        b = pickle.load(f)
        return b
    def df_sort(self,
                df,
                columns=['',''],
                sort_columns='',
                weishu=2,
                ascending=False
                ):
        '''
        将小数列转换成百分比，保留最后的总计列不变
        df=DataFrame()
        columns=是一个列表，放所有要转换的小区的列
        sort_columns=字符，放需要排序的列名
        ascending=布尔类型，真升序，假的降序

        '''
        df_head = df.iloc[:-1]
        df_head_sort = df_head.sort_values(sort_columns,ascending=ascending)
        df_head_foot = df_head_sort.append(df.iloc[-1])
        for xx in columns:
            df_head_foot[xx] = df_head_foot[xx].apply(lambda x: format(x, '.{}%'.format(weishu)) if (str(x) !='nan' or x =='') else np.nan)#转成百分比
        return df_head_foot
    def df_yield(self,
                    df,
                    number=1000,
                    print_info=True
                    ):
        y = number
        x = 0
        while x<df.shape[0]:
            df_t = df.iloc[x:y,]
            yield df_t
            if print_info:
                print('共计{zong}行,完成{cishu}到{cishu2}行'.format(cishu=x,cishu2 = y,zong=df.shape[0]))
            x = y 
            y = y + number

    def pip(self,name_str='bao'):
        import pyperclip
        pip1='pip install scrapy -i https://pypi.tuna.tsinghua.edu.cn/simple '+ name_str
        return pyperclip.copy(pip1)
    def str_copy(self,name_str='bao'):
        import pyperclip
        return pyperclip.copy(name_str)        
    def file_to_mysql(self,
                        path=r'D:/uup/',
                        table_name='mro_it',
                        sep='  ',
                        encoding='utf8'
                        ):
        '''例子：file_to_mysql(r'D:/uup/','mro_it ')
            默认使用分割负sep = '  ',编码方式encoding = 'utf8'
            可选',' gbk
        '''
        files = self.file_name_paths(path=path)
        tablename = table_name
        tada_res = '-- ---------\n'
        print('''truncate table mro_it;truncate table mro_it_yy_dt;''')
        for i in files:
            e=i.replace( '\\','/')
            data = r'''
    Load Data LOCAL InFile  
    '''+"'"+e+"'"+r'''
    Into Table mro.`'''+tablename+r'''` 
    character set '''+encoding+r''' Fields Terminated By'''+"'"+sep+"'"+r''' -- 或者 ","
    optionally enclosed by '"' 
    Enclosed By '"' 
    Escaped By '"' 
    Lines Terminated By '\n' 
    IGNORE 1 LINES;'''
            tada_res = tada_res+'\n'+data

            print(data+'\n\n\n')
        
    # def file_name_paths(self,path=r'D:\UP'):
    #         path_collection=[]
    #         for dirpath,dirnames,filenames in os.walk(path):
    #                 for file in filenames:
    #                         fullpath=os.path.join(dirpath,file)
    #                         path_collection.append(fullpath)
    #         return path_collection
    def str_inlist(self,list_x , str='ca'):
        list_a = []
        for x in enumerate(list_x):
            if str in x[1]:
                list_a.append(x[1])
        return list_a

    def file_name(self,path=r'D:\UP'):
            path_collection=[]
            for dirpath,dirnames,filenames in os.walk(path):
                    for file in filenames:
                            fullpath=os.path.join(file)
                            path_collection.append(fullpath)
            return path_collection
    
    def con(self):
        from sqlalchemy import create_engine
        yconnect = create_engine('mysql+pymysql://root:root@localhost:3306/mro?charset=utf8')
        return yconnect

    def to_sql(self,
                df,
                name='name', 
                schema=None, 
                if_exists='fail', 
                index=True, 
                index_label=None, 
                chunksize=None
                ):
        dtype = self.to_sql_dtype(df)
        con=self.con()
        df.to_sql(name=name, con=con, schema=schema, if_exists=if_exists, index=index, index_label=index_label, chunksize=chunksize, dtype=dtype)


    def to_sql_dtype(self,df):
        from sqlalchemy.types import NVARCHAR, Float, Integer
        dtypedict = {}
        for i, j in zip(df.columns, df.dtypes):
            if "object" in str(j):
                dtypedict.update({i: NVARCHAR(length=255)})
            if "float" in str(j):
                dtypedict.update({i: Float(precision=2, asdecimal=True)})
            if "int" in str(j):
                dtypedict.update({i: Integer()})
        return dtypedict

    def get_file_one(self):
        import easygui
        path = easygui.fileopenbox()
        return path
    
    def get_file_one_tk(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        return file_path

    def get_file_more_tk(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilenames()
        return file_path

    def get_file_name(self,path=r'D:/UP/'):
        pant_split=path
        path_collection=[]
        for dirpath,dirnames,filenames in os.walk(path):
                for file in filenames:
                        fullpath=os.path.join(dirpath,file).split(path)[1]
                        path_collection.append(fullpath)
        return path_collection
    def file_name_paths(self,
                        path=r'D:\UP',
                        find=None ,
                        case_sensitive=False):
        path_collection=[]
        for dirpath,dirnames,filenames in os.walk(path):
                for file in filenames:
                        fullpath=os.path.join(dirpath,file)
                        if '~$' not in file.upper():
                            if case_sensitive:
                                if find:
                                    if find in file:
                                        path_collection.append(fullpath)
                                else:
                                    path_collection.append(fullpath)
                            else:
                                if find:
                                    if find.upper() in file.upper():
                                        path_collection.append(fullpath)
                                else:
                                    path_collection.append(fullpath)
                        else:
                            pass
        return path_collection
