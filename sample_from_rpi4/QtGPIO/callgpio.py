'''
2021.1.25作成
GPIOコントロールのテストアプリ

【解決済みの課題】
・lineeditから変数に設定
・sleepで画面ロックする件
・

【今後の課題】
・ステータスボタンの実装
・message windowの位置の指定
・プログレスバーの実装
・残時間の表示
・csvのドラッグｎドロップで、グラフ表示
・グラフのｘ軸を時間に


'''
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtCore import QObject, pyqtSignal
from Ltika_ui import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtTest

import pigpio
import time

'''
2021.1.21現在の設定
'''
gpio_pin0 = 12
gpio_pin1 = 13
pi = pigpio.pi()

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # ここまでは必須
        self.ui.addButton.clicked.connect(self.dispsum)
        self.ui.pushButton_2.clicked.connect(self.stopClicked)
        # ウィンドウサイズを固定
        self.setFixedSize(350, 200)
        self.ui.pushButton.clicked.connect(self.terminate)

    def parityCheck(self,num):
        range_list = []
        if num %2 != 1:
            range_list = [0,1000000,1000]
            return range_list
        else:
            range_list = [1000000,0,-1000]
            return range_list

    def dispsum(self):
        self.stop = False
        try:
            isinstance(float(self.ui.lineFirstNumber.text()),float)
        except ValueError:
            QMessageBox.warning(None, "Notice!", "数字を入力してください。", QMessageBox.Yes)
        else:
            a = float(self.ui.lineFirstNumber.text())
            sum=a
            self.ui.labelAddition.setText("繰り返し: " +str(sum)+' '+str(type(sum)))                
            pi.set_mode(gpio_pin0, pigpio.OUTPUT)
            pi.set_mode(gpio_pin1, pigpio.OUTPUT)
            try:
                num = 0
                while num < a:
                    range_list = self.parityCheck(num)
                    flag = False
                    for i in range(range_list[0],range_list[1],range_list[2]):
                        # GPIO18: 2Hz、duty比0.5
                        pi.hardware_PWM(gpio_pin1, 50, i)
                        # GPIO19: 8Hz、duty比0.1
                        pi.hardware_PWM(gpio_pin0, 50, i)
                        QtTest.QTest.qWait(1)
                        print(num, i)
                        if self.stop:
                            self.stop = False
                            flag = True
                            break
                    num +=1
                    if flag:
                        break
                '''
                    pi.write(gpio_pin0,1)
                    pi.write(gpio_pin1,1)
                    QtTest.QTest.qWait(1000)
                    pi.write(gpio_pin0,0)
                    pi.write(gpio_pin1,0)
                    QtTest.QTest.qWait(1000)
                    num +=1
                    if self.stop:
                        self.stop = False
                        break
                '''
            except KeyboardInterrupt:
                QMessageBox.warning(None, "Notice!", "Ctrl-Cが押されました。", QMessageBox.Yes)
                pi.set_mode(gpio_pin0, pigpio.INPUT)
                pi.set_mode(gpio_pin1, pigpio.INPUT)

            pi.set_mode(gpio_pin0, pigpio.INPUT)
            pi.set_mode(gpio_pin1, pigpio.INPUT)

    def stopClicked(self):
        pi.set_mode(gpio_pin0, pigpio.INPUT)
        pi.set_mode(gpio_pin1, pigpio.INPUT)
        self.stop = True

    def terminate(self):
        pi.set_mode(gpio_pin0, pigpio.INPUT)
        pi.set_mode(gpio_pin1, pigpio.INPUT)
        self.stop = True
        self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
