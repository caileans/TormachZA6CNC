import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(__file__.split("Tormach")[0]+"TormachZA6CNC\\rosNodes\\src\\tormach_controller\\scripts\\lib\\preProcessing"))
sys.path.append(os.path.abspath(__file__.split("Tormach")[0]+"TormachZA6CNC\\rosNodes\\src\\tormach_controller\\scripts\\lib"))
sys.path.append(os.path.abspath(__file__.split("Tormach")[0]+"TormachZA6CNC\\data\\jointvel"))
sys.path.append(os.path.abspath(__file__.split("Tormach")[0]+"TormachZA6CNC\\data"))
import numpy as np
from math import sin, cos, pi,exp
import csv
from scipy.stats import linregress
import math
import gravityIsolation as grav
import InverseKinematics as ik
import general_robotics_toolbox as grtb

straightUp= [0,0,-np.pi/2,0,0,0]

def frictionModel(v,tau,a,b=[0,0,0,0,0,0]):
	A=np.zeros((6,6));
	for i in range(6):
		for j in range(6):
			A[i][j]=a[6*i+j]
	v=np.array(v)[0:6]
	# print(v)
	tau=np.array(tau)[0:6]
	# print(tau)
	tau=tau-np.matmul(A,v)
	# print(tau)
	# print(np.shape(v))
	for val in range(6):
		# print(b[val]*np.sign(v[val]))
		k=1
		barrier=.005
		if np.sign(v[val])*v[val]<barrier:
			k=np.sign(v[val])*v[val]/barrier
		tau[val]+=k*b[val]*np.sign(v[val])
	# print(tau)
	return tau

def optModel(v,tau,a,b=[0,0,0,0,0,0]):
	output=[];
	for i in range(np.shape(tau)[0]):
		temp=frictionModel(v,tau,a)[:,0]
		for c in range(6):
			output.append(temp[c]**2)
	return output
def getData(filename):
	vel=[[],[],[],[],[],[]];
	# tau=np.zeros((6,7));
	# vel=[]
	tau=[[],[],[],[],[],[]];
	index=0
	c=1
	flag=False
	flag2=False
	with open(filename, 'r') as file:
		for line in file:
		# print(line.strip())
			temp=line.strip()
			if (c%19)==17 and flag: #velocity
				temp=temp.split('[')[1][0:-1].split(',')
				temp=np.array(temp, dtype=float)
				for i in range(6):
					# print(vel)
					# print(i)
					if  temp[i]<-.055:
						index=i
						vel[i].append(temp[i])
						flag2=True
			elif(c%19)==18 and flag and flag2: #effort
				temp=temp.split('[')[1][0:-1].split(',')
				temp=np.array(temp, dtype=float)
				if any(val>100 for val in temp) or any(val<-100 for val in temp):
					vel[index]=vel[index][:-1]
				else:
					# for i in range(6):
					# 	tau[index,i]+=temp[i]/vel[index][-1]
					# tau[index,6]+=1
					tau[index].append(temp[index])
				flag=False
				flag2=False
			elif (c%19)==16: #position
				flag=True
				temp=temp.split('[')[1][0:-1].split(',')
				temp=np.array(temp, dtype=float)
				for point in range(6):
					if temp[point]>pi*5.0/180.0+straightUp[point] or temp[point]<-pi*5.0/180.0+straightUp[point]:
						flag=False

			c+=1
	return (vel),(tau)
def getTestData(filename):
	time=[]
	initialTime=0
	vel=[];
	pos=[];
	tau=[];
	c=1
	flag=True
	with open(filename, 'r') as file:
		for line in file:
		# print(line.strip())
			temp=line.strip()
			if (c%19)==17 and flag: #velocity
				temp=temp.split('[')[1][0:-1].split(',')
				vel.append(np.array(temp[0:6], dtype=float))
			elif(c%19)==18 and flag: #effort
				temp=temp.split('[')[1][0:-1].split(',')
				tau.append(np.array(temp[0:6], dtype=float))
				flag=False
			elif (c%19)==16: #position
				flag=True
				temp=temp.split('[')[1][0:-1].split(',')
				temp=np.array(temp, dtype=float)
				pos.append(np.array(temp[0:6], dtype=float))
				# for point in range(6):
				# 	if temp[point]>pi*5.0/180.0+straightUp[point] or temp[point]<-pi*5.0/180.0+straightUp[point]:
				# 		flag=False
			elif (c%19)==4: #secs
				temp=float(temp.split(':')[1].split(' ')[-1])
				time.append(temp)
			elif (c%19)==5: #nsecs
				temp=float(temp.split(':')[1].split(' ')[-1])
				time[-1]+= temp/10.0**9 - initialTime
				if c==5:
					initialTime=time[0]
					time[0]=0
			c+=1
	return time,pos,vel,tau
def calibrate(filename):
	# m,b,r=0
	vel,tau=getData(filename)
	a0=np.zeros(36)
	b=np.zeros(6)
	r=np.zeros(6)
	# for i in range(6):
	# 	for j in range(6):
	# 		a0[6*i+j]=tau[i,j]/tau[i,6]
	# print(len(vel[0]))
	# print(len(tau[0]))
	for i in range(6):
		# print(len(vel[i]))
		# print(len(tau[i]))
		temp=linregress(vel[i],tau[i])
		a0[6*i+i]=temp.slope
		b[i]=temp.intercept
		r[i]=temp.rvalue
	# print(a0)
	# obj= lambda x:optModel(vel,tau,x)
	# res = least_squares(obj, a0, args=())
	# adjustedTau= lambda v, tau: frictionModel(v,tau,res.x);
	return a0,b,r
	# print(obj(a0))

def saveA(a):
	print(a)
	with open('velFrictionGains.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(a)
def saveB(b):
	print(b)
	with open('velFrictionConst.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(b)

def getA():
	with open(__file__.split("Tormach")[0]+"TormachZA6CNC\\data\\jointvel\\"+'velFrictionGains.csv', 'r', newline='') as csvfile:
		reader = csv.reader(csvfile)
		a=np.zeros(36)
		for row in reader:
			c=0
			# print(c)
			# print(row)
			for val in row:
				a[c]=float( val)
				c+=1
	return a

def getB():
	with open(__file__.split("Tormach")[0]+"TormachZA6CNC\\data\\jointvel\\"+'velFrictionConst.csv', 'r', newline='') as csvfile:
		reader = csv.reader(csvfile)
		a=np.zeros(6)
		for row in reader:
			c=0
			# print(c)
			# print(row)
			for val in row:
				a[c]=float( val)
				c+=1
	return a

def getFrictionModel():
	return getA(),getB()