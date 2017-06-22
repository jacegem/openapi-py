"""
작성중인..호출 프로그램
"""

import sys, time
from Kiwoom import *
from PyQt5.QtWidgets import QApplication
import sqlalchemy
import pandas

if __name__ == "__main__":
    print("START")
    app = QApplication(sys.argv)

    try:

        kiwoom = Kiwoom()
        kiwoom.commConnect()
        # 코스피 종목리스트 가져오기
        stock_list = kiwoom.getCodeList("0")
        print(stock_list)
        # DB 접속
        engine = sqlalchemy.create_engine('mysql://pyadmin:password@localhost/pystock')

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
            kiwoom.commRqData("주식일봉차트조회요청", "opt10081", 0, "0615")
            kiwoom.data.to_sql(con=kiwoom.conn, name='opt10081', if_exists='fail')
            time.sleep(0.3)
            while kiwoom.inquiry == '2':
                kiwoom.setInputValue("종목코드", stock)
                kiwoom.setInputValue("기준일자", '20170217')
                kiwoom.setInputValue("수정주가구분", '0')
                kiwoom.commRqData("주식일봉차트조회요청", "opt10081", 2, "0615")
                kiwoom.data.to_sql(con=kiwoom.conn, name='opt10081', if_exists='fail')
                time.sleep(0.3)
    except Exception as e:
        print(e)

    print("END")

    sys.exit(app.exec_())