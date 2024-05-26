import sys, threading
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QObject, QThread, Signal, Slot
import shiboken6
import time

class Worker(QObject):
    """バックグラウンドで処理を行うクラス
    """

    countup = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__is_canceled = False

    def run(self):
        print(f'worker started, thread_id={threading.get_ident()}')
        count = 0
        while not self.__is_canceled:
            count += 1
            self.countup.emit(count)
            time.sleep(0.001)
        print(f'worker finished, thread_id={threading.get_ident()}')

    def stop(self):
        self.__is_canceled = True

class MainWindow(QWidget):
    """メインウィンドウ
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__thread = None

        layout = QVBoxLayout()
        button = QPushButton('Start')
        button.clicked.connect(self.__start)
        layout.addWidget(button)
        button = QPushButton('Stop')
        button.clicked.connect(self.__stop)
        layout.addWidget(button)
        self.__label = QLabel()
        layout.addWidget(self.__label)
        self.setLayout(layout)

    def __start(self):
        """開始
        """
        print(f'start, thread_id={threading.get_ident()}')
        self.__stop()

        self.__thread = QThread()
        self.__worker = Worker()
        self.__worker.moveToThread(self.__thread) # 別スレッドで処理を実行する
        # シグナルスロットの接続（self.__countup をスレッド側で実行させるために Qt.DirectConnection を指定）
        self.__worker.countup.connect(self.__countup, type=Qt.DirectConnection)
        # スレッドが開始されたら worker の処理を開始する
        self.__thread.started.connect(self.__worker.run)
        # ラムダ式を使う場合は Qt.DirectConnection を指定
        #self.__thread.started.connect(lambda: self.__worker.run(), type=Qt.DirectConnection) 
        # スレッドが終了したら破棄する
        self.__thread.finished.connect(self.__worker.deleteLater)
        self.__thread.finished.connect(self.__thread.deleteLater)

        # 処理開始
        self.__thread.start()

    def __stop(self):
        """停止
        """
        print(f'stop, thread_id={threading.get_ident()}')
        if self.__thread and shiboken6.isValid(self.__thread):
            # スレッドが作成されていて、削除されていない
            if self.__thread.isRunning() or not self.__thread.isFinished():
                print('thread is stopping')
                self.__worker.stop()
                self.__thread.quit()
                self.__thread.wait()
                print('thread is stopped')

    def __countup(self, count):
        """countup シグナルに対する処理
        """
        self.__label.setText(f'count={count}, thread_id={threading.get_ident()}')

    def closeEvent(self, event):
        """closeEvent のオーバーライド（ウィンドウを閉じたときにスレッドを終了させる）
        """
        self.__stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
