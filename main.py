# -*- coding: utf-8 -*-

from form import *
import sys
def main():
    app = QApplication(sys.argv)
    mywin = MyWindow()
    mywin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

