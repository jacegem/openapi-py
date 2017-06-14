"""
작성중인..호출 프로그램
"""

import sys, time
from Kiwoom import Kiwoom, ParameterTypeError, ParameterValueError, KiwoomProcessingError, KiwoomConnectError
from PyQt5.QtWidgets import QApplication
import MySQLdb

if __name__ == "__main__":
    print("START")
    app = QApplication(sys.argv)

    try:

        kiwoom = Kiwoom()
        kiwoom.commConnect()
        # 코스닥과 코스피 종목리스트 가져오기
        stock_list = kiwoom.getCodeList("0")#, "10")[:-1] + kiwoom.getCodeListByMarket(10)[:-1]
        print(stock_list)
        # DB 접속
        kiwoom.conn = MySQLdb.connect(host='localhost', user='pyadmin', password='password', db='pystock', charset='utf8')
        kiwoom.curs = kiwoom.conn.cursor(MySQLdb.cursors.DictCursor)

        for stock in stock_list:
            kiwoom.setInputValue("종목코드", stock)
            kiwoom.setInputValue("기준일자", '20170217')
            kiwoom.setInputValue("수정주가구분", '0')
            kiwoom.commRqData("주식틱차트조회요청", "opt10079", 0, "0612")
            time.sleep(0.3)
            while kiwoom.inquiry == '2':
                kiwoom.setInputValue("종목코드", stock)
                kiwoom.setInputValue("기준일자", '20170217')
                kiwoom.setInputValue("수정주가구분", '0')
                kiwoom.commRqData("주식틱차트조회요청", "opt10079", 2, "0612")
                time.sleep(0.3)
    except Exception as e:
        print(e)

    print("END")

    #sys.exit(app.exec_())