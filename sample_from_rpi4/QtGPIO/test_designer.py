import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pigpio_control import Ui_Dialog
 

import pigpio
import time
pi = pigpio.pi()

# sudo pigpiod

GPIO_NUM = 16
pi.set_mode(GPIO_NUM, pigpio.OUTPUT)

class Test(QDialog):
    def __init__(self,parent=None):
        super(Test, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def slot1(self):
#        self.ui.pushButton_3.setText("OFF")
        try:
            for i in range(10):
                pi.write(GPIO_NUM, 1)
                time.sleep(0.5)
                pi.write(GPIO_NUM, 0)
                time.sleep(0.5)
                i += 1 
        except KeyboardInterrupt:
            pass


    def slot2(self):
            pi.set_mode(GPIO_NUM, pigpio.INPUT)
            pi.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec_())