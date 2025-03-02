from jd.api.base import RestApi

class UnionOpenStatisticsGoodsSalesQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.effectDataReq = None

		def getapiname(self):
			return 'jd.union.open.statistics.goods.sales.query'

		def get_version(self):
			return '1.0'
			
	

class EffectDataReq(object):
		def __init__(self):
			"""
			"""
			self.skuIds = None
			self.type = None
			self.number = None





