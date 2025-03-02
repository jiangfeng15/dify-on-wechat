from jd.api.base import RestApi

class UnionOpenActivityBonusMatchQueryRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.userMatchActivityRequest = None

		def getapiname(self):
			return 'jd.union.open.activity.bonus.match.query'

		def get_version(self):
			return '1.0'
			
	

class UserMatchActivityRequest(object):
		def __init__(self):
			"""
			"""
			self.userIdType = None
			self.userId = None





