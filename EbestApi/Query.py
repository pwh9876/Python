
import win32com.client
import pythoncom
import Login as login

class XAQueryEvent :
    query_state = 0

    def OnReceiveData(self, code):
        XAQueryEvent.query_state = 1

    def ProcT1102(self):
        self = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvent)
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1102.res"
        self.SetFieldData("t1102InBlock", "shcode", 0, "078020")
        self.Request(0)

        while XAQueryEvent.query_state == 0:
            pythoncom.PumpWaitingMessages()

        name = self.GetFieldData("t1102OutBlock", "hname", 0)
        price = self.GetFieldData("t1102OutBlock", "price", 0)

        print(name)
        print(price)


if __name__ == "__main__":
    inXASession = login.XASessionEvents()
    inXASession.ProcLogin()

    inXAQuery = XAQueryEvent()
    inXAQuery.ProcT1102()

