"""
작성중인..호출 프로그램
"""

import sys, time
from Kiwoom import *
from PyQt5.QtWidgets import QApplication
import MySQLdb

if __name__ == '__main__':
    print("START")
    app = QApplication(sys.argv)

    try:

        kiwoom = Kiwoom()
        kiwoom.commConnect()
        # 코스피 종목리스트 가져오기
        stock_list = kiwoom.getCodeList("0")
        print(stock_list)
        # DB 접속
        conn = MySQLdb.connect(host='localhost', user='pyadmin', password='password', db='pystock', charset='utf8')
        curs = conn.cursor()

        # opt10079
        # for stock in stock_list:
        #     kiwoom.setInputValue("종목코드", stock)
        #     kiwoom.setInputValue("틱범위", 1)
        #     kiwoom.setInputValue("수정주가구분", '0')
        #     kiwoom.commRqData("주식틱차트조회요청", "opt10079", 0, "0615")
        #     time.sleep(0.3)
        #     while kiwoom.inquiry == '2':
        #         kiwoom.setInputValue("종목코드", stock)
        #         kiwoom.setInputValue("틱범위", 1)
        #         kiwoom.setInputValue("수정주가구분", '0')
        #         kiwoom.commRqData("주식틱차트조회요청", "opt10079", 2, "0615")
        #         time.sleep(0.3)

        # opt10081
        for stock in stock_list:
            kiwoom.setInputValue("종목코드", stock)
            kiwoom.setInputValue("기준일자", '20170217')
            kiwoom.setInputValue("수정주가구분", '0')
            kiwoom.commRqData("주식일봉차트조회요청", "OPT10081", 0, "0615")
            for cnt in kiwoom.data:
                curs.execute("""insert into opt10081
                              (종목코드, 현재가, 거래량, 거래대금, 일자,
                              시가, 고가, 저가, 수정주가구분, 수정비율,
                              대업종구분, 소업종구분, 종목정보, 수정주가이벤트, 전일종가) values
                              (%s, %s, %s, %s, %s,
                               %s, %s, %s, %s, %s,
                               %s, %s, %s, %s, %s)
                              """, (stock, cnt[1], cnt[2], cnt[3], cnt[4],
                                    cnt[5], cnt[6], cnt[7], cnt[8], cnt[9],
                                    cnt[10], cnt[11], cnt[12], cnt[13], cnt[14]))
            conn.commit()
            time.sleep(0.5)
            while kiwoom.inquiry == '2':
                kiwoom.setInputValue("종목코드", stock)
                kiwoom.setInputValue("기준일자", '20170217')
                kiwoom.setInputValue("수정주가구분", '0')
                kiwoom.commRqData("주식일봉차트조회요청", "OPT10081", 2, "0615")
                for cnt in kiwoom.data:
                    curs.execute("""insert into opt10081
                                  (종목코드, 현재가, 거래량, 거래대금, 일자,
                                  시가, 고가, 저가, 수정주가구분, 수정비율,
                                  대업종구분, 소업종구분, 종목정보, 수정주가이벤트, 전일종가) values
                                  (%s, %s, %s, %s, %s,
                                   %s, %s, %s, %s, %s,
                                   %s, %s, %s, %s, %s)
                                  """, (stock, cnt[1], cnt[2], cnt[3], cnt[4],
                                        cnt[5], cnt[6], cnt[7], cnt[8], cnt[9],
                                        cnt[10], cnt[11], cnt[12], cnt[13], cnt[14]))
                conn.commit()
                time.sleep(0.5)

    except Exception as e:
        print(e)

    print("END")

    sys.exit(app.exec_())