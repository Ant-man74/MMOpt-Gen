from lxml import etree

class XmlHandler:
	"""
	Static class handling xml files
	"""
	
	treeConfig = None
	paramAlgoGen = {}
	paramMmopt = {}

	"""
	Entry method for the xml config handler
	"""
	@staticmethod
	def loadConfig():
		XmlHandler.initConfigFile()
		XmlHandler.parseConfig()

	"""
	Retrieve the Xml tree of the config file
	"""
	@staticmethod
	def initConfigFile():
		XmlHandler.treeConfig = etree.parse("config.xml")

	"""
	Parse the xml tree of the config file
	"""
	@staticmethod
	def parseConfig():
		for categories in XmlHandler.treeConfig.iter('paramsList'):
			id = categories.get("id")
			for param in categories.iter('param'):
				if( id == "geneticAlgoParams" ) :
					XmlHandler.paramAlgoGen[param.find('name').text] = param.find('value').text
				elif(id == "mmoptParams" ) :
					XmlHandler.paramMmopt[param.find('name').text] = param.find('value').text
			pass
		pass

	"""
	retrieve an entry of the dictionnary,
	catch error if entry or dictionnary not defined
	"""
	@staticmethod
	def getItemFrom(dictionnary, item):
		try:
			if( dictionnary == "algoGen") :
				XmlHandler.paramAlgoGen[item]
			elif ( dictionnary == "mmopt" ) :
				XmlHandler.paramMmopt[item]
			else :
				raise NameError("NameError: Unknown dictionnary")
		except KeyError:
			print ("KeyError: Unknown dictionnary entry")
	
	"""
	Print the two config dictionnaries
	"""
	@staticmethod
	def printConfig():
		print (XmlHandler.paramMmopt)
		print (XmlHandler.paramAlgoGen) 	