from jd.api.base import RestApi

class UnionOpenExtraDeliverymanValidateRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.deliverymanReq = None

		def getapiname(self):
			return 'jd.union.open.extra.deliveryman.validate'

		def get_version(self):
			return '1.0'
			
	

class DeliverymanReq(object):
		def __init__(self):
			"""
			"""
			self.unionId = None
			self.mobile = None





