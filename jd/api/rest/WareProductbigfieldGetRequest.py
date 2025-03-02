from jd.api.base import RestApi

class WareProductbigfieldGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.wid = None
			self.fields = None

		def getapiname(self):
			return 'jingdong.ware.productbigfield.get'

		def get_version(self):
			return '1.0'
			
	




