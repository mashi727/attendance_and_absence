import schedule
import threading
from PySide6 import QtCore, QtWidgets, QtGui
import sys
import time


class QEvent_Custom_ShowMessageBox(QtCore.QEvent):
    # QMessageBox を表示するためのカスタムイベント
    custom_type = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())
    def __init__(self) -> None:
        super().__init__(self.custom_type)

class MainWindow(QtWidgets.QWidget):
    # 主ウィンジット
    def __init__(self) -> None:
        super().__init__()
        self.init_widget()
        self.scheduler_thread = Scheduler_Thread(self)

    def init_widget(self) -> None:

        self.setGeometry(500, 300, 400, 270)
        self.setWindowTitle("test")

        button = QtWidgets.QPushButton("close", self)
        button.move(150, 70)
        button.clicked.connect(self.close)

    def event(self, event: QtCore.QEvent) -> bool:
        # カスタムイベントの処理
        if isinstance(event,QEvent_Custom_ShowMessageBox):
            QtWidgets.QMessageBox.information(None, "通知", "インフォメーションです。", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.NoButton)
            return True
        return super().event(event)


class Scheduler_Thread(threading.Thread):
    # 定期的に QMessageBox を表示するためのスレッド
    def __init__(self, main_window: MainWindow) -> None:
        super().__init__(daemon=True)
        self.main_window = main_window
        # schedule.every().day.at("23:00").do(self.alart)
        schedule.every(4).seconds.do(self.alart)
        self.start()

    def alart(self) -> None:
        # QMessageBox を表示するカスタムイベントをポストする
        QtCore.QCoreApplication.postEvent(self.main_window, QEvent_Custom_ShowMessageBox())

    def run(self) -> None:
        while True:
            schedule.run_pending()
            time.sleep(1)

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()

    app.exec()

if __name__ == "__main__" :
    main()
