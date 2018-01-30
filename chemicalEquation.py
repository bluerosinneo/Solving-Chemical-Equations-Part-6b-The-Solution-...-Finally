# This code follows the following post.
# http://cramerexplainsmath.com/2018/01/30/solving-chemical-equations-part-6b-the-solution-finally/
# @desc This code works on the last part of getting the text of a chemical equation into
# a data structure.  Additionally the code exports a matrix representing
# the homogeneous linear system that solves for the coefficients of
#a balanced equation
# A detailed description can be found in the post
# @author Cramer Grimes cramergrimes@gmail.com

from chemicalFormula import chemicalFormula

class chemicalEquation:

	def __init__ (self):
		self.reactantDict = {}
		self.productDict = {}
		self.masterElementFormula = chemicalFormula()
		self.origEquation = ""

	def readEquation(self,equationText):
		self.origEquation = equationText
		start = equationText.find('-')
		end = equationText.find('>')
		reactantText = equationText[:start]
		if ((end+1)<len(equationText)):
			productText = equationText[(end+1):]
		else:
			productText = ""

		formulaCounter = {}
		formulaCounter['i'] = 0

		for reactantFormula in reactantText.split('+'):
			if len(reactantFormula.strip())>0:
				self.addFormula(True,reactantFormula.strip(),formulaCounter)

		[self.addFormula(False,productFormula.strip(),formulaCounter)
		for productFormula
		in productText.split('+')
		if len(productFormula.strip())>0]
	
	def addFormula(self,reactantBool,formulaText,formulaCounter):
		if (reactantBool == True):
			self.reactantDict[formulaCounter['i']] = chemicalFormula()
			self.reactantDict[formulaCounter['i']].readFormula(formulaText,1)
			formulaCounter['i'] = formulaCounter['i'] + 1
		else:
			self.productDict[formulaCounter['i']] = chemicalFormula()
			self.productDict[formulaCounter['i']].readFormula(formulaText,1)
			formulaCounter['i'] = formulaCounter['i'] + 1

	def generateMasterList(self):
		for i in self.reactantDict.keys():
			for elSym in self.reactantDict[i].elementDict.keys():
				self.masterElementFormula.addElement(elSym,1)
		for i in self.productDict.keys():
			for elSym in self.productDict[i].elementDict.keys():
				self.masterElementFormula.addElement(elSym,1)


	def checkEquation(self):
		reactantCount = len(self.reactantDict)
		productCount = len(self.productDict)
		for elSym in self.masterElementFormula.elementDict.keys():
			inReactants = False
			inProducts = False
			for i in range(0,reactantCount):
				if (elSym in self.reactantDict[i].elementDict):
					inReactants = True
			for i in range(reactantCount,reactantCount+productCount):
				if (elSym in self.productDict[i].elementDict):
					inProducts = True
			if ((inReactants==False)|(inProducts==False)):
				return False
		return True

	def showEquation(self):
		reactantCount = len(self.reactantDict)
		productCount = len(self.productDict)
		for i in range(0,reactantCount):
			print self.reactantDict[i].elementDict
			if (i!=(reactantCount-1)):
				print '+'
		print '->'
		for i in range(reactantCount,reactantCount+productCount):
			print self.productDict[i].elementDict
			if (i!=(reactantCount+productCount-1)):
				print '+'

	def generateMatrix(self):
		reactantCount = len(self.reactantDict)
		productCount = len(self.productDict)
		# elementCount = len(self.masterElementFormula.elementDict)
		A = []
		for elSym in self.masterElementFormula.elementDict.keys():
			a = []
			for i in range(0,reactantCount):
				if (elSym in self.reactantDict[i].elementDict):
					a.append(self.reactantDict[i].elementDict[elSym])
				else:
					a.append(0)
			for i in range(reactantCount,reactantCount+productCount):
				if (elSym in self.productDict[i].elementDict):
					a.append((self.productDict[i].elementDict[elSym])*(-1))
				else:
					a.append(0)
			A.append(a)
		return A

# everything added after original chemicalEquation post

	def setCoefficients(self,coefficientList):
		reactantCount = len(self.reactantDict)
		productCount = len(self.productDict)
		for i in range(0,reactantCount):
			self.reactantDict[i].formulaCoef = coefficientList[i]
		for i in range(reactantCount,reactantCount+productCount):
			self.productDict[i].formulaCoef = coefficientList[i]	

	def checkIfBalanced(self):
		reactantCount = len(self.reactantDict)
		productCount = len(self.productDict)
		for elSym in self.masterElementFormula.elementDict.keys():
			reactantElementCount = 0
			productElementCount = 0
			for i in range(0,reactantCount):
				if (elSym in self.reactantDict[i].elementDict):
					reactantElementCount = reactantElementCount + \
						(self.reactantDict[i].elementDict[elSym]*self.reactantDict[i].formulaCoef)
			for i in range(reactantCount,reactantCount+productCount):
				if (elSym in self.productDict[i].elementDict):
						productElementCount = (productElementCount + \
							(self.productDict[i].elementDict[elSym]*self.productDict[i].formulaCoef))
			if (reactantElementCount != productElementCount):
				return False
		return True

	def getBalancedString(self):
		stringList = []
		reactantCount = len(self.reactantDict)
		productCount = len(self.productDict)
		for i in range(0,reactantCount):
			if (self.reactantDict[i].formulaCoef!=1):
				stringList.append(str(self.reactantDict[i].formulaCoef)+self.reactantDict[i].origFormula)
			else:
				stringList.append(self.reactantDict[i].origFormula)
			if (i!=(reactantCount-1)):
				stringList.append('+')
		stringList.append('->')
		for i in range(reactantCount,reactantCount+productCount):
			if (self.productDict[i].formulaCoef!=1):
				stringList.append(str(self.productDict[i].formulaCoef)+self.productDict[i].origFormula)
			else:
				stringList.append(self.productDict[i].origFormula)
			if (i!=(reactantCount+productCount-1)):
				stringList.append('+')
		return ''.join(stringList)