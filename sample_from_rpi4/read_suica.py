import os
import sys
from PySide6 import QtGui
from PySide6 import QtCore, QtWidgets, QtUiTools
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton
from PySide6.QtWidgets import QTableView
from PySide6.QtGui import QFont
import sqlite3

import datetime
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

# end::model[]

from dataclasses import dataclass
@dataclass
class FilePath:
    filename: str
    data_filename: str




class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        # QUiLoaderで.uiファイルを読み込む
        self.Ui_MainWindow = QtUiTools.QUiLoader().load("./suica_ui.ui")
        self.Ui_MainWindow.setWindowTitle("出退勤入力ツール")


        layout = QVBoxLayout()
        self.Ui_MainWindow.widget.setLayout(layout)
        self.layout = layout
        
        self.clearLayout(self.layout)
        DrawClock.draw_graph(self) # DrawClockは、execの中で定義する必要がある。 

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            childWidget = child.widget()
            if childWidget:
                childWidget.setParent(None)
                childWidget.deleteLater()


class DrawClock():
    def __init__(self, *args, **kwargs):
        super(DrawClock, self).__init__(*args, **kwargs)

    def draw_graph(self):
        #area = DockArea()
        win = pg.GraphicsLayoutWidget(show=True, title='Analog clock')
        init_window_size = 900
        win.resize(init_window_size, init_window_size)
        self.layout.addWidget(win)  
        

        pg.setConfigOptions(antialias=True)
        graph = win.addPlot()
        # 軸は非表示にする
        graph.showAxis('bottom', False) 
        graph.showAxis('left', False)
        # アスペクト比を固定する
        graph.setAspectLocked(lock=True)
        # マウスによる軸の移動を無効化する
        graph.setMouseEnabled(x=False, y=False)

        radius = 1

        # 円を描画する
        x = radius * np.cos(np.linspace(0, 2 * np.pi, 1000))
        y = radius * np.sin(np.linspace(0, 2 * np.pi, 1000))
        graph.plot(x, y, pen=pg.mkPen(width=6))


        for second in range(60):
            # ５の倍数のメモリは少し長く太くしてそれっぽさを出す
            line_length = 0.1 if second % 5 == 0 else 0.05
            line_width = 4 if second % 5 == 0 else 2

            # メモリの始点と終点の座標を求める
            x1 = np.sin(np.radians(360 * (second / 60))) * radius
            x2 = np.sin(np.radians(360 * (second / 60))) * (radius - line_length)
            y1 = np.cos(np.radians(360 * (second / 60))) * radius
            y2 = np.cos(np.radians(360 * (second / 60))) * (radius - line_length)

            # 描画する
            pen = pg.mkPen(width=line_width)
            pen.setCapStyle(QtCore.Qt.RoundCap)  # この設定をすることで線の端が丸くなります
            graph.plot([x1, x2], [y1, y2], pen=pen)


        font_size = 48

        hour_texts = []

        for hour in range(1, 13, 1):
            x = np.sin(np.radians(360 * (hour / 12))) * radius * 0.8
            y = np.cos(np.radians(360 * (hour / 12))) * radius * 0.8

            # anchorは位置の基準をテキストのどこにおくかを指定します
            # anchor=(0, 0)だとテキストの左上、anchor=(1, 1)だと右下が基準になります
            # ここではテキストの中心を基準にするためにanchor=(0.5, 0.5)とします
            hour_text = pg.TextItem(text=str(hour), anchor=(0.5, 0.5))
            # 位置を設定する
            hour_text.setPos(x, y)
            # フォントサイズを指定する
            font = QtGui.QFont()
            font.setPixelSize(font_size)
            hour_text.setFont(font)
            graph.addItem(hour_text)
            hour_texts.append(hour_text)

        # 日付と曜日
        dt_now = datetime.datetime.now()
        date_str = '{}/{}/{} {}'.format(dt_now.year, dt_now.month, dt_now.day, dt_now.strftime('%a'))
        date_text = pg.TextItem(text=date_str, anchor=(0.5, 0.5))
        date_text.setPos(0, -radius / 3.5)
        font = QtGui.QFont()
        font.setPixelSize(int(font_size / 2))
        date_text.setFont(font)
        graph.addItem(date_text)

        # 時刻のデジタル表示
        time_text = pg.TextItem(text='00:00:00', anchor=(0.5, 0.5))
        time_text.setPos(0, -radius / 2.5)
        time_text.setFont(font)
        graph.addItem(time_text)

        # 短針
        pen = pg.mkPen(width=12)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        hour_hand_plot = graph.plot(pen=pen)

        # 長針
        pen = pg.mkPen(width=6)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        minute_hand_plot = graph.plot(pen=pen)

        # 秒針
        pen = pg.mkPen(width=2)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        second_hand_plot = graph.plot(pen=pen)


        def set_time(hour, minute, second):
            # 時計の針の角度（１２時の方向が０度で右回りが正）
            deg_second = (second / 60) * 360
            deg_minute = (minute / 60) * 360 + (1 / 60) * 360 * (second / 60)
            deg_hour = (hour / 12) * 360 + (1 / 12) * 360 * (minute / 60)

            # 針の長さを適当に決める
            second_hand_length = 0.85
            minute_hand_length = 0.8
            hour_hand_length = 0.5

            # 針を描画する
            x_second = np.sin(np.radians(deg_second)) * radius * second_hand_length
            y_second = np.cos(np.radians(deg_second)) * radius * second_hand_length
            second_hand_plot.setData([0, x_second], [0, y_second])

            x_minute = np.sin(np.radians(deg_minute)) * radius * minute_hand_length
            y_minute = np.cos(np.radians(deg_minute)) * radius * minute_hand_length
            minute_hand_plot.setData([0, x_minute], [0, y_minute])

            x_hour = np.sin(np.radians(deg_hour)) * radius * hour_hand_length
            y_hour = np.cos(np.radians(deg_hour)) * radius * hour_hand_length
            hour_hand_plot.setData([0, x_hour], [0, y_hour])

            # デジタル表示を描画する
            time_str = '{:02d}:{:02d}:{:02d}'.format(hour, minute, second)
            time_text.setText(time_str)
        
        #set_time(self, 10, 10, 35)


        def update_clock():
            dt_now = datetime.datetime.now()
            h = dt_now.hour
            m = dt_now.minute
            s = dt_now.second

            set_time(h, m, s)

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(update_clock)
        self.update_timer.start(50)  # 更新周期は50ms


        #self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(update)
        #self.timer.start(50)

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
