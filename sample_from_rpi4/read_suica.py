import os
import sys
from PySide6 import QtCore, QtWidgets, QtUiTools
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton
from PySide6.QtWidgets import QTableView
from PySide6.QtGui import QFont
import sqlite3


import sys

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication



sys.setrecursionlimit(2000)



# Key Event
from PySide6.QtCore import Qt

# 自作のライブラリ
import numpy as np
import pandas as pd
import math

def test_deco(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper

os.environ["PYSIDE_DESIGNER_PLUGINS"]="."
os.environ["QT_LOGGING_RULES"]='*.debug=false;qt.pysideplugin=false'
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)


"""
This example demonstrates many of the 2D plotting capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with 
the left/right mouse buttons. Right click on any plot to show a context menu.
"""
import numpy as np
import pyqtgraph as pg
import pandas as pd
import math
import matplotlib.pyplot as plt


import pyqtgraph as pg

fontCss = {'font-family': "Arial, Meiryo", 'font-size': '16pt'}
fontCss["color"] = '#fff' 

# DockLabelをグレーにする
# http://fatbald.seesaa.net/article/451667700.html
from pyqtgraph.dockarea.Dock import DockLabel
def updateStyle(self):
    self.setStyleSheet("DockLabel { color: #FFF; background-color: #444; font-size:20pt}")
setattr(DockLabel, 'updateStyle', updateStyle)


# tag::model[]

class FileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, path=None):
        super().__init__()

        self.path_dash = './models/dash'

# end::model[]

from dataclasses import dataclass
@dataclass
class FilePath:
    filename: str
    data_filename: str


import platform
osname = platform.system()
def get_screensize():
    if osname == 'Darwin':
        from screeninfo import get_monitors
        for monitor in get_monitors():
            width = monitor.width
            height = monitor.height
        return width, height
    elif osname == 'Windows':
        import ctypes
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize[0], screensize[1]




class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        # QUiLoaderで.uiファイルを読み込む
        
        self.Ui_MainWindow = QtUiTools.QUiLoader().load("./suica_ui.ui")
        self.Ui_MainWindow.setWindowTitle("Awesome Visualization TOOL")


        osname = platform.system()
        width, height = get_screensize()
        if width > 1920 and height > 1200:
            self.Ui_MainWindow.setGeometry(0, 0, 1920, 1080) # WQXGA (Wide-QXGA)
        else:
            self.Ui_MainWindow.setGeometry(0, 0, 1024, 768) # WQXGA (Wide-QXGA)

        if osname == 'Darwin':
            font = QFont()
            font.setPointSize(18)
            font1 = QFont()
            font1.setPointSize(14)
            font2 = QFont()
            font2.setPointSize(14)
            font3 = QFont()
            font3.setPointSize(14)
            font4 = QFont()
            font4.setPointSize(14)
            font5 = QFont()
            font5.setPointSize(20)
            font6 = QFont()
            font6.setPointSize(20)
            self.Ui_MainWindow.btnFin.setFont(font)
            self.Ui_MainWindow.btnMyData.setFont(font)
            self.Ui_MainWindow.btnAnalytic.setFont(font)
            self.Ui_MainWindow.label_2.setFont(font1)
            self.Ui_MainWindow.treeView.setFont(font2)
            self.Ui_MainWindow.label.setFont(font1)
            self.Ui_MainWindow.treeViewData.setFont(font2)
            self.Ui_MainWindow.label_3.setFont(font3)
            self.Ui_MainWindow.codeView.setFont(font4)
            self.Ui_MainWindow.label_4.setFont(font5)
            self.Ui_MainWindow.lineNum.setFont(font6)
            self.Ui_MainWindow.plotButton.setFont(font5)
            self.Ui_MainWindow.quitButton.setFont(font5)

        elif osname == 'Windows':

            font = QFont()
            font.setPointSize(14)
            font1 = QFont()
            font1.setPointSize(14)
            font2 = QFont()
            font2.setPointSize(14)
            font3 = QFont()
            font3.setPointSize(10)
            font4 = QFont()
            font4.setPointSize(14)
            font5 = QFont()
            font5.setPointSize(14)
            font6 = QFont()
            font6.setPointSize(14)
            self.Ui_MainWindow.btnFin.setFont(font)
            self.Ui_MainWindow.btnMyData.setFont(font)
            self.Ui_MainWindow.btnAnalytic.setFont(font)
            self.Ui_MainWindow.label_2.setFont(font1)
            self.Ui_MainWindow.treeView.setFont(font2)
            self.Ui_MainWindow.label.setFont(font1)
            self.Ui_MainWindow.treeViewData.setFont(font2)
            self.Ui_MainWindow.label_3.setFont(font3)
            self.Ui_MainWindow.codeView.setFont(font4)
            self.Ui_MainWindow.label_4.setFont(font5)
            self.Ui_MainWindow.lineNum.setFont(font6)
            self.Ui_MainWindow.plotButton.setFont(font5)
            self.Ui_MainWindow.quitButton.setFont(font5)


        # ボタン操作
        self.Ui_MainWindow.btnFin.clicked.connect(lambda:self.pltFin())
        self.Ui_MainWindow.btnFin.setStyleSheet("QPushButton:checked{background-color: rgb(100, 200, 0)}")
        self.Ui_MainWindow.btnAnalytic.clicked.connect(lambda:self.pltAnalytic())
        self.Ui_MainWindow.btnAnalytic.setStyleSheet("QPushButton:checked{background-color: rgb(100, 200, 0)}")

        self.Ui_MainWindow.plotButton.clicked.connect(lambda:DataViz.load_model(self))


        # codeView関連のイベント
        self.Ui_MainWindow.codeView.installEventFilter(self)
        self.Ui_MainWindow.codeView.cursorPositionChanged.connect(self.count_line_number)
        self.Ui_MainWindow.codeView.textChanged.connect(self.auto_save_file)


        layout = QVBoxLayout()
        self.Ui_MainWindow.widget.setLayout(layout)
        self.layout = layout



    def pltProtoType(self):
        self.file_system_model = FileSystemModel()
        self.file_system_model.setRootPath(self.file_system_model.path_prototype)
        self.file_system_model.setNameFilters(['*.py','*.fo'])
        self.file_system_model.setNameFilterDisables(False)

        self.file_system_model_for_data = FileSystemModel()
        self.file_system_model_for_data.setRootPath(self.file_system_model_for_data.path_data)
        self.file_system_model_for_data.setNameFilters(['*.csv'])
        self.file_system_model_for_data.setNameFilterDisables(False)

        self.file_system_view = self.Ui_MainWindow.treeView
        self.file_system_view.setModel(self.file_system_model)
        self.file_system_view.setRootIndex(self.file_system_model.index(self.file_system_model.path_prototype))
        self.file_system_view.setColumnWidth(0,300)

        self.file_system_view_for_data = self.Ui_MainWindow.treeViewData
        self.file_system_view_for_data.setModel(self.file_system_model_for_data)
        self.file_system_view_for_data.setRootIndex(self.file_system_model_for_data.index(self.file_system_model_for_data.path_data))
        self.file_system_view_for_data.setColumnWidth(0,300)

        self.file_system_view.clicked.connect(self.getFileContents)
        self.file_system_view_for_data.clicked.connect(self.getFileName)

    def pltMyData(self):
        pass


    def pltAnalytic(self):
        pass

    def pltFin(self):
        pass

    def pltMatplt(self):
        self.file_system_view.clicked.connect(self.getFileContents)
        self.file_system_view_for_data.clicked.connect(self.getFileName)

    def pltDash(self):
        self.file_system_view_for_data.clicked.connect(self.getFileName)


    def count_line_number(self):
        line_num = self.Ui_MainWindow.codeView.textCursor().blockNumber()
        line_num = str(line_num + 1) # 0行目から数え始めなので、+1。
        self.Ui_MainWindow.lineNum.setText(line_num)
        # self.Ui_MainWindow.codeView.textChanged.textCursor().position()


    def getFileContents(self, index):
        '''
        クリックしたファイルの中身をtextに格納する。
        '''
        try:
            filepath = []
            indexItem = self.file_system_model.index(index.row(), 0, index.parent())
            if os.path.isfile(self.file_system_model.filePath(indexItem)):
                filepath.insert(0,self.file_system_model.filePath(indexItem))
                FilePath.filename = filepath[0]
                text = open(FilePath.filename, encoding='utf-8').read()
                self.Ui_MainWindow.codeView.setPlainText(text)
            else:
                pass

        except AttributeError as e:
            pass

    def getFileName(self, index):
        '''
        クリックしたファイルの中身をtextに格納する。
        '''
        try:
            filepath = []
            indexItem = self.file_system_model_for_data.index(index.row(), 0, index.parent())
            if os.path.isfile(self.file_system_model_for_data.filePath(indexItem)):
                filepath.insert(0,self.file_system_model_for_data.filePath(indexItem))
                FilePath.data_filename = filepath[0]
            else:
                pass

        except AttributeError as e:
            pass

    def auto_save_file(self):
        with open(FilePath.filename, encoding='utf-8', mode='w') as f:
            f.write(self.Ui_MainWindow.codeView.toPlainText())


    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            childWidget = child.widget()
            if childWidget:
                childWidget.setParent(None)
                childWidget.deleteLater()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.Ui_MainWindow.codeView:
            if event.key() == Qt.Key_Tab and self.Ui_MainWindow.codeView.hasFocus():
                # Special tab handling
                tc = self.Ui_MainWindow.codeView.textCursor()
                tc.insertText("    ")
                return True
            else:
                return False
        return False


class DataViz(MainWindow):
    def __init__(self, *args, **kwargs):
        super(DataViz, self).__init__(*args, **kwargs)

    def double_clicked(self):
        print("Double Clicked!!")

    def load_model(self):
        try:
            self.timer.stop()
            print("timer stopped!")
        except Exception as e:
            pass
        model_code = self.Ui_MainWindow.codeView.toPlainText()
        if FilePath.filename.endswith('.py'):
            #print("python!!")
            exec(model_code, globals()) # globals() を指定することでクラスがグローバルスコープに登録されます。)
        elif FilePath.filename.endswith('.fo'):
            pass
        self.clearLayout(self.layout)
        # インスタンスを作成して実行すると
        # RuntimeError: Internal C++ object (PlotDataItem) already deleted.
        # がでて、消せなかった。
        DrawGraph.draw_graph(self) # DrawGraphは、execの中で定義する必要がある。 
        

def main():
    # Qt Applicationを作ります
    app = QApplication(sys.argv)
    # formを作成して表示します
    mainWin = MainWindow()
    mainWin.Ui_MainWindow.show()
    # Qtのメインループを開始します
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
