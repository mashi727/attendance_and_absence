# -*- coding: utf-8 -*-
import binascii
import nfc
import time
import sys
from threading import Thread, Timer

# Suica待ち受けの1サイクル秒
TIME_cycle = 0.5
# Suica待ち受けの反応インターバル秒
TIME_interval = 0.2
# タッチされてから次の待ち受けを開始するまで無効化する秒
TIME_wait = 1.5

# NFC接続リクエストのための準備
# 212F(FeliCa)で設定
#target_req_suica = nfc.clf.RemoteTarget("212F")
# 0003(Suica)
#target_req_suica.sensf_req = bytearray.fromhex("0000030000")





def led_on(COLOR):
    # GPIO_NUM
    # RED 16
    # BLUE 20
    # YELLOW 21
    
    import platform
    osname = platform.system()
    if osname == 'Darwin':
        if COLOR == 'RED':
            print('RED ON')
        elif COLOR == 'BLUE':
            print('BLUE ON')
        elif COLOR == 'YELLOW':
            print('YELLOW ON')

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
        while True:  # 16番ピンのLEDの点灯→消灯を繰り返す
            pi.write(GPIO_NUM, 1)
            time.sleep(1.5)
            pi.write(GPIO_NUM, 0)
    except KeyboardInterrupt:  # Ctrl+Cを押すとループを抜ける
        pass
    # cleanup
    pi.set_mode(GPIO_NUM, pigpio.INPUT)
    pi.stop()



def on_connect(tag):
    
    import pandas as pd
    df = pd.read_excel('data.xlsx', dtype=str)

    #タッチ時の処理
    #IDmのみ取得して表示
    idm = binascii.hexlify(tag.idm).decode()
    idm = str(idm)
    #idm = binascii.hexlify(tag._nfcid)
    print("IDm : " + idm)
    
    from datetime import datetime, date, timedelta
    print(df[df['Idm'].isin([idm])])
    s = df[df['Idm'].isin([idm])]['Expiration'].values.tolist()[0]
    s_format = '%Y-%m-%d %H:%M:%S'
    expiration_date = datetime.strptime(str(s), s_format).date()
    #print(expiration_date)

    #print(dt,type(dt))
    from dateutil.relativedelta import relativedelta

    # 6ヶ月後の1日前を求める
    today = date.today()
    after_six_months = today + relativedelta(years=0, months=6, days=-1) # 2019-05-31
    
    def discriminate():
        if (today > expiration_date):
            return 'RED'
        elif (after_six_months > expiration_date):
            return 'YELLOW'
        else:
            return 'BLUE'

    COLOR = discriminate()
    led_on(COLOR)
    #print(name)
    return True



def read_id():
    global clf
    clf = nfc.ContactlessFrontend('usb')
    try:
        clf.connect(rdwr={'on-connect': on_connect}, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)
    finally:
        clf.close()
 

def main():
    print('カードをタッチしてください')

# USBに接続されたNFCリーダに接続してインスタンス化
    try:
        while True:
            read_id()
            print('sleep ', TIME_wait, ' seconds')
            time.sleep(TIME_wait)
            print('カードをタッチしてください')
            #end if

    except KeyboardInterrupt:
        clf.close()
        print(' Catch Ctrl-C. 終了します。')
        sys.exit()

if __name__ == "__main__":
    main()


#end while
