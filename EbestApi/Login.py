# -*-coding: utf-8 -*-

import win32com.client
import pythoncom
import sys


class XASessionEvents:
    logInState = 0

    def OnLogin(self, code, msg):
        print("onLogin method is called")
        print(str(code))
        print(str(msg))

        # 0000이 입력될 때만 로그인 성공
        if str(code) == '0000':
            XASessionEvents.logInState = 1

    def OnLogout(self):
        print("OnLogout method is called")

    def OnDisconnect(self):
        print("OnDisconnect method is called")

    def ProcLogin(self):
        server_addr = 'hts.ebestsec.co.kr'
        server_port = 200001
        server_type = 0
        user_id = input("아이디: ")
        user_pass = input("비밀번호: ")
        user_cert = input("공인인증서 비밀번호: ")

        self = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents)
        bConnect = self.ConnectServer(server_addr, server_port)

        if not bConnect:
        # 로그인 실패
            nErrCode = self.GetLastError()
            strErrMsg = self.GetErrorMessage(nErrCode)
            print(strErrMsg)
            sys.exit(0)

        # 로그인 성공

        self.Login(user_id, user_pass, user_cert, server_type, 0)

        while XASessionEvents.logInState == 0:
            pythoncom.PumpWaitingMessages()

        # 계좌정보 불러오기
        nCount = self.GetAccountListCount()
        for i in range(nCount):
            print("Account : %d - %s" % (i, self.GetAccountList(i)))




if __name__ == "__main__":
    inXASession = XASessionEvents()
    inXASession.ProcLogin()