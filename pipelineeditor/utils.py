import traceback
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def dump_exception(e):
    print("Exeption:", e)
    traceback.print_tb(e.__traceback__)


def loadStylesheet(filename):
    print(f"STYLE loading: {filename}")
    q_file = QFile(filename)
    q_file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = q_file.readAll()
    QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf-8"))


def loadStylesheets(*args):
    res = ''

    for arg in args:
        q_file = QFile(arg)
        q_file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = q_file.readAll()
        res += '\n' + str(stylesheet, encoding='utf-8')

    QApplication.instance().setStyleSheet(res)