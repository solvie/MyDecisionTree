#***************************************************************************************************************#
#	THIS IS A DECISION TREE ADAPTATION BASED ON THE ID3 ALGORITHM						#
#  														#
#	Solvie Lee/ 2015											#
#	This algorithm only deals with a specific dataset of binary values but later it should be modified	#
#	such that it can take as input any dataset with binary attribute value pairs				#
#														#
#***************************************************************************************************************#

# A decision tree should be a root node that has a bunch of children attached to it.
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
		self.holeInJeansAuthentic = values[0]
		self.dreadlocks = values[1]
		self.coffeeCupEmpty = values[2]
		self.smartPhone = values[3]
		self.hoboOrHippie = values[4]
	
	def read(self):
		print self.holeInJeansAuthentic, self.dreadlocks, self.coffeeCupEmpty, self.smartPhone, self.hoboOrHippie
	
	def getAttribute(self, i):
		if i ==1:
			return int(self.holeInJeansAuthentic)
		elif i ==2:
			return int(self.dreadlocks)
		elif i ==3:
			return int(self.coffeeCupEmpty)
		elif i ==4:
			return int(self.smartPhone)
		else: 
			return None	
			print "invalid attribute number"
			
#TODO
class Node:
	"""
	The tree is built up of nodes. If the attribute_no is -1, that means it is a leaf. 

	"""

	def __init__(self, attribute_no = -1):
		self.children = []
		self.numAncestors = 0
		self.attribute = attribute_no	 #integer code
		self.parent = None
		self.leaf = None

	def addChild(self, node):
		self.children.append(node)
		node.setParent(self)

	def setParent(self, node):
		self.parent = node
	
	def getNumAncestors(self):
		self.numAncestors = 0
		ancestor = self.parent
		while  ancestor != None:
			self.numAncestors = self.numAncestors+1
			ancestor = ancestor.parent
		return self.numAncestors
	
	def setLeaf(self, value):
		self.leaf = value

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
			if int(point.hoboOrHippie) ==1 and int(point.getAttribute(optional_attribute))==1:
				plus = plus +1
			elif int(point.hoboOrHippie)==0 and int(point.getAttribute(optional_attribute))==1:
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
	while i<4:
		gain = calculateGain(data_list, i)
		list_of_gains.append(gain)
		i = i+1
	
	attributeIndex = list_of_gains.index(max(list_of_gains))
	return attributeIndex

def trimDataList(attribute, on_off, data_list): #on =1 off =0
	for datapoint in data_list:
		if datapoint.getAttribute(attribute) != on_off:
			data_list.remove(datapoint)
	return data_list
	
	


##------TREE-------------###

#TODO
class Tree:
	def __init__(self):
		self.rootNode = None
		self.currentNode = None	

	
	def construct(data_list):
		attribute = gainistAttribute(data_list)
		self.rootNode = Node(attribute)
		self.buildBranches(data_list, self.rootNode))

	
	def buildBranches(data_list, node):
	
		currentNode = node
		theS = getS(data_list)	

		#if the current node has 3 ancestors, or the entropy of the datalist is 0, then it is a dead end

		if currentNode.getNumAncestors()==3  or calculateEntropy(theS[0], theS[1]) ==0:
			#calculate the value of that dead end by which one has the highest count.
			hobos = 0
			hippies = 0
			for datapoint in data_list:
				if datapoint.hoboOrHippie == 1:
					hobos = hobos+1
				else:
					hippies = hippies +1
			node = Node()
			if hobos>hippies:
				node.setLeaf(True)
			else:
				node.setLeaf(False)

			currentNode.addChild(node)	 
	
		else:
			#we split the node, and call build branches on it again. 	
			new_pos_data_list = trimDataList(currentNode.attribute, True, data_list)	
			attribute1 = gainiestAttribute(new_pos_data_list)
			newNode1 = Node(attribute1)		
			currentNode.addChild(newNode1)
			buildBranches(new_pos_data_list, newNode1)
			
	
			new_neg_data_list = trimDataList(currentNode.attribute, False, data_list)
			attribute0 = gainiestAttribute(new_neg_data_list)	
			newNode0 = Node(attribute0)
			currentNode.addChild(newNode0)
			buildBranches(new_neg_data_list, newNode0)	

##----------------MAIN METHOD ----------------------##


# Here have some code that decides how much of the data to use to train the algorithm. 

#1.take all of the features and calculate entropy. While not zero or not all attributes have been noded, calculate gain for every attribute
#2.pick the one with biggest gain and split the node and call function again. If
# it is the first time, make it the root node; every subsequent node, add to the previous node; make the previous node the parent, 
# and any subsequent nodes become the children. 
#3.base case, set value.  

#FIXME

#data_list = csvToDatapointList("hobohippiedataset.csv")
#entropy = calculateEntropy(data_list)
#notFinished = True
#tree = Tree()

#while notFinished:
#	gainiestAttribute(data_list)
	#find the biggest one, make that a node! If no tree, 
#	node = Node(attributeIndex)
#	if tree.rootNode = None:
#		tree.setRootNode(node)
#	else:
#		tree.rootNode
		
	
	
	
# construct tree from 75% of data default, or customizeable.  


 
