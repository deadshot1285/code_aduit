from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import *
from qtpy import QtGui

from untitled import Ui_MainWindow
from PyQt5.QtCore import *
from os.path import split as split_pathname
import function_form
import subprocess
from os.path import join as join_pathname
from text_area import *
from find_form import *
import os
from Parser import *


class MyWindow(QMainWindow, Ui_MainWindow):
    new_tab = pyqtSignal()
    nothing_open = pyqtSignal()
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.model = QFileSystemModel()
        self.setup()
        self.nothing_open.emit()
        self.ismain = False
        self.zoomsize = 9
        self.ctrlPressed = False

    def setup(self):
        self.new_tab.connect(self.enable_eidting)
        self.nothing_open.connect(self.disable_eidting)
        self.Open.triggered.connect(self.file_open)
        self.Save.triggered.connect(self.file_save)
        self.Saveas.triggered.connect(self.file_saveas)
        self.Close.triggered.connect(self.fileCloseTab)
        self.Closeall.triggered.connect(self.fileCloseAll)
        self.Exit.triggered.connect(self.closeEvent)
        self.Undo.triggered.connect(self.undo)
        self.Copy.triggered.connect(self.copy)
        self.Cut.triggered.connect(self.cut)
        self.CMD.triggered.connect(self.Cmd)
        self.Paste.triggered.connect(self.paste)
        self.Function.triggered.connect(self.function_Form)
        self.Find.triggered.connect(self.find_Form)
        self.treeView.doubleClicked.connect(self.tree_file)
        self.tabWidget.tabCloseRequested.connect(self.fileCloseTab)
        self.lineEdit.returnPressed.connect(self.cmd)
        self.splitter_2.setStretchFactor(0, 2)
        self.splitter_2.setStretchFactor(1, 6)
        self.splitter_2.setStretchFactor(2, 2)
        self.splitter.setStretchFactor(0, 70)
        self.splitter.setStretchFactor(1, 1)
        self.treeWidget.setColumnWidth(0, 500)
        self.treeWidget.setColumnWidth(1, 100)
        self.treeWidget.setColumnWidth(2, 100)
        self.treeWidget.setColumnWidth(3, 200)
        self.treeWidget.setColumnWidth(4, 700)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\document-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Open.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\document-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Save.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\document-save-as.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Saveas.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\close-tab.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Close.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\close-all-tabs.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Closeall.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\system-log-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Exit.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\edit-copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Copy.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\edit-cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Cut.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\edit-undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Undo.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\edit-paste.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Paste.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\edit-find-replace.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Find.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\goto-start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Goto.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\compile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Compile.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\run.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Run.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\utilities-terminal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CMD.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\node_function.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Function.setIcon(icon)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\resource\\icon\\theme-water.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Pie.setIcon(icon)


    def file_open(self):
        self.ismain = False
        self.treeWidget.clear()
        self.treeWidget_1.clear()
        self.fileCloseAll()
        self.treeView
        fileName, isOk = QFileDialog.getOpenFileName(self, "选取文件", "./", "C(*.c)")
        path, name = split_pathname(fileName)
        if isOk:
            f = open("demo.txt", "w")
            text = "0$" + fileName + "$\n"
            f.write(text)
            f.close()
            os.system(".\\resource\\program\\lex.yy.exe < " + fileName)
            f = open(fileName, "r")
            text = f.read()
            f.close()
            textEdit = TextArea(name, text, path)
            self.tabWidget.addTab(textEdit, textEdit.get_name())
            self.tabWidget.setCurrentWidget(textEdit)
            self.ismain = self.isMain()
            if self.ismain == True:
                self.model.setRootPath(path)
                self.model.setNameFilterDisables(False)
                self.model.setNameFilters(["*.c", "*.h"])
                self.treeView.setModel(self.model)
                self.treeView.setColumnHidden(1, True)
                self.treeView.setColumnHidden(2, True)
                self.treeView.setColumnHidden(3, True)
                self.treeView.setRootIndex(self.model.index(path))
                self.obj = FileFunction(fileName, self)
                self.mythread = QThread()
                self.obj.moveToThread = (self.mythread)
                self.mythread.started.connect(self.obj.set_filelist)
                self.obj.stop_singnal.connect(self.stop_td)
                self.mythread.start()
            self.new_tab.emit()

    def stop_td(self):
        print("b")
        self.mythread.quit()

    def wheelEvent(self, event):  # 滚轮事件
        if self.ctrlPressed:  # ctrl按下
            textEdit = self.tabWidget.currentWidget()
            try:
                if event.angleDelta().y() / 120.0 > 0:
                    self.zoomsize += 1
                else:
                    self.zoomsize -= 1
            except:
                pass
            #print(self.zoomsize)
            textEdit.setFont(QFont("Consolas, 'Courier New', monospace", self.zoomsize))
        else:  #
            return super().wheelEvent(event)
    def keyReleaseEvent(self, QKeyEvent):#按键弹起
        if QKeyEvent.key() == QtCore.Qt.Key_Control:
            self.ctrlPressed = False
        return super().keyReleaseEvent(QKeyEvent)
    def keyPressEvent(self, event):#按键按下
        if event.key() == Qt.Key_Control:
            self.ctrlPressed = True

    def file_display(self, filename):
        path, name = split_pathname(filename)
        for i in range(self.tabWidget.count()):
            textEdit = self.tabWidget.widget(i)
            if textEdit.get_path() + '/' + textEdit.get_name() == filename:
                self.tabWidget.setCurrentWidget(textEdit)
                return
        else:
            f = open(filename, "r")
            text = f.read()
            f.close()
            textEdit = TextArea(name, text, path)
            self.tabWidget.addTab(textEdit, textEdit.get_name())
            self.tabWidget.setCurrentWidget(textEdit)
            self.new_tab.emit()

    def tree_file(self):
        filename = self.model.filePath(self.treeView.currentIndex())
        self.file_display(filename)

    def file_save(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit is None or not isinstance(textEdit, QsciScintilla):
            return True
        try:
            print(textEdit.get_name())
            filename = textEdit.get_path() + '/' + textEdit.get_name()
            f = open(filename, "w")
            f.write(textEdit.text().replace("\r", ''))
            f.close()
            textEdit.modified = False
            return True
        except EnvironmentError as e:
            print(e)
            return False

    def file_saveas(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit is None or not isinstance(textEdit, QsciScintilla):
            return True
        filename, isOk = QFileDialog.getSaveFileName(self, "另存为", "./", "*")
        if isOk:
            f = open(filename, "w")
            f.write(textEdit.text().replace("\r", ''))
            f.close()
            textEdit.modified = False
            return True

    def fileCloseTab(self):
        textEdit = self.tabWidget.currentWidget()
        if textEdit is None or not isinstance(textEdit, QsciScintilla):
            return
        if (textEdit.modified == True and
                QMessageBox.question(self,
                                     "Text Editor - Unsaved Changes",
                                     "Save unsaved changes in {0}?".format(textEdit.get_name()),
                                     QMessageBox.Yes | QMessageBox.No) ==
                QMessageBox.Yes):
            try:
                self.file_save()
            except EnvironmentError as e:
                QMessageBox.warning(self,
                                    "Text Editor -- Save Error",
                                    "Failed to save {0}: {1}".format(textEdit.get_name(), e))
        self.tabWidget.removeTab(self.tabWidget.currentIndex())
        if self.tabWidget.count() == 0:
            self.nothing_open.emit()

    def fileCloseAll(self):
        failures = []
        self.tabWidget_2.setCurrentIndex(0)
        for i in range(self.tabWidget.count()):
            textEdit = self.tabWidget.widget(i)
            if textEdit is None or not isinstance(textEdit, QsciScintilla):
                return
            try:
                if (textEdit.modified == True and
                        QMessageBox.question(self,
                                             "Text Editor - Unsaved Changes",
                                             "Save unsaved changes in {0}?".format(textEdit.get_name()),
                                             QMessageBox.Yes | QMessageBox.No) ==
                        QMessageBox.Yes):
                    try:
                        self.file_save()
                    except EnvironmentError as e:
                        QMessageBox.warning(self,
                                            "Text Editor -- Save Error",
                                            "Failed to save {0}: {1}".format(textEdit.get_name(), e))
                self.tabWidget.removeTab(i)
            except IOError as e:
                failures.append(str(e))
        if (failures and QMessageBox.warning(self, "Text Editor -- Save Error",
                                             "Failed to save{0}\nQuit anyway?".format("\n\t".join(failures)),
                                             QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
            return False
        return True


    def is_open_something(self):
        return self.tabWidget.count() != 0

    def undo(self):
        if self.is_open_something():
            self.tabWidget.currentWidget().undo()

    def copy(self):
        if self.is_open_something():
            self.tabWidget.currentWidget().copy()

    def cut(self):
        if self.is_open_something():
            self.tabWidget.currentWidget().cut()

    def paste(self):
        if self.is_open_something():
            self.tabWidget.currentWidget().paste()

    def enable_eidting(self):
        self.Save.setEnabled(True)
        self.Saveas.setEnabled(True)
        self.Close.setEnabled(True)
        self.Closeall.setEnabled(True)
        self.Compile.setEnabled(True)
        self.Run.setEnabled(True)
        self.Pie.setEnabled(True)
        for i in self.Edit.actions():
            i.setEnabled(True)
        self.Find.setEnabled(True)

    def disable_eidting(self):
        self.Save.setEnabled(False)
        self.Saveas.setEnabled(False)
        self.Close.setEnabled(False)
        self.Closeall.setEnabled(False)
        self.Compile.setEnabled(False)
        self.Run.setEnabled(False)
        self.Pie.setEnabled(False)
        for i in self.Edit.actions():
            i.setEnabled(False)
        self.Find.setEnabled(False)

    def isMain(self):
        f = open("demo.txt", "r")
        list = f.readlines()
        code = []
        for s in list:
            s.rstrip()
            str = s.split("$")
            result = [x.strip() for x in str if x.strip()!='']
            code.append(result)
        print(code)
        for s in code:
            if "main" in s:
                i = s.index("main")
                if s[i + 1] == '(':
                    return True
        QMessageBox.information(self, ("查找main函数"), ("未找到到main函数"),
                                 QMessageBox.StandardButtons(QMessageBox.Yes))
        self.tabWidget.removeTab(self.tabWidget.currentIndex())
        self.nothing_open.emit()
        return False

    def function_Form(self):
        self.fun = function_form.functionForm()
        self.fun.show()

    def find_Form(self):
        self.findform = FindForm(self)
        self.findform.show()

    def closeEvent(self, event):
        if self.fileCloseAll() == False:
            event.ignore()
            return
        else:
            self.close()

    def cmd(self):
        self.tabWidget_2.setCurrentIndex(1)
        cmd = self.lineEdit.text().strip('\r')
        cmd = cmd.strip('\n')
        self.textEdit_2.append(cmd)
        env = os.environ
        print(cmd)
        p = subprocess.Popen(["cmd", '/c', "{:s}".format(cmd)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                             cwd=".")
        (stdout, stderr) = p.communicate()
        print(stdout.decode("gbk"))
        self.textEdit_2.append(stdout.decode("gbk"))
        self.textEdit_2.append(stderr.decode("gbk"))

    def Cmd(self):
        print("a")
        subprocess.Popen(["cmd",'/c','cmd'],creationflags =subprocess.CREATE_NEW_CONSOLE)

