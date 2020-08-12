import pandas as pd

data = pd.read_excel('内参表-规划库-20200610.xlsx')

df=data.copy() #你的df
writer = pd.ExcelWriter("输出.xlsx", engine='xlsxwriter')#输出地方
df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False,index=False)
workbook  = writer.book
worksheet = writer.sheets['Sheet1']
# Add a header format.
header_format = workbook.add_format({
    'bold': True,# 字体加粗
    'text_wrap': True,# 是否自动换行
    'valign': 'top',#对其方式
    'fg_color': '#D7E4BC',# 单元格背景颜色
    'border': 1})# 单元格边框宽度
# 定义标题
for col_num, value in enumerate(df.columns.values):
    worksheet.write(0, col_num , value, header_format)
# 导出关闭.
writer.save()
writer.close() 