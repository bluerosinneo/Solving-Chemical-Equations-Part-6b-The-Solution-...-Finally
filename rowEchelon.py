# This code follows the following post.
# http://cramerexplainsmath.com/2018/01/30/solving-chemical-equations-part-6b-the-solution-finally/
# @desc This class offers the means to get an n by m 
# into a sort of reduced row echelon form for the purpose 
# of balancing a chemical eqution.  A detailed description of each
# method can be found in the post
# @author Cramer Grimes cramergrimes@gmail.com

class rowEchelon:
	@staticmethod
	def showMatrix(A):
		for i in range(0,len(A)):
			print A[i]

	@staticmethod
	def swapRow(A,i1,i2):
		hold = A[i1] #pass the ball in your i1 hand to hold
		A[i1]=A[i2] #pas the ball in your i2 hand to your i1 hand
		A[i2]=hold #take the ball from hold with your i2 hand

	@staticmethod
	def findMakeBlastPoint(A,blastInfo):
		for j in range(blastInfo['j'],len(A[0])): #search first down a column to find a non-zero
			for i in range(blastInfo['i'],len(A)): #will move to the next column to continue search
				if (A[i][j]!=0):
					if (i!=blastInfo['i']):
						rowEchelon.swapRow(A,i,blastInfo['i'])
					blastInfo['j']=j
					return 
		blastInfo['endOfLine']=True
		return

	@staticmethod
	def crissCross(A,i1,j1,i2,j2):
		A[i2][j2]=((A[i1][j1]*A[i2][j2])-(A[i1][j2]*A[i2][j1]))

	@staticmethod
	def pivotBlastsAsh(A,iBlast,jBlast):
		for i in range(0,len(A)):
			for j in range(0,len(A[0])):
				if((i!=iBlast)&(j!=jBlast)):
					rowEchelon.crissCross(A,iBlast,jBlast,i,j)
		for i in range(0,len(A)):
			if(i!=iBlast):
				A[i][jBlast]=0

	@staticmethod
	def gCD(a,b):
		if(b>a):
			temp = a
			a=b
			b=temp
		while(b>0):
			temp = b
			b = a%b
			a = temp
		return a

	@staticmethod
	def gCDBar(aBar):
		result = 1
		if (len(aBar)>0):
			result = aBar[0]
		if(len(aBar)>1):
			for i in range(1,len(aBar)):
				result = rowEchelon.gCD(result,aBar[i])
		return result




	@staticmethod
	def simplifyRow(A,i):
		nonZeroElements = []
		for j in range(0,len(A[i])):
			if (A[i][j]!=0):
				if(A[i][j]<0):
					nonZeroElements.append((A[i][j])*(-1))
				else:
					nonZeroElements.append(A[i][j])
		factor = rowEchelon.gCDBar(nonZeroElements)
		for j in range(0,len(A[i])):
			if (A[i][j]!=0):
				A[i][j]=(A[i][j]/factor)

	@staticmethod
	def simplifyMat(A):
		for i in range(0,len(A)):
			simplify = False
			for j in range(0,len(A[i])):
				if (A[i][j]!=0):
					simplify = True
			if (simplify == True):
				rowEchelon.simplifyRow(A,i)

	@staticmethod
	def solveRowEchelon(A):
		blastInfo={'i': 0, 'j': 0, 'endOfLine': False }
		while(blastInfo['endOfLine']!=True):
			rowEchelon.findMakeBlastPoint(A,blastInfo)
			if(blastInfo['endOfLine']==True):
				break
			rowEchelon.pivotBlastsAsh(A,blastInfo['i'],blastInfo['j'])
			rowEchelon.simplifyMat(A)
			if(blastInfo['i']==(len(A)-1)|(blastInfo['j']==(len(A[0])-1))):
				blastInfo['endOfLine']=True
				break
			else:
				blastInfo['i']=blastInfo['i']+1
				blastInfo['j']=blastInfo['j']+1
		rowEchelon.simplifyMatNoLeadingNegativ(A) # added after original roeEchlon post

# everything added after original roeEchlon post

	@staticmethod
	def multiplyByRow(A,i,k):
		for j in range(0,len(A[0])):
			A[i][j]=(A[i][j]*k)

	@staticmethod
	def simplifyMatNoLeadingNegativ(A):
		for i in range(0, len(A)):
			foundLeading = False
			for j in range(0, len(A[0])):
				if(A[i][j]!=0):
					foundLeading = True
					if (A[i][j]<0):
						rowEchelon.multiplyByRow(A,i,(-1))
				if(foundLeading == True):
					break

	@staticmethod
	def lCM(a,b):
		return ((a*b)/rowEchelon.gCD(a,b))

	@staticmethod
	def lCMbar(aBar):
		result = 1
		if (len(aBar)>0):
			result = aBar[0]
		if (len(aBar)>1):
			for i in range(1,len(aBar)):
				if (aBar[i]!=0):
					result = rowEchelon.lCM(result,aBar[i])
		return result

	@staticmethod
	def partialSolution(A,jFreedom):
		iMax = len(A)
		jMax = len(A[0])
		numeratorBar = [0 for i in range(0,jMax)]
		denominatorBar = [0 for i in range(0,jMax)]

		for i in range(0,iMax):
			if (A[i][jFreedom]!=0):
				for j in range(0,jMax):
					if ((A[i][j]!=0)&(j<jFreedom)):
						numeratorBar[j] = A[i][jFreedom]*(-1)
						denominatorBar[j] = A[i][j]
						break
		
		multiplier = rowEchelon.lCMbar(denominatorBar)
		
		for i in range(0,jMax):
			if (denominatorBar[i]!=0):
				numeratorBar[i] = numeratorBar[i]*(multiplier/denominatorBar[i])
		
		numeratorBar[jFreedom] = multiplier
		return numeratorBar

	@staticmethod
	def addVectors(a,b):
		if (len(a)==len(b)):
			for i in range(0,len(a)):
				a[i] = a[i] + b[i]


	@staticmethod
	def solveHomogenous(A):
		iMax = len(A)
		jMax = len(A[0])
		solution = [0 for i in range(0,jMax)]

		for j in range(1,jMax):
			doneWithCheckFreedom = False
			for i in range(0,iMax):
				if (A[i][j]!=0):
					for jLead in range(0,j):
						if (A[i][jLead]!=0):
							smallSolution = []
							smallSolution = rowEchelon.partialSolution(A,j)
							rowEchelon.addVectors(solution,smallSolution)
							doneWithCheckFreedom = True
							break
				if (doneWithCheckFreedom == True):
					break
		return solution