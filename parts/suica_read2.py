# -*- coding: utf-8 -*-
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

print('Suicaをタッチしてください')
# USBに接続されたNFCリーダに接続してインスタンス化
clf = nfc.ContactlessFrontend('usb')
try:
    while True:
        # Suica待ち受け開始
        # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
        target_res = clf.sense(target_req_suica, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)
        #print(type(target_res))
        if target_res is None:
            pass
        else:
            #tag = nfc.tag.tt3.Type3Tag(clf, target_res)
            #なんか仕様変わったっぽい？↓なら動いた
            tag = nfc.tag.activate_tt3(clf, target_res)
            tag.sys = 3

            #IDmを取り出す
            idm = binascii.hexlify(tag.idm).decode()
            print('Suica detected. idm = ', idm)
            clf.close()
            print('終了します!')
            break

        #end if

except KeyboardInterrupt:
    clf.close()
    print(' Catch Ctrl-C. 終了します!')
    sys.exit()

#end while
