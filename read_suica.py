import os
import sys
from PySide6 import QtGui
from PySide6 import QtCore, QtWidgets, QtUiTools
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLabel, QMessageBox, QDialogButtonBox
from PySide6.QtWidgets import QTableView
from PySide6.QtGui import QFont

import datetime
import sys

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)

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
import pyqtgraph as pg
import pandas as pd
import math


fontCss = {'font-family': "Arial, Meiryo", 'font-size': '16pt'}
fontCss["color"] = '#fff' 







# tag::model[]

# end::model[]

from dataclasses import dataclass
@dataclass
class FilePath:
    filename: str
    data_filename: str

import binascii
import nfc
import time
import sys
from threading import Thread, Timer

# Suica待ち受けの1サイクル秒
TIME_cycle = 1.0
# Suica待ち受けの反応インターバル秒
TIME_interval = 0.2
# タッチされてから次の待ち受けを開始するまで無効化する秒
TIME_wait = 3

# NFC接続リクエストのための準備
# 212F(FeliCa)で設定
target_req_suica = nfc.clf.RemoteTarget("212F")
# 0003(Suica)
target_req_suica.sensf_req = bytearray.fromhex("0000030000")


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        # QUiLoaderで.uiファイルを読み込む
        self.Ui_MainWindow = QtUiTools.QUiLoader().load("./suica_ui.ui")
        self.Ui_MainWindow.setWindowTitle("出退勤入力ツール")

        # pressedは、すぐリリースされる。
        self.Ui_MainWindow.shukkinnButton.setStyleSheet("QPushButton::checked{background-color: #aaff00}")
        self.Ui_MainWindow.taikinButton.setStyleSheet("QPushButton:checked{background-color: #aaff00}")
        #self.Ui_MainWindow.shukkinnButton.toggle()
        #self.Ui_MainWindow.taikinButton.toggle()
        self.Ui_MainWindow.readButton.clicked.connect(self.read_card)
        #self.Ui_MainWindow.shukkinnButton.released.connect(lambda:self.device_close())
        #self.Ui_MainWindow.taikinButton.clicked.connect(self.taikin)
        #self.Ui_MainWindow.taikinButton.released.connect(lambda:self.device_close())




        layout = QVBoxLayout()
        self.Ui_MainWindow.widget.setLayout(layout)
        self.layout = layout
        self.clearLayout(self.layout)
        DrawClock.draw_graph(self) # DrawClockは、execの中で定義する必要がある。 



    def read_card(self):
        import sqlite3
        dbname = 'idm_and_name.db'
        conn = sqlite3.connect(dbname)
        df = pd.read_sql_query('SELECT * FROM persons', conn)

        if self.Ui_MainWindow.shukkinnButton.isChecked():
            try:
                dt_now = now.strftime('%Y/%m/%d %I:%M(%p)')
                idm = self.readSuica()
                if idm == 0:
                    #button = QMessageBox.question(self, "Error dialog", "読み取りできません。")
                    #if button == QMessageBox.Yes:
                    #    print("Yes!")
                    #else:
                    #    print("No!")

                    QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

                    buttonBox = QDialogButtonBox(QBtn)
                    print('can not read')
                    #buttonBox.accepted.connect(accept)
                    #buttonBox.rejected.connect(reject)
                    layout = QVBoxLayout()
                    message = QLabel('test')
                    layout.addWidget(message)
                    layout.addWidget(buttonBox)
                    QDialog.setLayout(layout)

                else:
                    if pd.isnull(df.query('idm == idm')['name'].values[0]):
                        button = QMessageBox.question(self, "Error", "未登録です!")
                        if button == QMessageBox.Yes:
                            print("Yes!")
                        else:
                            print("No!")
                    else:
                        name = df.query('idm == idm')['name'].values[0]
                        print(name)

                        button = QMessageBox.question(self, "Result", str(name)+'\n'+str(dt_now)+"\n登録しますか?")
                        if button == QMessageBox.Yes:
                            print("Yes!")
                        else:
                            print("No!")
                #msg = QMessageBox()
                #msg.question(currentWindow, None, "Notice!", idm+'\n'+'出勤\n'+str(dt_now), QMessageBox.Yes)
                #QMessageBox.about(icon, '出勤', idm, dt_now)
            except:
                pass


        elif self.Ui_MainWindow.taikinButton.isChecked():
            try:
                dt_now = datetime.datetime.now()
                idm = self.readSuica()
                print('退勤', idm, dt_now)
            except:
                print('Read Error!')


    def readSuica(self):
        idm = 0
        try:
            clf = nfc.ContactlessFrontend('usb')
            self.clf = clf
            try_num = 0
            while True:
                # Suica待ち受け開始
                # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
                target_res = clf.sense(target_req_suica, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)
                #print(type(target_res))
                if target_res is None:
                    try_num = try_num + 1
                    if try_num > 3:
                        clf.close()
                        break
                    else:
                        pass
                else:
                    #tag = nfc.tag.tt3.Type3Tag(clf, target_res)
                    #なんか仕様変わったっぽい？↓なら動いた
                    tag = nfc.tag.activate_tt3(clf, target_res)
                    tag.sys = 3

                    #IDmを取り出す
                    idm = binascii.hexlify(tag.idm).decode()
                    clf.close()
                    break
            return idm

        except KeyboardInterrupt:
            self.clf.close()
            print(' Catch Ctrl-C. 終了します!')

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            childWidget = child.widget()
            if childWidget:
                childWidget.setParent(None)
                childWidget.deleteLater()

class CustomDialog(QDialog):
    def __init__(self, arg, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")
        #self.message_text = arg

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(arg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)






class DrawClock():
    def __init__(self, *args, **kwargs):
        super(DrawClock, self).__init__(*args, **kwargs)

    def draw_graph(self):
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


        font_size = 36

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
