import subprocess
import sys

from PyQt5 import QtCore
import re
import os
import numpy
from PyQt5.Qsci import QsciScintillaBase
from PyQt5.QtGui import QIcon, QTextCursor, QColor, QFont
from PyQt5.QtWidgets import QTreeWidgetItem
import matplotlib.pyplot as plt


class FunctionValue:
    def __init__(self, filepath = '', name = '', val_type = '', type = "",line = ""):
        self.filepath = filepath
        self.name = name
        self.val_type = val_type
        self.type = type
        self.line = line
        self.list = []
        self.father = ""
        self.flag = 0

    def add(self, value):
        self.list.append(value)

class FileFunction(QtCore.QObject):
    stop_singnal = QtCore.pyqtSignal(str)
    def __init__(self, filename, parent=None):
        super(FileFunction, self).__init__(parent)
        self.master = parent
        self.filename = filename
        self.filelist = []
        self.funlist = []

        self.vallist = []
        self.validfun = []
        self.validval = []
        self.dic = {"最危险":0, "很危险":0, "危险":0, "很危险（或稍小，取决于实现）":0, "中等危险":0, "低危险":0, "无效函数和变量": 0}
        self.keyword = ["SHORT", "INT", "LONG", "CHAR", "FLOAT", "DOUBLE", "VOID"]
        self.master.tabWidget.currentChanged.connect(self.tree_display)
        self.master.treeWidget.doubleClicked.connect(self.tree_find)
        self.master.treeWidget_1.doubleClicked.connect(self.tree_1_find)
        self.master.Pie.triggered.connect(self.pie_show)
        self.master.Goto.triggered.connect(self.goto_declaration)
        self.master.Compile.triggered.connect(self.compile)
        self.master.Run.triggered.connect(self.run)



    def add(self, filepath):
        self.filelist.append(filepath)

    def get_function(self):
        filename = self.filename
        path, name = os.path.split(filename)
        self.getfile(path)
        cmd = ".\\resource\\program\\ctags.exe --languages=c -R -I argv --kinds-c=+defglmpstuvx --fields=+n"
        for s in self.filelist:
            cmd += " " + s
        os.system(cmd)
        f = open("tags", "r")
        code = f.readlines()
        f.close()
        for line in code:
            if line.startswith("!_TAG"):
                continue
            split_line = line.split('\t')
            print(split_line)
            fun = FunctionValue()
            fun.name = split_line[0]
            fun.filepath = split_line[1]
            if len(split_line) == 8 or len(split_line) == 6:
                fun.line = split_line[4]
                fun.type = split_line[3]
                if fun.type == 'l':
                    fun.val_type = split_line[6].split(":")[-1]
                    fun.father = split_line[5].split(":")[-1]
                    self.vallist.append(fun)
                else:
                    fun.val_type = split_line[5].strip("\n").split(":")[-1]
                    if fun.type == 'f':
                        self.funlist.append(fun)
                    else:
                        if fun.type == "s":
                            fun.val_type = "struct"
                        self.vallist.append(fun)
            elif len(split_line) == 9:
                fun.line = split_line[5]
                fun.type = split_line[4]
                if fun.type == 'm':
                    fun.val_type = split_line[7].split(":")[-1]
                    fun.father = split_line[6]
                    self.vallist.append(fun)
                elif fun.type == 'l':
                    fun.val_type = split_line[7].split(":")[-2] + ' ' + split_line[7].split(":")[-1]
                    fun.father = split_line[6].split(":")[-1]
                    self.vallist.append(fun)
        for i in self.vallist:
            if i.type == 'm':
                for v in self.vallist:
                    if v.type == 's':
                        self.vallist[self.vallist.index(v)].add(i)
            elif i.type == 'l':
                for f in self.funlist:
                    if i.filepath == f.filepath and i.father == f.name:
                        self.funlist[self.funlist.index(f)].add(i)

    def tree_display(self):
        if self.master.tabWidget.count() == 0  or self.master.ismain == False:
            return
        self.master.treeWidget_1.clear()
        self.master.treeWidget_1.setColumnWidth(0, 300)
        filename = self.master.tabWidget.currentWidget().get_path() + '/' + self.master.tabWidget.currentWidget().get_name()
        file = QTreeWidgetItem(self.master.treeWidget_1)
        file.setText(0, "文件名：" + filename)
        fun = QTreeWidgetItem(self.master.treeWidget_1)
        fun.setText(0, "函数")
        val = QTreeWidgetItem(self.master.treeWidget_1)
        val.setText(0, "变量")
        for i in self.funlist:
            if i.filepath == filename:
                child = QTreeWidgetItem(fun)
                child.setText(0, i.name + '(' + i.line + ')')
                child.setText(1, i.val_type)
                child.setIcon(0, QIcon("./resource/icon/node_procedure.png"))
                if i.list != []:
                    for l in i.list:
                        child1 = QTreeWidgetItem(child)
                        child1.setText(0, l.name + '(' + l.line + ')')
                        child1.setText(1, l.val_type)
                        child1.setIcon(0, QIcon("./resource/icon/node_variable.png"))
        for i in self.vallist:
            if i.filepath == filename:
                if i.type == 'v':
                    child = QTreeWidgetItem(val)
                    child.setText(0, i.name + '(' + i.line + ')')
                    child.setText(1, i.val_type)
                    child.setIcon(0, QIcon("./resource/icon/node_variable.png"))
                elif i.type == 's':
                    child = QTreeWidgetItem(val)
                    child.setText(0, i.name + '(' + i.line + ')')
                    child.setText(1, i.val_type)
                    child.setIcon(0, QIcon("./resource/icon/node_variable.png"))
                    if i.list != []:
                        for l in i.list:
                            child1 = QTreeWidgetItem(child)
                            child1.setText(0, l.name + '(' + l.line + ')')
                            child1.setText(1, l.val_type)
                            child1.setIcon(0, QIcon("./resource/icon/node_variable.png"))
        self.master.treeWidget_1.expandAll()

    def set_filelist(self):
        self.get_function()
        self.tree_display()
        self.report()
        self.stop_singnal.emit("")

    def getfile(self, filepath):
        # 遍历filepath下所有文件，包括子目录
        list = []
        files = os.listdir(filepath)
        for fi in files:
            if re.match("(\w*)\.c", fi) != None:
                fi_d = filepath + '/' + fi
                if not os.path.isdir(fi_d):
                    list.append(fi_d)
        self.filelist = list

    def report(self):
        self.master.treeWidget.clear()
        self.master.tabWidget_2.setCurrentIndex(0)
        fun_name = []
        fun_vul = []
        fun_sol = []
        f = open("fun.txt", "r")
        while True:
            s = f.readline().strip("\n")
            s = s.strip("\r")
            if s:
                fun_name.append(s.split('\t')[0])
                fun_vul.append(s.split('\t')[1])
                fun_sol.append(s.split('\t')[2])
            else:
                break
        f.close()
        danger = QTreeWidgetItem(self.master.treeWidget)
        danger.setText(0, "风险函数")
        for fn in self.filelist:
            f = open(fn, "r")
            s = f.readlines()
            f.close()
            for fun in fun_name:
                pattern = re.compile("\W" + fun + "[(]")
                for ss in s:
                    if re.search(pattern, ss) != None:
                        row = s.index(ss) + 1
                        index = fun_name.index(fun)
                        child = QTreeWidgetItem(danger)
                        child.setText(0, fn)
                        child.setText(1, "line:" + str(row))
                        child.setText(2, fun_name[index])
                        child.setText(3, fun_vul[index])
                        child.setText(4, fun_sol[index])
                        self.dic[fun_vul[index]] += 1
        for f in self.funlist:
            if f.name == 'main':
                main = f
        self.validfun.append(main)
        self.invalid_find(main, [])
        invalidfun = QTreeWidgetItem(self.master.treeWidget)
        invalidfun.setText(0, "无效函数")
        for f in list(set(self.funlist) - set(self.validfun)):
            child = QTreeWidgetItem(invalidfun)
            child.setText(0, f.filepath)
            child.setText(1, f.line)
            child.setText(2, f.name)
            self.dic["无效函数和变量"] += 1
        invalidval = QTreeWidgetItem(self.master.treeWidget)
        invalidval.setText(0, "无效变量")
        for f in list(set(self.vallist) - set(self.validval)):
            child = QTreeWidgetItem(invalidval)
            child.setText(0, f.filepath)
            child.setText(1, f.line)
            child.setText(2, f.name)
            self.dic["无效函数和变量"] += 1

    def open_demo(self, fileName):
        f = open("demo.txt", "w")
        text = "0$" + fileName + "$\n"
        f.write(text)
        f.close()
        os.system(".\\resource\\program\\lex.yy.exe  < " + fileName)
        f = open("demo.txt", "r")
        list = f.readlines()
        code = []
        for s in list:
            s.rstrip()
            str = s.split("$")
            result = [x.strip() for x in str if x.strip() != '']
            code.append(result)
        return code

    def get_main(self):
        for f in self.funlist:
            if f.name == 'main':
                return f.filepath

    def invalid_find(self, fun, l):
        code = self.open_demo(fun.filepath)
        flag = 0
        first = True
        l.append(fun)
        fline = fun.line.split(":")[-1]
        for line in code[int(fline):]:
            if len(line) > 1:
                if line[1] == '{' or line[-1] == '{':
                    flag += 1
                    first = False
                if line[1] == '}' or line[-1] == '}':
                    flag -= 1
            if flag == 0 and first == False:
                break
            for v in self.vallist:
                if v.name in line:
                    index = line.index(v.name)
                    if len(line) > index + 1:
                        if line[index + 1] != "(" and v.line != "line:" + self.get_linenum(line[0]) and v in fun.list:
                            self.validval.append(v)
                    else:
                        if v.line != "line:" + self.get_linenum(line[0]) and v in fun.list:
                            self.validval.append(v)
            for v in self.vallist:
                if v.name in line and v not in self.validval and v.filepath == fun.filepath:
                    index = line.index(v.name)
                    if len(line) > index + 1:
                        if line[index + 1] != "(" and v.line != "line:" + self.get_linenum(line[0]):
                            print(line)
                            self.validval.append(v)
                    else:
                        if v.line != "line:" + self.get_linenum(line[0]):
                            self.validval.append(v)
            for f in self.funlist:
                if f.name in line and f not in self.validfun:
                    index = line.index(f.name)
                    if line[index + 1] == '(' and f.line != "line:" + self.get_linenum(line[0]):
                        self.validfun.append(f)
        if self.validfun != l:
            for f in list(set(self.validfun) - set(l)):
                self.invalid_find(f, l)

    def tree_find(self):
        filename = self.master.treeWidget.currentItem().text(0)
        text = self.master.treeWidget.currentItem().text(1)
        if "line" in text:
            line = int(text.strip(')').split(":")[-1])
            self.master.file_display(filename)
            textedit = self.master.tabWidget.currentWidget()
            textedit.setSelection(line, 0, line - 1, 0)

    def tree_1_find(self):
        text = self.master.treeWidget_1.currentItem().text(0)
        if "line" in text:
            line = int(text.strip(')').split(":")[-1])
            print(line)
            textedit = self.master.tabWidget.currentWidget()
            textedit.setSelection(line, 0, line - 1, 0)

    def goto_declaration(self):
        filename = self.master.tabWidget.currentWidget().get_path() + "/" + self.master.tabWidget.currentWidget().get_name()
        position = self.master.tabWidget.currentWidget().getSelection()
        text = self.master.tabWidget.currentWidget().text()
        code = text.split("\n")
        print(code)
        print(position)
        word = code[position[0]][position[1]:position[3]]
        print(word)
        code = self.open_demo(filename)
        for line in code:
            if line[1] in self.keyword and len(line) > 4 and line[3] == '(':
                name = line[2]
                for f in self.funlist:
                    if f.name == name:
                        fun = f
                        flag = 0
                        first = True
            if len(line) > 1:
                if line[1] == '{' or line[-1] == '{':
                    flag += 1
                    first = False
                if line[1] == '}' or line[-1] == '}':
                    flag -= 1
            print(line)
            linenum = int(self.get_linenum(line[0]))
            if word in line and linenum == position[0] + 1:
                print("c")
                index = line.index(word)
                if len(line) > index :
                    print("c")
                    if line[index + 1] == '(':
                        for f in self.funlist:
                            if f.name == word:
                                self.master.file_display(f.filepath)
                                textedit = self.master.tabWidget.currentWidget()
                                line = int(f.line.split(":")[-1])
                                textedit.setSelection(line - 1, 0, line - 1, 0)
                    else:
                        print("d")
                        for v in self.vallist:
                            if v.name == word and filename == v.filepath:
                                print("d")
                                if flag == 0 and first == False:
                                    if v.type != "l":
                                        self.master.file_display(filename)
                                        textedit = self.master.tabWidget.currentWidget()
                                        line = int(v.line.split(":")[-1])
                                        textedit.setSelection(line - 1, 0, line - 1, 0)
                                else:
                                    if v in fun.list:
                                        self.master.file_display(filename)
                                        textedit = self.master.tabWidget.currentWidget()
                                        line = int(v.line.split(":")[-1])
                                        textedit.setSelection(line - 1, 0, line - 1, 0)
                                    else:
                                        self.master.file_display(filename)
                                        textedit = self.master.tabWidget.currentWidget()
                                        line = int(v.line.split(":")[-1])
                                        textedit.setSelection(line - 1, 0, line - 1, 0)

    def pie_show(self):
        plt.rcParams['font.sans-serif'] = 'SimHei'
        plt.figure(figsize=(12, 5))
        explode = []
        keys = list(self.dic.keys())
        values = list(self.dic.values())
        label = []
        vals = []
        length = len(list(self.dic.values()))
        for i in range(length):
            if values[i] != 0:
                label.append(keys[i])
                vals.append(values[i])
                explode.append(0.01)
        patches,l_text,p_text = plt.pie(vals, explode=explode, labels=label, autopct='%1.1f%%')
        for t in l_text:
            t.set_size = (30)
        for t in p_text:
            t.set_size = (20)
        plt.axis('equal')
        plt.legend()
        plt.title('风险报告')
        plt.savefig('风险报告.jpg')
        plt.show()

    def get_linenum(self, line):
        pattern = re.compile("[0-9]+")
        m = re.search(pattern, line)
        return m.group(0)

    def get_all_file(self, filepath):
        # 遍历filepath下所有文件，包括子目录
        list = []
        files = os.listdir(filepath)
        for fi in files:
            if re.match("(\w*)\.c$", fi) != None:
                fi_d = filepath + '/' + fi
                if not os.path.isdir(fi_d):
                    list.append(fi_d)
            if re.match("(\w*)\.h$", fi) != None:
                fi_d = filepath + '/' + fi
                if not os.path.isdir(fi_d):
                    list.append(fi_d)
        return list

    def compile(self):
        self.master.tabWidget_2.setCurrentIndex(1)
        cmd = "clang.exe"
        filename = self.filename
        path, name = os.path.split(filename)
        filelist = self.get_all_file(path)
        for i in range(len(filelist)):
            filelist[i] += " "
        env = os.environ
        p = subprocess.Popen([cmd, filelist], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=".")
        stdout = []
        stderr = []
        while (True):
            reads = [p.stderr.fileno()]
            read = p.stderr.readline()
            read = read.decode('utf-8')
            sys.stderr.write(read)
            stderr.append(read)
            if (p.poll() != None):
                break
        stderr = ''.join(stderr)
        if stdout == [] and stderr == "":
            result = "编译成功"
            self.master.textEdit_2.setText(result)
            return
        self.master.textEdit_2.setText(stderr)

    def run(self):
        subprocess.Popen(["cmd",'/c','a.exe & pause'],creationflags =subprocess.CREATE_NEW_CONSOLE)









