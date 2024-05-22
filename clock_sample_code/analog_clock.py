from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import (QApplication,
                               QWidget)
import pyqtgraph as pg
import numpy as np
import datetime

win = pg.GraphicsLayoutWidget(show=True, title='Analog clock')
init_window_size = 800
win.resize(init_window_size, init_window_size)

pg.setConfigOptions(antialias=True)

graph = win.addPlot()
graph.showAxis('bottom', False)
graph.showAxis('left', False)
graph.setAspectLocked(lock=True)
graph.setMouseEnabled(x=False, y=False)

radius = 1

x = radius * np.cos(np.linspace(0, 2 * np.pi, 1000))
y = radius * np.sin(np.linspace(0, 2 * np.pi, 1000))
graph.plot(x, y, pen=pg.mkPen(width=6))

for second in range(60):
    line_length = 0.1 if second % 5 == 0 else 0.05
    line_width = 4 if second % 5 == 0 else 2
    x1 = np.sin(np.radians(360 * (second / 60))) * radius
    x2 = np.sin(np.radians(360 * (second / 60))) * (radius - line_length)
    y1 = np.cos(np.radians(360 * (second / 60))) * radius
    y2 = np.cos(np.radians(360 * (second / 60))) * (radius - line_length)
    pen = pg.mkPen(width=line_width)
    pen.setCapStyle(QtCore.Qt.RoundCap)
    graph.plot([x1, x2], [y1, y2], pen=pen)

font_size = 64

hour_texts = []

for hour in range(1, 13, 1):
    x = np.sin(np.radians(360 * (hour / 12))) * radius * 0.8
    y = np.cos(np.radians(360 * (hour / 12))) * radius * 0.8
    hour_text = pg.TextItem(text=str(hour), anchor=(0.5, 0.5))
    hour_text.setPos(x, y)
    font = QtGui.QFont()
    font.setPixelSize(font_size)
    hour_text.setFont(font)
    graph.addItem(hour_text)
    hour_texts.append(hour_text)

dt_now = datetime.datetime.now()
date_str = '{}/{}/{} {}'.format(dt_now.year, dt_now.month, dt_now.day, dt_now.strftime('%a'))
date_text = pg.TextItem(text=date_str, anchor=(0.5, 0.5))
date_text.setPos(0, -radius / 3.5)
font = QtGui.QFont()
font.setPixelSize(int(font_size / 2))
date_text.setFont(font)
graph.addItem(date_text)

time_text = pg.TextItem(text='00:00:00', anchor=(0.5, 0.5))
time_text.setPos(0, -radius / 2.5)
time_text.setFont(font)
graph.addItem(time_text)


pen = pg.mkPen(width=12)
pen.setCapStyle(QtCore.Qt.RoundCap)
hour_hand_plot = graph.plot(pen=pen)

pen = pg.mkPen(width=6)
pen.setCapStyle(QtCore.Qt.RoundCap)
minute_hand_plot = graph.plot(pen=pen)

pen = pg.mkPen(width=2)
pen.setCapStyle(QtCore.Qt.RoundCap)
second_hand_plot = graph.plot(pen=pen)


def set_time(hour, minute, second):
    deg_second = (second / 60) * 360
    deg_minute = (minute / 60) * 360 + (1 / 60) * 360 * (second / 60)
    deg_hour = (hour / 12) * 360 + (1 / 12) * 360 * (minute / 60)

    second_hand_length = 0.85
    minute_hand_length = 0.8
    hour_hand_length = 0.5

    x_second = np.sin(np.radians(deg_second)) * radius * second_hand_length
    y_second = np.cos(np.radians(deg_second)) * radius * second_hand_length
    second_hand_plot.setData([0, x_second], [0, y_second])

    x_minute = np.sin(np.radians(deg_minute)) * radius * minute_hand_length
    y_minute = np.cos(np.radians(deg_minute)) * radius * minute_hand_length
    minute_hand_plot.setData([0, x_minute], [0, y_minute])

    x_hour = np.sin(np.radians(deg_hour)) * radius * hour_hand_length
    y_hour = np.cos(np.radians(deg_hour)) * radius * hour_hand_length
    hour_hand_plot.setData([0, x_hour], [0, y_hour])

    time_str = '{:02d}:{:02d}:{:02d}'.format(hour, minute, second)
    time_text.setText(time_str)


def resize_text():
    size = win.size()
    height = size.height()
    width = size.width()
    new_font_size = font_size * (min(height, width) / init_window_size)

    font = QtGui.QFont()
    font.setPixelSize(int(new_font_size / 2))
    date_text.setFont(font)
    time_text.setFont(font)

    for hour_text in hour_texts:
        font = QtGui.QFont()
        font.setPixelSize(new_font_size)
        hour_text.setFont(font)


resize_timer = QtCore.QTimer()
resize_timer.timeout.connect(resize_text)
resize_timer.start(200)


def update_clock():
    dt_now = datetime.datetime.now()
    h = dt_now.hour
    m = dt_now.minute
    s = dt_now.second

    set_time(h, m, s)


update_timer = QtCore.QTimer()
update_timer.timeout.connect(update_clock)
update_timer.start(50)

if __name__ == '__main__':
    app = QApplication([])
    app.show()
