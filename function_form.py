from PyQt5.QtWidgets import *

from function import Ui_Dialog

class functionForm(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(functionForm, self).__init__(parent)
        self.setupUi(self)
        self.context_show()
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)

    def add(self):
        if str(self.lineEdit).strip() == '' or str(self.lineEdit_2).strip() == '':
            QMessageBox.warning(self, "Alert", "添加函数信息未填完整")
            return
        fun_name = self.lineEdit.text()
        fun_level = self.comboBox.currentText()
        fun_solution = self.lineEdit_2.text()
        self.table_add(fun_name, fun_level, fun_solution)
        self.file_update()
        self.lineEdit.clear()
        self.lineEdit_2.clear()

    def context_show(self):
        f = open("fun.txt", "r")
        while True:
            s = f.readline()
            if s and s != '':
                self.table_add(s.split("\t")[0], s.split("\t")[1], s.split("\t")[2])
            else:
                break
        f.close()

    def table_add(self, fun_name, fun_level, fun_solution):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        newItem = QTableWidgetItem(fun_name)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, newItem)
        newItem = QTableWidgetItem(fun_level)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, newItem)
        newItem = QTableWidgetItem(fun_solution)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, newItem)

    def delete(self):
        self.tableWidget.removeRow(self.tableWidget.currentRow())
        self.file_update()

    def file_update(self):
        f = open("fun.txt", "w")
        rowPosition = self.tableWidget.rowCount()
        text = ""
        if rowPosition > 0:
            for rP in range(0, rowPosition):
                text += self.tableWidget.item(rP, 0).text() + '\t' + self.tableWidget.item(rP, 1).text() + '\t' + self.tableWidget.item(rP, 2).text()
        f.write(text)



