from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

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
	contract.symbol = symbol[:3]
	contract.secType = 'CASH'
	contract.exchange = 'IDEALPRO'
	contract.currency = symbol[3:]
	return contract

def order( action, stock, totalQuantity, lmtPrice):
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
    order.totalQuantity = totalQuantity
    order.orderType = 'LMT'
    order.lmtPrice = lmtPrice

    #Place order
    app.placeOrder(app.nextorderId, FX_order(stock), order)
    #app.nextorderId += 1

    time.sleep(3)
    app.disconnect()

def buy(stock, totalQuantity, lmtPrice):
	order('BUY',stock ,totalQuantity, lmtPrice)
	
def sell(stock, totalQuantity, lmtPrice):
	order('SELL',stock ,totalQuantity, lmtPrice)
	
buy('EURUSD', 10,1.1)
sell('EURUSD', 10,1.1)