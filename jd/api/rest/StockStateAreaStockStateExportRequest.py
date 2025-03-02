from jd.api.base import RestApi

class StockStateAreaStockStateExportRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.CallerParam = None
			self.AreaStockStateSpuGlobalParam = None

		def getapiname(self):
			return 'jingdong.stock.state.areaStockStateExport'

			
	

class CallerParam(object):
		def __init__(self):
			"""
			"""
			self.buId = None
			self.useDefaultTenant = None
			self.timezone = None
			self.nationId = None
			self.skuTenant = None
			self.sysIp = None
			self.language = None
			self.tenantId = None
			self.CallerParamextMap = None


class SkuNumParam(object):
		def __init__(self):
			"""
			"""
			self.num = None
			self.skuId = None


class AreaParam(object):
		def __init__(self):
			"""
			"""
			self.stateId = None
			self.provinceId = None
			self.cityId = None
			self.countyId = None
			self.townId = None


class CoordnateParam(object):
		def __init__(self):
			"""
			"""
			self.longtitude = None
			self.latitude = None
			self.coordType = None


class AreaStockStateSpuGlobalParam(object):
		def __init__(self):
			"""
			"""
			self.skuNumList = None
			self.channelId = None
			self.areaParam = None
			self.coordnateParam = None
			self.AreaStockStateSpuGlobalParamextMap = None





