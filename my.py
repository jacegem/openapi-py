"""
작성중인..호출 프로그램
"""

import sys, time
from Kiwoom import *
from PyQt5.QtWidgets import QApplication
import MySQLdb
import datetime

ACTION = ["주식일봉차트조회요청"]
TODAY = '20170626'
if __name__ == '__main__':
    print("START")
    app = QApplication(sys.argv)

    try:
        kiwoom = Kiwoom()
        kiwoom.commConnect()
        # 코스피 종목리스트 가져오기
        stock_list = kiwoom.getCodeList("0")
        print(len(stock_list))
        # DB 접속
        conn = MySQLdb.connect(host='localhost', user='pyadmin', password='password', db='pystock', charset='utf8')
        curs = conn.cursor()
        if "주식기본정보요청" in ACTION: #opt10001
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
        if "업종별주가요청" in ACTION: #OPT20002
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
                curs.execute("select 일자 from opt10081 where 종목코드=%s and 일자=%s", (stock, TODAY))
                if curs.fetchall():
                    continue
                kiwoom.setInputValue("종목코드", stock)
                kiwoom.setInputValue("기준일자", TODAY)
                kiwoom.setInputValue("수정주가구분", '0')
                kiwoom.commRqData("주식일봉차트조회요청", "OPT10081", 0, "0615")
                for cnt in kiwoom.data:
                    curs.execute("""replace into opt10081
                                  (종목코드, 현재가, 거래량, 거래대금, 일자,
                                  시가, 고가, 저가, 수정주가구분, 수정비율,
                                  대업종구분, 소업종구분, 종목정보, 수정주가이벤트, 전일종가) values
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
                                      (종목코드, 현재가, 거래량, 거래대금, 일자,
                                      시가, 고가, 저가, 수정주가구분, 수정비율,
                                      대업종구분, 소업종구분, 종목정보, 수정주가이벤트, 전일종가) values
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
    finally:
        conn.close()

    print("END")

    sys.exit(app.exec_())