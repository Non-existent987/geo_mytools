#!/usr/bin/env python
# coding: utf-8
# '''

# # lin_one_lise = list(map(LineString, zip(lin_one.coords[:-1], lin_one.coords[1:])))

# # \\xa0 是不间断空白符 &nbsp;
# # 我们通常所用的空格是 \\x20 ，是在标准ASCII可见字符 0x20~0x7e 范围内。
# # 而 \\xa0 属于 latin1 （ISO/IEC_8859-1）中的扩展字符集字符，代表空白符nbsp(non-breaking space)。
# # latin1 字符集向下兼容 ASCII （ 0x20~0x7e ）。通常我们见到的字符多数是 latin1 的，比如在 MySQL 数据库中。
# # 有如下信息：

# # 'T-shirt\\xa0\\xa0短袖圆领衫,体恤衫\\xa0,', 'V-neck\\xa0\xa0V型领\xa0sleeve\xa0\xa0袖子\xa0,',
# # 1
# # 我们如何将其中的\\xz0去掉呢，试了re模块的sub方法，发现没有作用，于是又开始查阅相关资料，终于解决了该问题。方法如下：

# # >>> inputstring = u'\n                      Door:\xa0Novum          \t      '
# # >>> move = dict.fromkeys((ord(c) for c in u"\xa0\n\t"))
# # >>> output = inputstring.translate(move)
# # >>> output
# # '                      Door:Novum                '
# # 1
# # 2
# # 3
# # 4
# # 5
# # 另外还有一种更简单的方法，利用split方法：

# # >>> s
# # 'T-shirt\xa0\xa0短袖圆领衫,体恤衫\xa0'
# # >>> out = "".join(s.split())
# # >>> out
# # 'T-shirt短袖圆领衫,体恤衫'
# # ————————————————
# # 版权声明：本文为CSDN博主「wangbowj123」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# # 原文链接：https://blog.csdn.net/wangbowj123/article/details/78061618

# # '''

def help(document=''):
    if document == '包含' or document == '':
        print(r"gongcan_use = gongcan_use.loc[~gongcan_use['小区中文名'].str.contains('W-')]")
        print('\n')
    if document == '质心' or document == '':
        print(r"kongd_valid[['lon','lat']] = kongd_valid.apply(lambda x:pd.Series(x['geometry'].centroid.coords[:][0]),axis=1)")
        print('\n')
    if (document in '替换') or document == '':
        print(r"替换掉空格符号：：data['lon'] = data['lon'].replace(r'\s+','',regex=True)")
        
        print(r"data_site = data_site.replace(u'\xa0', u'', regex=True)")
        print(r"替换df中的特殊符号::data = data.replace(regex=[r'\''],value='')")
        print(r"替换标题中的特殊符号::data.columns = [i.replace('\'','') for i in list(data.columns)]")
        print(r"将priority列中的yes, no替换为布尔值True, False::df['priority'] = df['priority'].map({'yes': True, 'no': False})")
        print(r"将animal列中的snake替换为python::df['animal'] = df['animal'].replace('snake', 'python')")
        print(r"凡是数据1，4，全部替换成np.nan::data.replace([1, 4], np.nan)")
        print('\n')
    
    if (document in 'groupby') or document == '':
        print(r"分组后保留最大的某个列的一行，排序，降序::data_text.groupby(by = 'id').apply(lambda x:x.nlargest(1,'数量'))")
        print('\n')
    if (document in '行列转换行转列列转行') or document == '':
        print(r"data_B的行少")
        print(r"data_B = data_A.groupby('名字').first().reset_index().drop('心情',axis=1).merge(data_A.groupby(by = '名字').apply(lambda g:g['心情'].str.cat(sep='/')).rename('心情').reset_index(),on='名字').reindex(columns=list(data_A.columns))")
        print(r"data_A = data_B.drop('心情', axis=1).join(data_B['心情'].str.split('/', expand=True).stack().reset_index(level=1, drop=True).rename('心情')).reindex(columns=list(data_B.columns))")
        print('\n')
    if (document in 'sheet表合并') or document == '':
        print(r'''file_name_list = file_name_paths('d:/表格存放')
writer = pd.ExcelWriter('d:/合并后表格2.xlsx')#创建一个表
for file_name in file_name_list: 
    data_temp = pd.read_excel(file_name) #循环读取每个表格
    data_temp.to_excel(writer,os.path.splitext(os.path.basename(file_name))[0],index=False) #将每个表分别放到以名称命名的sheet中
writer.save() #保存d:/合并后表格2.xlsx
file_name_list = file_name_paths('d:/表格存放')
 

#定一个一个空的df，用来存放所有的表格
summary_table = pd.DataFrame()
 
for file_name in file_name_list: 
    data_temp = pd.read_excel(file_name) #循环读取每个表格
    summary_table = summary_table.append(data_temp) #添加到上面的空的df中
 
summary_table.to_excel('d:/合并后表格.xlsx',index=False) #导出
''')
    
    if (document in '字典转dfdataframe') or document == '':
        print(r"dict_df_n = pd.DataFrame(pd.Series(MyThread.ico_dict),columns=['列'])")
        print(r"dict_df_n = dict_df_n.reset_index().rename(columns={'index':'分类'})")       
        print('\n')
    if (document in '列分类按照列表分裂') or document == '':
        print(r"字典每条为一行，值分割成列")
        print(r"pd.DataFrame(data.values(),index=data.keys()).rename(columns={0:'11',1:'11',2:'22'})")
        print(r"pd.DataFrame(gongcan_res['小区CGI(*)'].str.split('-',expand=True)[2])#筛选，分裂，cgi转enodeb")
        print(r"gongcan_res['enodeb']=gongcan_res['小区CGI(*)'].str.split('-',expand=True)[2]")
        print('\n')
    if (document in '分段分层划分') or document == '':
        print(r"df['colour'] = pd.cut(df[fgl],bins=[-0.1, 0.7, 0.936, 1.1],labels =['red', 'yellow', 'green'] )")
        print('\n')
    if (document in '类型格式') or document == '':
        print(r"data_geo_use['栅格大小'] = data_geo_use['栅格大小'].astype('str')")
        print(r"df['test'] = pd.to_numeric(df.audit_id[:, 0], errors='coerce').fillna(0)")
        print('\n')
    if (document in '有效图形交叉空') or document == '':
        print(r"is_empty::对于一个空的几何图形，该值就为True")
        print(r"is_simple::如果几何体自身不交叉，该值就为True(仅对线串--LineStrings和线环--LineRings有意义)")
        print(r"is_valid::如果几何体是有效的，该值就为True")
        print('\n')

    if (document in 'id编号递增序号') or document == '':
        print(r"data_z['id'] = [ '5Gkd_21_{}'.format(str('%05d' %name)) for name in data_z.index+1]")
        print('\n')
    if (document in 'interiors内圈去掉一层列表') or document == '':
        print(r"from itertools import chain")
        print(r"list(chain.from_iterable(interior.coords[:-1] for interior in aa.interiors))")
        print(r"[interior.coords[:-1] for interior in aa.interiors]")
        print('\n')
    if (document in '字符转列表') or document == '':
        print(r"eval('[1,2]')")
    if (document in '') or document == '':
        print(r"")
        print('\n')
    if (document in '') or document == '':
        print(r"")
        print('\n')
    if (document in '') or document == '':
        print(r"") 
        print('\n')