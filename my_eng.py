# coding=utf-8
"""
작성중인..호출 프로그램
"""

import time
from Kiwoom import *

import MySQLdb
# import datetime

'''Python2'''
from PyQt4.QtGui import QApplication
'''Python3'''
#from PyQt5.QtWidgets import QApplication


ACTION = ["주식일봉차트조회요청"]
TODAY = '20170626'
TARGET = ["코스피"]
if __name__ == '__main__':
    print("START")
    app = QApplication(sys.argv)

    try:
        kiwoom = Kiwoom()
        kiwoom.commConnect()
        # 코스피 종목리스트 가져오기
        if '코스피' in TARGET:
            stock_list = kiwoom.getCodeList("0")[:-1]
        elif '코스닥' in TARGET:
            stock_list = kiwoom.getCodeList("10")[:-1]
        elif '코스피,코스닥' in TARGET:
            stock_list = kiwoom.getCodeList("0")[:-1] + kiwoom.getCodeList("10")[:-1]
        else:
            sys.exit(app.exec_())

        print(stock_list)
        print(len(stock_list))
        # DB 접속
        conn = MySQLdb.connect(host='localhost', user='pyadmin', password='password', db='pystock', charset='utf8', port=3390)
        curs = conn.cursor()
        if "주식기본정보요청" in ACTION:  # opt10001
            for stock in stock_list:
                print(stock)
                kiwoom.setInputValue("종목코드", stock)
                kiwoom.commRqData("주식기본정보요청", "OPT10001", 0, "0291")
                for cnt in kiwoom.data:
                    curs.execute("""replace into opt10079
                                  (종목코드, 현재가, 거래량, 체결시간, 시가,
                                  고가, 저가, 수정주가구분, 수정비율, 대업종구분,
                                  소업종구분, 종목정보, 수정주가이벤트, 전일종가) values
                                  (%s, %s, %s, %s, %s,
                                   %s, %s, %s, %s, %s,
                                   %s, %s, %s, %s)
                                  """, (stock, cnt[1], cnt[2], cnt[3], cnt[4],
                                        cnt[5], cnt[6], cnt[7], cnt[8], cnt[9],
                                        cnt[10], cnt[11], cnt[12], cnt[13]))
                time.sleep(0.5)
        if "업종별투자자순매수요청" in ACTION: #opt10051
            pass
        if "업종별주가요청" in ACTION:  # OPT20002
            pass
        if "주식틱차트조회요청" in ACTION:
            for stock in stock_list:
                print(stock)
                curs.execute("select * from opt10079 where 종목코드=%s and 일자=%s", (stock, TODAY))
                if curs.fetchall():
                    continue
                kiwoom.setInputValue("종목코드", stock)
                kiwoom.setInputValue("틱범위", 1)
                kiwoom.setInputValue("수정주가구분", '0')
                kiwoom.commRqData("주식틱차트조회요청", "OPT10079", 0, "0615")
                for cnt in kiwoom.data:
                    curs.execute("""replace into opt10079
                                  (종목코드, 현재가, 거래량, 체결시간, 시가,
                                  고가, 저가, 수정주가구분, 수정비율, 대업종구분,
                                  소업종구분, 종목정보, 수정주가이벤트, 전일종가) values
                                  (%s, %s, %s, %s, %s,
                                   %s, %s, %s, %s, %s,
                                   %s, %s, %s, %s)
                                  """, (stock, cnt[1], cnt[2], cnt[3], cnt[4],
                                        cnt[5], cnt[6], cnt[7], cnt[8], cnt[9],
                                        cnt[10], cnt[11], cnt[12], cnt[13]))
                time.sleep(0.5)
                while kiwoom.inquiry == '2':
                    kiwoom.setInputValue("종목코드", stock)
                    kiwoom.setInputValue("틱범위", 1)
                    kiwoom.setInputValue("수정주가구분", '0')
                    kiwoom.commRqData("주식틱차트조회요청", "OPT10079", 0, "0615")
                    for cnt in kiwoom.data:
                        curs.execute("""replace into opt10079
                                      (종목코드, 현재가, 거래량, 체결시간, 시가,
                                      고가, 저가, 수정주가구분, 수정비율, 대업종구분,
                                      소업종구분, 종목정보, 수정주가이벤트, 전일종가) values
                                      (%s, %s, %s, %s, %s,
                                       %s, %s, %s, %s, %s,
                                       %s, %s, %s, %s)
                                      """, (stock, cnt[1], cnt[2], cnt[3], cnt[4],
                                            cnt[5], cnt[6], cnt[7], cnt[8], cnt[9],
                                            cnt[10], cnt[11], cnt[12], cnt[13]))
                    time.sleep(0.5)
                conn.commit()
        if "주식일봉차트조회요청" in ACTION:
            # opt10081
            for stock in stock_list:
                print(stock)
                curs.execute("select date from opt10081 where symbol=%s and date=%s", (stock, TODAY))
                if curs.fetchall():
                    continue
                kiwoom.setInputValue("종목코드", stock)
                kiwoom.setInputValue("기준일자", TODAY)
                kiwoom.setInputValue("수정주가구분", '0')
                kiwoom.commRqData("주식일봉차트조회요청", "OPT10081", 0, "0615")
                for cnt in kiwoom.data:
                    curs.execute("""replace into opt10081
                              (symbol, close, volume, volume_price, date,
                              open, high, low, modify_gubun, modify_ratio,
                              big_gubun, small_gubun, symbol_inform, modify_event, before_close) values
                                  (%s, %s, %s, %s, %s,
                                   %s, %s, %s, %s, %s,
                                   %s, %s, %s, %s, %s)
                                  """, (stock, cnt[1], cnt[2], cnt[3], cnt[4],
                                        cnt[5], cnt[6], cnt[7], cnt[8], cnt[9],
                                        cnt[10], cnt[11], cnt[12], cnt[13], cnt[14]))
                time.sleep(0.5)
                while kiwoom.inquiry == '2':
                    kiwoom.setInputValue("종목코드", stock)
                    kiwoom.setInputValue("기준일자", TODAY)
                    kiwoom.setInputValue("수정주가구분", '0')
                    kiwoom.commRqData("주식일봉차트조회요청", "OPT10081", 2, "0615")
                    for cnt in kiwoom.data:
                        curs.execute("""replace into opt10081
                                  (symbol, close, volume, volume_price, date,
                                  open, high, low, modify_gubun, modify_ratio,
                                  big_gubun, small_gubun, symbol_inform, modify_event, before_close) values
                                      (%s, %s, %s, %s, %s,
                                       %s, %s, %s, %s, %s,
                                       %s, %s, %s, %s, %s)
                                      """, (stock, cnt[1], cnt[2], cnt[3], cnt[4],
                                            cnt[5], cnt[6], cnt[7], cnt[8], cnt[9],
                                            cnt[10], cnt[11], cnt[12], cnt[13], cnt[14]))
                    time.sleep(0.5)
                conn.commit()

    except Exception as e:
        print(e)

    print("END")

    sys.exit(app.exec_())
