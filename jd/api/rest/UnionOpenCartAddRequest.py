from jd.api.base import RestApi

class UnionOpenCartAddRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.addCartReq = None

		def getapiname(self):
			return 'jd.union.open.cart.add'

		def get_version(self):
			return '1.0'
			
	

class AddCartReq(object):
		def __init__(self):
			"""
			"""
			self.xid = None
			self.materialId = None
			self.skuId = None
			self.ip = None
			self.deviceId = None
			self.ua = None
			self.refer = None





