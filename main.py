import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui2 import Ui_MainWindow
from currency_converter import CurrencyConverter
import sqlite3
conn = sqlite3.connect('mylist.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS CURRENCY_COURSE ")
sql ='''CREATE TABLE CURRENCY_COURSE(
   COURSE BLOB
)'''
cursor.execute(sql)
print("Table created successfully........")
conn.commit()
conn.close()

class CurrencyConv(QtWidgets.QMainWindow):
    def __init__(self):
        super(CurrencyConv, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('Конвертер валют')
        self.ui.in_cur.setPlaceholderText('Из валюты:')
        self.ui.in_am.setPlaceholderText('У меня есть:')
        self.ui.out_cur.setPlaceholderText('В валюту:')
        self.ui.out_am.setPlaceholderText('Я получу:')
        self.ui.pushButton.clicked.connect(self.converter)
        self.ui.add_db.clicked.connect(self.save_it)

    def converter(self):
        c = CurrencyConverter()
        input_amount = int(self.ui.in_am.text())
        output_amount = round(c.convert(input_amount, '%s' % (self.ui.in_cur.text()), '%s' % (self.ui.out_cur.text())), 2)
        self.ui.out_am.setText(str(output_amount))
    def save_it(self):
        course=int(self.ui.in_am.text())/round(CurrencyConverter().convert(int(self.ui.in_am.text()), '%s' % (self.ui.in_cur.text()), '%s' % (self.ui.out_cur.text())), 2)
        conn = sqlite3.connect('mylist.db')
        curs = conn.cursor()
        course=str(course)
        item=self.ui.out_cur.text()+"="+str(course)+self.ui.in_cur.text()
        curs.execute("INSERT INTO CURRENCY_COURSE VALUES (:item)",
                     {
                         'item':item
                     }

                     )
        conn.commit()
        conn.close()
        msg=QMessageBox()
        msg.setWindowTitle("Сохранено в базу данных")
        msg.setText("Курс валюты был сохранен")
        x=msg.exec_()
app = QtWidgets.QApplication([])
application = CurrencyConv()
application.show()

sys.exit(app.exec())