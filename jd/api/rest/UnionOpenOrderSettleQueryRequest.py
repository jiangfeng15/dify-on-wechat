from jd.api.base import RestApi

class UnionOpenOrderSettleQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.OrderSettleReq = None

		def getapiname(self):
			return 'jd.union.open.order.settle.query'

		def get_version(self):
			return '1.0'
			
	

class OrderSettleReq(object):
		def __init__(self):
			"""
			"""
			self.applyId = None
			self.startTime = None
			self.endTime = None
			self.pageIndex = None
			self.pageSize = None





