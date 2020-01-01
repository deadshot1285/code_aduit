from PyQt5.QtWidgets import QDialog

from find import Ui_Dialog

class FindForm(QDialog, Ui_Dialog):
    def __init__(self, parent = None):
        super(FindForm, self).__init__(parent)
        self.setupUi(self)
        self.master = parent
        self.pushButton.clicked.connect(self.find_btn)
        self.pushButton_3.clicked.connect(self.replace_btn)
        self.pushButton_4.clicked.connect(self.replaceall_btn)

    def find_btn(self):
        self.label.clear()
        text = self.lineEdit.text()
        textEdit = self.master.tabWidget.currentWidget()
        founded = textEdit.findFirst(text, self.checkBox.isChecked(), True, True, self.checkBox_2.isChecked())
        if not founded:
            self.label.setStyleSheet("QLabel {color: red;}")
            self.label.setText(
                "没有找到 \"{}\"".format(
                    self.lineEdit.text()
                )
            )

    def replace_btn(self):
        self.label.setText('')
        self.master.tabWidget.currentWidget().replace(self.lineEdit_2.text())

    def replaceall_btn(self):
        self.label.setText('')
        textEdit = self.master.tabWidget.currentWidget()
        replaced = 0
        text = self.lineEdit.text()
        founded = textEdit.findFirst(text, self.checkBox.isChecked(), True, True, self.checkBox_2.isChecked())
        while founded:
            textEdit.replace(self.lineEdit_2.text())
            founded = textEdit.findNext()
            replaced += 1

        self.label.setStyleSheet("QLabel {color: red;}")
        self.label.setText(f"{replaced}处被替换")


