import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__).split("controller.py")[0]+"/lib")))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__).split("controller.py")[0]+"/lib/__init__.py")))
# print(os.path.dirname(os.path.dirname('/scripts/lib')))
# print(os.path.abspath(__file__.split("controller.py")[0]+"/lib"))
sys.path.append(os.path.abspath(__file__.split("/lib")[0]))
sys.path.append(os.path.abspath(__file__.split("/lib")[0]+"/lib"))
sys.path.append(os.path.abspath(__file__.split("/lib")[0]+"/lib/preProcessing"))
# sys.path.append(os.path.abspath(__file__.split("lib")[0]+"../../../../preProcessing"))
# print(sys.path)

import numpy as np
# import lib.InverseKinematics as ik

import general_robotics_toolbox as grtb

def tormach():
	H=np.array([[0,0,0,1,0,1],[0,1,1,0,1,0],[1,0,0,0,0,0]])
	H=np.transpose(H)
	P=np.array([[.0,.025,.0,.123+.2965,.0,.0,.2175-.1],[.0,.0,.0,.0,.0,.0,.0],[.279,.171,.454,.035,.0,.0,.0]])*1000.0 
	P=np.transpose(P)
	return H,P

def NRJn(n,q,H):

	R=grtb.rot(H[0,:],q[0])
	for i in range(n-1):
		R=np.matmul(R,grtb.rot(H[i+1,:],q[i+1]))
	# print(R)
	# print(n)
	return R

# def JnRe(n,q,H):
# 	R=grtb.rot(H[5,:],q[5])
# 	for i in range(6-n):
# 		R=np.matmul(grtb.rot(H[4-i,:],q[4-i]),R)
# 	return R

def rJne(n,q,H,P):

	r=np.zeros(3);
	for i in range(7-n):
		r+=np.matmul(NRJn(n+i,q,H),P[n+i,:])
	return r

def map(q):

	H,P=tormach()
	matr=np.zeros((6,6))
	for i in range(6):
		matr[0:3,i]=np.matmul(H[i,:],np.matmul(np.transpose(NRJn(i+1,q,H)),grtb.hat(rJne(i+1,q,H,P))))
		matr[3:,i]=np.matmul(H[i,:],np.transpose(NRJn(i+1,q,H)))
	return matr

def map2(q):

	H,P=tormach()
	matr=np.zeros((6,6));
	for i in range(6):
		r=rJne(i+1,q,H,P)
		matr[0:3,i]=np.matmul(grtb.hat(np.matmul(NRJn(i+1,q,H),H[i,:])),r)/np.dot(r,r)
		temp=np.matmul(H[i,:],(NRJn(i+1,q,H)))
		for j in range(3):
			matr[3+j,i]=temp[j]
		# print(H[i,:])
		# c=NRJn(i+1,q,H)
		# print(c)
		# print(np.transpose(np.matmul(c,H[i,:])))
	return matr	

def getEEState(q,tau):
	return np.matmul(np.linalg.inv(map(q)),tau)
