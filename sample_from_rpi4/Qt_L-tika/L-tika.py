# _*_ coding: utf-8 _*_
import pigpio
import time
pi = pigpio.pi()

# sudo pigpiod

GPIO_NUM = 12

pi.set_mode(GPIO_NUM, pigpio.OUTPUT)
try:
    while True:  # 16番ピンのLEDの点灯→消灯を繰り返す
        pi.write(GPIO_NUM, 1)
        time.sleep(5)
        pi.write(GPIO_NUM, 0)
        time.sleep(0.5)
except KeyboardInterrupt:  # Ctrl+Cを押すとループを抜ける
    pass
# cleanup
pi.set_mode(GPIO_NUM, pigpio.INPUT)
pi.stop()
