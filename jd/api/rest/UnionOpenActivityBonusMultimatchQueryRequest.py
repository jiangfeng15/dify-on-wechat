from jd.api.base import RestApi

class UnionOpenActivityBonusMultimatchQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.batchUserMatchActivityRequest = None

		def getapiname(self):
			return 'jd.union.open.activity.bonus.multimatch.query'

		def get_version(self):
			return '1.0'
			
	

class BatchUserMatchActivityRequest(object):
		def __init__(self):
			"""
			"""
			self.userIdType = None
			self.userIds = None





