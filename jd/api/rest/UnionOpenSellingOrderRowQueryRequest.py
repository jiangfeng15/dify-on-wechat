from jd.api.base import RestApi

class UnionOpenSellingOrderRowQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.req = None

		def getapiname(self):
			return 'jd.union.open.selling.order.row.query'

		def get_version(self):
			return '1.0'
			
	

class Req(object):
		def __init__(self):
			"""
			"""
			self.pageIndex = None
			self.pageSize = None
			self.childUnionId = None
			self.key = None
			self.type = None
			self.startTime = None
			self.endTime = None
			self.fields = None
			self.orderId = None





