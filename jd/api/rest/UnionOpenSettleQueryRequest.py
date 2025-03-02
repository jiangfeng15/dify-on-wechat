from jd.api.base import RestApi

class UnionOpenSettleQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.payMonth = None

		def getapiname(self):
			return 'jd.union.open.settle.query'

		def get_version(self):
			return '1.0'
			
	




