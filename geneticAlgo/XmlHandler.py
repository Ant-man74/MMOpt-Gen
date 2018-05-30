
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
				if id == "algoGen":
					if param.find('value').text.find(";") == -1:
						XmlHandler.paramAlgoGen[param.find('name').text] = param.find('value').text
					else:
						XmlHandler.paramAlgoGen[param.find('name').text] = param.find('value').text.split(";")
				elif id == "mmopt":
					if param.find('value').text.find(";") == -1:
						XmlHandler.paramMmopt[param.find('name').text] = param.find('value').text
					else:
						XmlHandler.paramMmopt[param.find('name').text] = param.find('value').text.split(";")
		pass

	"""
	retrieve an entry of the dictionnary,
	catch error if entry or dictionnary not defined
	"""
	@staticmethod
	def getItemFrom(dictionnary, item):
		ret = 0
		try:
			if dictionnary == "algoGen":
				ret = XmlHandler.paramAlgoGen[item]
			elif dictionnary == "mmopt":
				ret = XmlHandler.paramMmopt[item]
			else :
				raise NameError("NameError: Unknown dictionnary")
			return ret
		except KeyError:
			print ("KeyError: Unknown dictionnary entry")
	
	"""
	set an entry of the dictionnary, the item must already be known (input a blank value in the XML config file in order to make it available)
	"""
	@staticmethod
	def setItemIn(dictionnary, item, value):

		try:
			if dictionnary == "algoGen":
				XmlHandler.paramAlgoGen[item] = value
			elif dictionnary == "mmopt":
				XmlHandler.paramMmopt[item] = value
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

