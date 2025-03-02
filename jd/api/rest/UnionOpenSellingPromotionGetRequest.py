from jd.api.base import RestApi

class UnionOpenSellingPromotionGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.req = None

		def getapiname(self):
			return 'jd.union.open.selling.promotion.get'

		def get_version(self):
			return '1.0'
			
	

class Req(object):
		def __init__(self):
			"""
			"""
			self.materialId = None
			self.siteId = None
			self.chainType = None
			self.couponUrl = None
			self.positionId = None
			self.subUnionId = None
			self.ext1 = None
			self.pid = None
			self.unionId = None





