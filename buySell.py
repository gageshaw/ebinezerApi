from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from flask import Flask, request

import threading
import time

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
    
    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

app = IBapi()

def run_loop():
    app.run()

#Function to create FX Order contract
def FX_order(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"
    contract.primaryExchange = "NASDAQ"
    return contract

def order( action, stock, quantity, lmtPrice):
    app.connect('127.0.0.1', 7497, 123)

    app.nextorderId = None

    #Start the socket in a thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    #Check if the API is connected via orderid
    while True:
        if isinstance(app.nextorderId, int):
            print('connected')
            break
        else:
            print('waiting for connection')
            time.sleep(1)

    #Create order object
    order = Order()
    order.action = action
    order.totalQuantity = quantity
    order.orderType = 'LMT'
    order.lmtPrice = lmtPrice
    order.tif = 'DAY'
    order.eTradeOnly = ''
    order.firmQuoteOnly = ''

    #Place order
    app.placeOrder(app.nextorderId, FX_order(stock), order)
    #app.nextorderId += 1

    time.sleep(3)
    app.disconnect()



def buy(stock, quantity, lmtPrice):
   order('BUY',stock ,quantity, lmtPrice)
    
def sell(stock, quantity, lmtPrice):
   order('SELL',stock ,quantity, lmtPrice)
    
fApp = Flask(__name__)

@fApp.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        if request.json["action"] == "BUY":
            buy(request.json["symbol"],request.json["quantity"] ,request.json["limit"] )
            return "bought... probably"
        elif request.json["action"] == "SELL":
            sell(request.json["symbol"],request.json["quantity"] ,request.json["limit"] )
            return "sold... probably"
        
    return "invalid request"
    	

fApp.run(host='0.0.0.0',port=80)