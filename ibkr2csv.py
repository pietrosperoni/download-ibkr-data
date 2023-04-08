import csv
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import BarData
from threading import Thread, Event
from datetime import datetime


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.options_data = []
        self.options_data_event = Event()
        self.market_data = {}
        self.market_data_event = Event()    

    #def contractDetails(self, reqId, contractDetails):
    #    option = contractDetails.contract
    #    self.options_data.append([option.symbol, option.lastTradeDateOrContractMonth, option.strike, option.right])
    #    print(f"Opzione: {option.symbol}, Data: {option.lastTradeDateOrContractMonth}, Strike: {option.strike}, Tipo: {option.right}")

    def contractDetails(self, reqId: int, contractDetails):
        option = contractDetails.contract
        self.options_data.append(option)

    def contractDetailsEnd(self, reqId: int):
        self.options_data_event.set()

    def tickPrice(self, reqId: int, tickType, price, attrib):
        if tickType in [1, 2, 9]:  # 1: Bid, 2: Ask, 4: Last, 6: High, 7: Low, 9: Close
            if price != -1:
                self.market_data[reqId] = price
                self.market_data_event.set()
    
    def error(self, reqId: int, errorCode: int, errorString: str):
        if errorCode in [200, 354]:  # 200: No security definition has been found, 354: Requested market data is not subscribed
            self.market_data[reqId] = None
            self.market_data_event.set()


def main():
    app = IBapi()
    app.connect('127.0.0.1', 7496, 0)
    api_thread = Thread(target=app.run)
    api_thread.start()

    contract = Contract()
    contract.symbol = "AMZN"
    contract.secType = "OPT"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.lastTradeDateOrContractMonth = "20240119"

    app.reqContractDetails(1, contract)
    app.options_data_event.wait()

    options_data_with_price = []
    for idx, option in enumerate(app.options_data):
        #app.reqMktData(idx + 1000, option, "9", False, False, [])
        app.reqMktData(idx + 1000, option, "", False, False, [])
        app.market_data_event.wait(timeout=5)
        app.cancelMktData(idx + 1000)
        app.market_data_event.clear()
        price = app.market_data.get(idx + 1000, None)
        if price is not None:
            options_data_with_price.append([option.symbol, option.lastTradeDateOrContractMonth, option.strike, option.right, price])
            print(f"Opzione: {option.symbol}, Data: {option.lastTradeDateOrContractMonth}, Strike: {option.strike}, Tipo: {option.right}, Prezzo: {price}")


    app.disconnect()
    api_thread.join()

    # with open("options_data.csv", "w", newline="") as csvfile:
    #     csv_writer = csv.writer(csvfile)
    #     csv_writer.writerow(["Symbol", "Expiry", "Strike", "Type", "Price"])
    #     csv_writer.writerows(options_data_with_price)
    call_options_data = []
    put_options_data = []

    for data in options_data_with_price:
        if data[3] == "C":
            call_options_data.append(data)
        elif data[3] == "P":
            put_options_data.append(data)

    call_options_data.sort(key=lambda x: x[2])
    put_options_data.sort(key=lambda x: x[2])

    ticker = "AMZN"
    expiration_date = "20240119"
    write_to_csv(f"{ticker}_{expiration_date}_CALL.csv", call_options_data)
    write_to_csv(f"{ticker}_{expiration_date}_PUT.csv", put_options_data)
    write_to_csv("CALL.csv", call_options_data)
    write_to_csv("PUT.csv", put_options_data)

    app.disconnect()
    api_thread.join()

def write_to_csv(file_name, data):
    with open(file_name, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Symbol", "Expiry", "Strike", "Type", "Price"])
        csv_writer.writerows(data)

if __name__ == "__main__":
    main()
