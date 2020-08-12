import sys
from form import Ui_Forms
from PyQt5.Qt import QWidget, QApplication,QTableWidgetItem
import psycopg2

class myform(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.btn1.clicked.connect(self.clear)
        self.btn2.clicked.connect(self.load)
        self.show()
        
    def clear(self):
        pass
    def load(self):
        conn=psycopg2.connect("dbname=test1_data user=jm password=123")
        cur=conn.cursor()
        cur.execute('select * from table1')
        rows=cur.fetchall()
        row=cur.rowcount  #取得记录个数，用于设置表格的行数
        vol=len(rows[0])  #取得字段数，用于设置表格的列数
        cur.close()
        conn.close()
        
        self.table.setRowCount(row)
        self.table.setColumnCount(vol)
        
        for i in range(row):
            for j in range(vol):
                temp_data=rows[i][j]  #临时记录，不能直接插入表格
                data=QTableWidgetItem(str(temp_data)) #转换后可插入表格
                self.table.setItem(i,j,data)
        
app=QApplication(sys.argv)
w=myform()
app.exec_()