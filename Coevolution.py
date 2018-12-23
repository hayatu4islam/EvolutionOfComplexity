from random import randint
from numpy.random import normal
from matplotlib import pyplot
import numpy
class Member(object):
	"""This is the class for a member of the population"""
	def __init__(self,dimensions,length,version):
		self.version = version
		self.dimensions = dimensions
		self.length = length
		if(version == 1):	
			self.value = [0 for i in range(self.length)]
		else:
			self.value = [[0 for i in range(self.length)] for j in range(dimensions)]
		self.fitness = 0
		self.failures = 0

	def Fitness(self, S):
		sum = 0
		if(self.version==1):
			for i in S:
				if(self.ToNumber(0)>i.ToNumber(0)):
					sum = sum + 1
		elif(self.version==2):
			for i in S:
				d = 0
				for j in range(i.dimensions):
					if(abs(self.ToNumber(j)-i.ToNumber(j))>abs(self.ToNumber(d)-i.ToNumber(d))):
						d = j
				if(self.ToNumber(d)>i.ToNumber(d)):
					sum = sum + 1
					i.failures = i.failures + 1
				else:
					self.failures = self.failures + 1
		elif(self.version==3 or self.version == 4):
			for i in S:
				d = 0
				for j in range(i.dimensions):
					if(abs(self.ToNumber(j)-i.ToNumber(j))<abs(self.ToNumber(d)-i.ToNumber(d))):
						d = j
				if(self.ToNumber(d)>i.ToNumber(d)):
					sum = sum + 1
					i.failures = i.failures + 1
				else:
					self.failures = self.failures + 1



		self.fitness = sum
	def ToNumber(self,dim):
		checker = [1 for i in range(self.length)]
		num = len([c for c,d in zip(checker,self.value[dim]) if c==d])
		return num
	def GetFitness(self):
		checker = [1 for i in range(self.length)]
		num = 0
		for i in range(self.dimensions):
			num = num + len([c for c,d in zip(checker,self.value[i]) if c==d])
		return num

class Population(object):
	"""docstring for population"""
	def __init__(self, size, dimensions, length, version, S=5):
		self.version = version
		self.dimensions = dimensions
		self.size = size
		self.length = length
		self.S = S
		self.members = [Member(dimensions, length, version) for i in range(size)]
	
	def GetMember(self):
		return self.members[randint(0,self.size-1)]

	def Replace(self, child):
		temp1 = randint(0,self.size-1)
		temp2 = randint(0,self.size-1)
		if(self.members[temp1].fitness > self.members[temp2].fitness):
			self.members[temp2] = child
		else:
			self.members[temp1] = child

	def Mutate(self, Pops):
		parent1 = self.GetMember()
		parent2 = self.GetMember()
		parent3 = self.GetMember()
		parent4 = self.GetMember()
		if(parent1.fitness>parent2.fitness):
			parent1 = parent1
		else:
			parent1 = parent2
		if(parent3.fitness>parent4.fitness):
			parent2 = parent3
		else:
			parent2 = parent4
		#child = Member(self.dimensions, self.length, self.version)
		child = self.CrossOver(parent1,parent2)
		if(self.version == 1):
			child.value = [child.value[i] if randint(0,200)!=1 else 1-child.value[i] for i in range(self.length)]
		else:
			for j in range(self.dimensions):
		 		child.value[j] = [child.value[j][i] if randint(0,200)!=1 else 1-child.value[j][i] for i in range(child.length)]
		fitnessCheckers = []
		for i in range(self.S):
			#fitnessCheckers.append(Pops[randint(0,len(Pops)-1)].GetMember())
			fitnessCheckers.append(Pops[randint(0,len(Pops)-1)].GetMember())
		child.Fitness(fitnessCheckers)
		# if(self.version==4):
		# 	self.members.append(child)
		# 	self.size = self.size + 1
		# else:
		self.Replace(child)
	def CrossOver(self,parent1,parent2):
		child = Member(self.dimensions, self.length, self.version)
		if(self.version == 1):
			child.value = [parent1.value[i] if randint(0,1)==1 else parent2.value[i] for i in range(self.length)]
		elif(self.version == 2 or self.version == 3 or self.version == 4):
			for j in range(self.dimensions):
				child.value[j] = [parent1.value[j][i] if randint(0,1)==1 else parent2.value[j][i] for i in range(self.length)]
		return child
def Figure3():
	size = 10
	generations = 600
	S = 1
	populations = [Population(size,1,100,2,S=1) for i in range(2)]
	values = []
	values1 = [[] for i in populations]
	values2 = [[] for i in populations]
	fitness1 = [[] for i in populations]
	for i in range(generations):
		valuestemp1 = [[] for j in populations]
		valuestemp2 = [[] for j in populations]
		for num,j in enumerate(populations):
			populations_ex = [populations[k] for k in range(2) if k!=num]
			
			#for k in range(int(size)):
				
			fitsum = 0
			for k in range(size):
				j.Mutate(populations_ex)
				valuestemp1[num].append(populations[num].members[k].ToNumber(0))
				fitsum = fitsum + populations[num].members[k].fitness

			values1[num].append(valuestemp1[num])
			fitsum = fitsum / size
			fitness1[num].append(fitsum)
			values2[num].append(valuestemp2[num])
	
	fig, axs = pyplot.subplots(3, 1, gridspec_kw = {'height_ratios':[10, 1, 1]})
	axs[0].plot(range(generations),values1[0],'b,')
	axs[0].plot(range(generations),values1[1],'r,')
	axs[0].plot(range(generations),[50 for i in range(generations)],'k:')
	axs[0].set_ylim(0,100)
	axs[0].set_xlim(0,generations)
	axs[0].set_ylabel("Objective Fitness")
	axs[1].plot(range(generations),fitness1[0],'b,')
	axs[1].set_ylim(0,1)
	axs[2].plot(range(generations),fitness1[1],'r,')
	axs[2].set_ylim(0,1)
	axs[2].set_ylabel("Subjective Fitness")
def Figure4():
	size = 10
	generations = 600
	populations = [Population(size,10,10,2,S=2) for i in range(2)]
	values = []
	values1 = [[] for i in populations]
	values2 = [[] for i in populations]
	fitness1 = [[] for i in populations]
	for i in range(generations):
		valuestemp1 = [[] for j in populations]
		valuestemp2 = [[] for j in populations]
		for num,j in enumerate(populations):
			populations_ex = [populations[k] for k in range(2) if k!=num]
			
			#for k in range(int(size)):
				
			fitsum = 0
			for k in range(j.size):
				j.Mutate(populations)
				valuestemp1[num].append(populations[num].members[k].GetFitness())
				fitsum = fitsum + populations[num].members[k].fitness
			values1[num].append(valuestemp1[num])
			fitsum = fitsum / j.size
			fitness1[num].append(fitsum)
			values2[num].append(valuestemp2[num])
	fig, axs = pyplot.subplots(3, 1, gridspec_kw = {'height_ratios':[10, 1, 1]})
	axs[0].plot(range(generations),values1[0],'b,')
	axs[0].plot(range(generations),values1[1],'r,')
	axs[0].plot(range(generations),[50 for i in range(generations)],'k:')
	axs[0].set_ylim(0,100)
	axs[0].set_xlim(0,generations)
	axs[0].set_ylabel("Objective Fitness")
	axs[1].plot(range(generations),fitness1[0],'b,')
	axs[1].set_ylim(0,1)
	axs[2].plot(range(generations),fitness1[1],'r,')
	axs[2].set_ylim(0,1)
	axs[2].set_ylabel("Subjective Fitness")
def Figure5():
	size = 15
	generations = 600
	S = 5
	dimensions = 10
	length = 10
	populations = [Population(size,dimensions,length,3) for i in range(2)]
	values = []
	values1 = [[] for i in populations]
	values2 = [[] for i in populations]
	fitness1 = [[] for i in populations]
	for i in range(generations):
		valuestemp1 = [[] for j in populations]
		valuestemp2 = [[] for j in populations]
		for num,j in enumerate(populations):
			populations_ex = [populations[k] for k in range(2) if k!=num]
			
			#for k in range(int(size)):
				
			fitsum = 0
			for k in range(size):
				j.Mutate(populations_ex)
				valuestemp1[num].append(populations[num].members[k].GetFitness())
				fitsum = fitsum + populations[num].members[k].fitness
			values1[num].append(valuestemp1[num])
			fitsum = fitsum 
			fitness1[num].append(fitsum/(dimensions*S))
			values2[num].append(valuestemp2[num])
	fig, axs = pyplot.subplots(3, 1, gridspec_kw = {'height_ratios':[10, 1, 1]})
	axs[0].plot(range(generations),values1[0],'b,')
	axs[0].plot(range(generations),values1[1],'r,')
	axs[0].plot(range(generations),[50 for i in range(generations)],'k:')
	axs[0].set_ylim(0,100)
	axs[0].set_xlim(0,generations)
	axs[0].set_ylabel("Objective Fitness")
	axs[1].plot(range(generations),fitness1[0],'b,')
	#axs[1].set_ylim(0,5)
	axs[2].plot(range(generations),fitness1[1],'r,')
	#axs[2].set_ylim(0,5)
	axs[2].set_ylabel("Subjective Fitness")
def Figure6():
	size = 10
	generations = 600
	S = 1
	dimensions = 1
	length = 100
	version = 3
	populations = [Population(size,dimensions,length,version,S=S) for i in range(2)]
	values = []
	values1 = [[] for i in populations]
	values2 = [[] for i in populations]
	fitness1 = [[] for i in populations]
	for i in range(generations):
		valuestemp1 = [[] for j in populations]
		valuestemp2 = [[] for j in populations]
		for num,j in enumerate(populations):
			populations_ex = [populations[k] for k in range(2) if k!=num]
			
			#for k in range(int(size)):
				
			fitsum = 0
			for k in range(size):
				j.Mutate(populations)
				valuestemp1[num].append(populations[num].members[k].GetFitness())
				fitsum = fitsum + populations[num].members[k].fitness

			for n,k in enumerate(j.members):
				if(k.failures>10):
					j.members.pop(n)
					choice = randint(0,size-2)
					while(k.failures<j.members[choice].failures):
						choice = randint(0,size-2)
					j.members.append(j.members[choice])
					j.members[-1].failures = 0
					for l in range(dimensions):
		 				j.members[-1].value[l] = [j.members[-1].value[l][p] if randint(0,200)!=1 else 1-j.members[-1].value[l][p] for p in range(length)]
			values1[num].append(valuestemp1[num])
			fitsum = fitsum / size
			fitness1[num].append(fitsum/(dimensions*S))
	fig, axs = pyplot.subplots(3, 1, gridspec_kw = {'height_ratios':[10, 1, 1]})

	axs[0].plot(range(generations),values1[0],'b,')
	axs[0].plot(range(generations),values1[1],'r,')
	axs[0].plot(range(generations),[50 for i in range(generations)],'k:')
	axs[0].set_ylim(0,100)
	axs[0].set_xlim(0,generations)
	axs[0].set_ylabel("Objective Fitness")
	axs[1].plot(range(generations),fitness1[0],'b,')
	#axs[1].set_ylim(0,5)
	axs[2].plot(range(generations),fitness1[1],'r,')
	#axs[2].set_ylim(0,5)
	axs[2].set_ylabel("Subjective Fitness")
print("Starting...")
Figure3()
# Figure4()
# Figure5()
Figure6()
print("Finished!")
pyplot.show()
