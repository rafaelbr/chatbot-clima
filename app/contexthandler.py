class ContextHandler(object):
	class __ContextHandler:
		def __init__(self):
			self.contextmap = {}
	
	instance = None
	
	def __new__(cls):
		if not ContextHandler.instance:
			ContextHandler.instance = ContextHandler.__ContextHandler()
		return ContextHandler.instance
		
	def __getattr__(self, name):
		return getattr(self.instance, name)
	
	def __setattr__(self, name):
		return setattr(self.instance, name)
		