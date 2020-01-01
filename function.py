# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'function.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        Dialog.setMinimumSize(QtCore.QSize(800, 600))
        Dialog.setMaximumSize(QtCore.QSize(800, 600))
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(30, 50, 130, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(180, 50, 150, 32))
        self.comboBox.setStyleSheet("min-height:30px")
        self.comboBox.setIconSize(QtCore.QSize(30, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(350, 50, 300, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(30, 100, 620, 460))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 130, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(180, 20, 150, 30))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(350, 20, 150, 30))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(670, 50, 100, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(670, 100, 100, 30))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "风险函数管理"))
        self.comboBox.setItemText(0, _translate("Dialog", "低危险"))
        self.comboBox.setItemText(1, _translate("Dialog", "中等危险"))
        self.comboBox.setItemText(2, _translate("Dialog", "危险"))
        self.comboBox.setItemText(3, _translate("Dialog", "很危险（或稍小，取决于实现）"))
        self.comboBox.setItemText(4, _translate("Dialog", "很危险"))
        self.comboBox.setItemText(5, _translate("Dialog", "最危险"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "函数名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "函数危险等级"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "建议解决方法"))
        self.label.setText(_translate("Dialog", "函数名"))
        self.label_2.setText(_translate("Dialog", "函数危险等级"))
        self.label_3.setText(_translate("Dialog", "建议解决方法"))
        self.pushButton.setText(_translate("Dialog", "添加"))
        self.pushButton_2.setText(_translate("Dialog", "删除"))


