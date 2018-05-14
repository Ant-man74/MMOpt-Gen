
import os

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
	def __init__ (self):
		self.initConfigFile()
		self.parseConfig()

	"""
	Retrieve the Xml tree of the config file
	"""
	def initConfigFile(self):
		XmlHandler.treeConfig = etree.parse(os.path.dirname(os.path.abspath(__file__))+"/config.xml")

	"""
	Parse the xml tree of the config file
	"""
	def parseConfig(self):
		for categories in self.treeConfig.iter('paramsList'):
			id = categories.get("id")
			for param in categories.iter('param'):
				if( id == "algoGen" ) :
					XmlHandler.paramAlgoGen[param.find('name').text] = param.find('value').text
				elif(id == "mmopt" ) :
					XmlHandler.paramMmopt[param.find('name').text] = param.find('value').text
			pass
		pass

	"""
	retrieve an entry of the dictionnary,
	catch error if entry or dictionnary not defined
	"""
	@staticmethod
	def getItemFrom(dictionnary, item):
		ret = 0
		try:
			if( dictionnary == "algoGen") :
				ret = XmlHandler.paramAlgoGen[item]
			elif ( dictionnary == "mmopt" ) :
				ret = XmlHandler.paramMmopt[item]
			else :
				raise NameError("NameError: Unknown dictionnary")
			return ret
		except KeyError:
			print ("KeyError: Unknown dictionnary entry")
	
	"""
	Print the two config dictionnaries
	"""
	@staticmethod
	def printConfig():
		print (XmlHandler.paramMmopt)
		print (XmlHandler.paramAlgoGen) 	