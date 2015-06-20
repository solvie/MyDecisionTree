#***************************************************************************************************************#
#	THIS IS A DECISION TREE ADAPTATION BASED ON THE ID3 ALGORITHM						#
#  														#
#	Solvie Lee/ 2015											#
#	This algorithm only deals with a specific dataset of binary values but later it should be modified	#
#	such that it can take as input any dataset with binary attribute value pairs				#
#														#
#***************************************************************************************************************#

import csv
import numpy as np
import sys

##------------CLASSES------------##

#TODO:we make a new datapoint for each line in a csv file, pretty much. 
class Datapoint:
	"""
	A Datapoint should take as input a list of attributes and their corresponding values.	

	The hipster vs hobo thing is a placeholder for now; consider making it flexible so that
	attribute value pairs can be changed

	"""
	def __init__(self, values):
		self.holeInJeansAuthentic = int(values[0])
		self.dreadlocks = int(values[1])
		self.coffeeCupEmpty = int(values[2])
		self.smartPhone = int(values[3])
		self.hoboOrHippie = int(values[4])
		self.asvalues = values
	
	def read(self):
		print "[", str(self.holeInJeansAuthentic), str(self.dreadlocks), str(self.coffeeCupEmpty), str(self.smartPhone), str(self.hoboOrHippie), "]"
	
	def getAttributeValue(self, i):
		if i ==1:
			return self.holeInJeansAuthentic
		elif i ==2:
			return self.dreadlocks
		elif i ==3:
			return self.coffeeCupEmpty
		elif i ==4:
			return self.smartPhone
		else: 
			return None	
			print "invalid attribute number"
			
#TODO
class Node:
	"""
	The tree is built up of nodes. If the attribute_no is 0, that means it is a leaf. 
	
	Attribute key: 1=holeInJeansAuthentic, 2=dreadlocks, 3=coffeeCupEmpty, 4=smartPhone
 
	"""

	def __init__(self, attribute_no = 0):
		self.children = []
		self.numAncestors = 0
		self.attribute = attribute_no	 #integer code
		self.parent = None
		self.leaf = None
		self.stem = None

	def addChild(self, node):
		self.children.append(node)
		node.setParent(self)

	def setParent(self, node):
		self.parent = node
	
	def getNumAncestors(self):
		self.numAncestors = 0
		ancestor = self.parent
		while  ancestor != None:
			self.numAncestors = self.numAncestors +1
			ancestor = ancestor.parent
		return self.numAncestors
	
	def toString(self):
		print "[ Attribute "+ str(self.attribute) + " ]"		

	# A node should have a parent and a list of children. 


##---------------HELPER METHODS---------------##

#Here be careful so that the right column corresponds to the right attribute.
def csvToDatapointList(filename):
	alist = []
	filepath = './'+filename
	with open(filepath, 'rU') as csvfile:
		datareader = csv.reader(csvfile, delimiter= ',')
		datareader.next()
		for row in datareader:
			datapoint = Datapoint([row[0],row[1],row[2],row[3],row[4]])
			alist.append(datapoint)
	return alist	


def getS(datapoint_list, optional_attribute=0):
	plus = 0
	minus = 0
	sValue = []
	if optional_attribute ==0:
		for point in datapoint_list:
			if int(point.hoboOrHippie) == 1:
				plus = plus + 1
			elif int(point.hoboOrHippie) == 0:
				minus = minus + 1
			else: print "something wrong with this value yo"
	else:
		for point in datapoint_list:
			if int(point.hoboOrHippie) ==1 and int(point.getAttributeValue(optional_attribute))==1:
				plus = plus +1
			elif int(point.hoboOrHippie)==0 and int(point.getAttributeValue(optional_attribute))==1:
				minus = minus + 1

	sValue.append(plus)
	sValue.append(minus)
	return sValue


def calculateEntropy(X, Y):
	if (X==0 or Y==0):
		return 0
	else:
		poo = float(X)/(X+Y)
		choo = float(Y)/(X+Y)
		x = -poo*(np.log2(poo))-choo*(np.log2(choo))
		return x

def calculateGain(datapoint_list, attribute):

	totalS = getS(datapoint_list)
	totalEntropy = calculateEntropy(totalS[0], totalS[1])
	
	if totalEntropy ==0:
		return 0

	else:
		denomin = totalS[0]+totalS[1]
	
		sAttribute = getS(datapoint_list, attribute)
		subEntropyPos = calculateEntropy(sAttribute[0], sAttribute[1])
		nomin1 = sAttribute[0]+sAttribute[1]
	 
		subEntropyNeg = calculateEntropy(totalS[0]-sAttribute[0], totalS[1]-sAttribute[1])
		nomin2 = denomin - nomin1

		gain = totalEntropy - (float(nomin1)/denomin)*subEntropyPos - (float(nomin2)/denomin)*subEntropyNeg
	
		return gain

def gainiestAttribute(data_list):
	list_of_gains = []
	i =0
	amt_of_atts = len(data_list[0].asvalues)
	while i < amt_of_atts:
		gain = calculateGain(data_list, i)
		list_of_gains.append(gain)
		i = i+1
	
	if max(list_of_gains) == 0:
		return 0
	else:
		attributeIndex = list_of_gains.index(max(list_of_gains))
		return attributeIndex

def trimDataList(attribute, on_off, data_list): #on =1 off =0
	if attribute ==0:
		return data_list
	else:
		newdatalist =[]
		for datapoint in data_list:
			if datapoint.getAttributeValue(attribute) == on_off:
				newdatalist.append(datapoint)
		return newdatalist

def moreHobosOrHippies(data_list):
	hobo = 0
	hippie = 0
	for point in data_list:
		if point.hoboOrHippie ==1:
			hobo = hobo + 1
		else:
			hippie = hippie +1
	if hobo>hippie:
		return 1
	else:
		return 0	
	


##------TREE-------------###

#TODO
class Tree:
	def __init__(self):
		self.rootNode = None
		self.currentNode = None
		self.notInitialized = True
		self.currDatalist = []
		self.nodes = [] 

	def construct(self, datalist):		
		if gainiestAttribute(datalist) ==0:
			node1 = Node()
			node1.leaf = moreHobosOrHippies(datalist)
			self.currentNode.addChild(node1)
			node1.stem = datalist[0].getAttributeValue(self.currentNode.attribute)
		else:
			node2= Node(gainiestAttribute(datalist))
			if self.rootNode == None:
				self.rootNode = node2
			else:
				self.currentNode.addChild(node2)	
				node2.stem = datalist[0].getAttributeValue(self.currentNode.attribute)
			self.currentNode = node2
				
			neg_list = trimDataList(gainiestAttribute(datalist), 0, datalist)
			pos_list = trimDataList(gainiestAttribute(datalist), 1, datalist)
			
			#because apparently the order of construction matters...
			if gainiestAttribute(neg_list) ==0 and gainiestAttribute(pos_list)!=0:
				self.construct(neg_list)
				self.construct(pos_list)
			
			else:
				self.construct(pos_list)
				self.construct(neg_list)

	def predictPoint(self, values):
		point = Datapoint(values)
		
		#start at root node and follow the tree down until you find a leaf. 
		self.currentNode = self.rootNode
		pred = None

		while self.currentNode.leaf == None:	
			target_att = self.currentNode.attribute
			value = point.getAttributeValue(target_att)

			for child in self.currentNode.children:
				if child.stem == value:
					found = True
					self.currentNode = child
			if found == False:
				print "something went wrong"
			else:
				pred = self.currentNode.leaf
		return pred
			
	def test(self, datalist):
		total = len(datalist)
		count = 0
		for point in datalist:
			if int(self.predictPoint(point.asvalues)) == int(point.asvalues[4]):
				count = count+1
		accuracy = float(count*100)/total
		return accuracy
	


 
