'''
2021.1.25作成
GPIOコントロールのテストアプリ
【解決済みの課題】
・lineeditから変数に設定
・sleepで画面ロックする件
・
【今後の課題】
・ステータスボタンの実装 -> OK!
・message windowの位置の指定
・プログレスバーの実装
・残時間の表示
・csvのドラッグｎドロップで、グラフ表示
・グラフのｘ軸を時間に
'''
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from LTika_ui2 import *
from PyQt5 import QtTest
import pigpio
import time

'''
2021.1.21現在の設定
hardware_PWM(gpio, PWMfreq, PWMduty)
Frequencies above 30MHz are unlikely to work.
Parameters
    gpio:= see descripton
    PWMfreq:= 0 (off) or 1-125M (1-187.5M for the BCM2711).
    PWMduty:= 0 (off) to 1000000 (1M)(fully on).
'''
gpio_pin0 = 12
gpio_pin1 = 13

# OS固有の設定
# どのPCでも、コードが書けるようにする。
import platform
osname = platform.system()
if osname == 'Darwin':
    pi = pigpio.pi('192.168.1.31')
    FontFamily = 'Arial'
    FontPointNormal = 12
    FontPointMiddle = 18
    FontPointLarge = 24
elif osname == 'Windows':
    FontFamily = 'Arial'
    FontPointNormal = 10
    FontPointMiddle = 12
    FontPointLarge = 18
    pi = pigpio.pi('192.168.1.31')
else:
    FontFamily = 'FreeSerif'
    FontPointNormal = 12
    FontPointMiddle = 18
    FontPointLarge = 24
    pi = pigpio.pi() # local環境
#pi = pigpio.pi() # local環境

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # ここまでは必須
        self.ui.addButton.clicked.connect(self.ledpwm)
        # ウィンドウサイズを固定
        self.setFixedSize(350, 200)
        font = QtGui.QFont()
        font.setFamily(FontFamily)
        font.setPointSize(FontPointNormal)
        font_Middle = QtGui.QFont()
        font_Middle.setFamily(FontFamily)
        font_Middle.setPointSize(FontPointMiddle)
        font_Large = QtGui.QFont()
        font_Large.setFamily(FontFamily)
        font_Large.setPointSize(FontPointLarge)
        font_Large.setBold(True)
        #font_button.setWeight(20)
        self.ui.addButton.setFont(font_Large)
        self.ui.pushButton.setFont(font_Middle)
        self.ui.lineFirstNumber.setFont(font)
        self.ui.labelAddition.setFont(font)
        self.ui.labelFirstNumber.setFont(font)
        self.ui.addButton.setStyleSheet("background-color: #aaff00")
        self.ui.addButton.setText("ON")
        self.ui.pushButton.clicked.connect(self.terminate)

    def parityCheck(self,num):
        range_list = []
        if num %2 != 1:
            range_list = [0,1000000,1000]
            return range_list
        else:
            range_list = [1000000,0,-1000]
            return range_list

    def ledpwm(self,checked):
        a = 1000000
        if checked:
            self.ui.addButton.setStyleSheet("background-color: #ff6767")
            self.stop = False        
            try:
                isinstance(int(self.ui.lineFirstNumber.text()),int)
            except ValueError:
                QMessageBox.warning(None, "Notice!", "数字を入力してください。", QMessageBox.Yes)            
            else:
                a = int(self.ui.lineFirstNumber.text())
                self.ui.labelAddition.setText("PWMDuty: " +str(a))
                pi.set_mode(gpio_pin0, pigpio.OUTPUT)
                pi.set_mode(gpio_pin1, pigpio.OUTPUT)
            try:
                num = 0
                while True:
                    range_list = self.parityCheck(num)
                    if range_list[2] == 1000:
                        self.ui.addButton.setText("OFF")
                    else:
                        self.ui.addButton.setText("")
                    flag = False
                    for i in range(int(range_list[0]*a/1000000),range_list[1],range_list[2]):
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
            except KeyboardInterrupt:
                QMessageBox.warning(None, "Notice!", "Ctrl-Cが押されました。", QMessageBox.Yes)
                pi.set_mode(gpio_pin0, pigpio.INPUT)
                pi.set_mode(gpio_pin1, pigpio.INPUT)
        else:
            self.stopClicked()
            self.ui.addButton.setStyleSheet("background-color: #aaff00")
            self.ui.addButton.setText("ON")

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
