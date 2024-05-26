# -*- coding: utf-8 -*-
import binascii
import nfc
import time
import sys

# 将来的には、QThreadを使ってGUIでも読み取り中に画面がロックしないようにする。




def led_on(COLOR):
    """
    引数の色に従ってLEDをONにする。

    ////// メモ //////

    ラズパイのGPIO_NUMは、以下の通りとしている。
    RED 16
    BLUE 20
    YELLOW 21
    
    GPIO and the 40-pin headerの仕様は、以下を参照すること。
    https://www.raspberrypi.com/documentation/computers/raspberry-pi.html
    """


    """
    LEDはラズパイにしかないので、plathomeにてMacもしくはラズパイの判定を行って
    処理を分岐している。
    """
    import platform
    osname = platform.system()
    # Macの場合は、コンソールに表示するだけ。
    if osname == 'Darwin':
        if COLOR == 'RED':
            print('RED ON')
        elif COLOR == 'BLUE':
            print('BLUE ON')
        elif COLOR == 'YELLOW':
            print('YELLOW ON')
    # Raspberry Piの場合は、GPIO_NUMを設定してLEDを点灯する。
    elif osname == 'Linux':
        if COLOR == 'RED':
            GPIO_NUM = 16
        elif COLOR == 'BLUE':
            GPIO_NUM = 20
        elif COLOR == 'YELLOW':
            GPIO_NUM = 21

        import pigpio
        pi = pigpio.pi() # local環境
        pi.set_mode(GPIO_NUM, pigpio.OUTPUT)

        try:
            pi.write(GPIO_NUM, 1)
            time.sleep(1.5)
            pi.write(GPIO_NUM, 0)
            pi.set_mode(GPIO_NUM, pigpio.INPUT)
            pi.stop()
        # Macの場合も、エラーをキャッチして実行するようにすると、コードが短くなるかも。
        # エラー前提というのは、少々気持ち悪いけど。
        # except KeyboardInterrupt:  # Ctrl+Cを押すとループを抜ける
        finally:
            pass


def on_connect(tag):
    
    import pandas as pd
    # 照合用のデータは、エクセルで作成
    # 照合用のデータをdfに読み込み
    df = pd.read_excel('data.xlsx', dtype=str)

    # タッチ時の処理
    # フルの情報を引き出す時は、以下のコード。
    #idm = binascii.hexlify(tag._nfcid)
    # IDmのみ取得して表示
    idm = binascii.hexlify(tag.idm).decode()
    idm = str(idm) # 念の為に str にする。
    print("IDm : " + idm) # 照合結果を表示
    
    # 有効期限と、本日を比較を行う
    from datetime import datetime, date, timedelta
    
    # Idmと一致する行を抽出
    print(df[df['Idm'].isin([idm])])
    
    # 日付の比較用に文字列を日付に変換。
    # 日付だけで良いので、dateを使用する。
    s = df[df['Idm'].isin([idm])]['Expiration'].values.tolist()[0]
    s_format = '%Y-%m-%d %H:%M:%S'
    
    # 比較用の有効期限
    expiration_date = datetime.strptime(str(s), s_format).date()

    #print(dt,type(dt))
    from dateutil.relativedelta import relativedelta

    # 6ヶ月後の1日前を求める
    today = date.today()
    after_six_months = today + relativedelta(years=0, months=6, days=-1) # 2019-05-31
    
    

    def discriminate():
        """
        有効期限に従って、表示する色を返す。
        赤：期限切れ
        黄：６ヶ月以内
        青：６ヶ月以上
        """
        if (today > expiration_date):
            return 'RED'
        elif (after_six_months > expiration_date):
            return 'YELLOW'
        else:
            return 'BLUE'

    # 期限を判定し、色を取得
    COLOR = discriminate()
    # 取得した色をled_onへ渡す。
    led_on(COLOR)
    #print(name)
    return True



def read_id():
    # あまり美しくないけど、グローバル変数に。
    # クラス化して実装する方が良さそう。
    global clf
    # USBに接続されたNFCリーダに接続してインスタンス化
    clf = nfc.ContactlessFrontend('usb')
    try:
        # on_connectを呼び出し。呼び出しの間隔、時間は以下の通り。
        # Suica待ち受けの1サイクル秒
        TIME_cycle = 0.5
        # Suica待ち受けの反応インターバル秒
        TIME_interval = 0.2
        clf.connect(rdwr={'on-connect': on_connect}, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)
    finally:
        clf.close()
 
def main():
    # タッチされてから次の待ち受けを開始するまで無効化する秒
    TIME_wait = 1.5
    # アプリ起動時に表示
    print('カードをタッチしてください')

    try:
        while True:
            read_id()
            print('sleep ', TIME_wait, ' seconds')
            time.sleep(TIME_wait)
            print('カードをタッチしてください')
            #end if
    
    # Ctrl-Cで終了できるようにする。
    except KeyboardInterrupt:
        clf.close()
        print(' Catch Ctrl-C. 終了します。')
        sys.exit()

if __name__ == "__main__":
    main()


#end while
