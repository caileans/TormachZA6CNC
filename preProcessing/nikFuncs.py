import numpy as np
import math 

def getTheta(centerPoint, startPoint, endPoint, rotAxis):

	rc=centerPoint
	rs=startPoint
	re = endPoint
	ar=rotAxis

	# at this point assume everything is a 3 element np array

	ar=ar/np.linalg.norm(ar) #get axis hat
	# print(ar)
	# get directional vectors
	rcs= rs-rc
	rce= re-rc
	# get planar vectors
	rcs-=np.dot(rcs,ar)*ar
	rce-=np.dot(rce,ar)*ar

	theta=math.acos(np.dot(rce,rcs)/np.linalg.norm(rce)/np.linalg.norm(rcs))

	direction= np.dot(np.cross(ar,rcs),rce)
	# print(theta)
	# print(direction)
	if direction<0:
		theta=2*math.pi-theta
	zmag= np.dot(re-rs,ar)
	return [0,theta], rs-rc,ar,zmag

def getPoint(rcs,ar, zmag,theta,thetaTotal):

	# print(ar)
	x=rcs
	z=ar
	magnitude=np.linalg.norm(z)
	# print(magnitude)
	z/=magnitude
	offset=np.dot(x,z)
	x-= np.dot(z,x)*z
	y=np.cross(z,x)
	return x*math.cos(theta)+y*math.sin(theta)+z*(zmag*theta/thetaTotal+offset)



# ------------- testing ---------


c=np.zeros(3)
s=np.array([1,0,1])
e=np.array([0,-1,-1])
z=np.array([0,0,1])

t1,rcs1,ar1, zm1 =getTheta(c,s,-1*e,z)
# print(getTheta(c,s,-1*e,z))

t2,rcs2,ar2,zm2=getTheta(c,s,e,-1*z)

for i in range(11):
	print(getPoint(rcs1,ar1,zm1,i*t1[1]/10,t1[1]))
	print(getPoint(rcs2,ar2,zm2,i*t2[1]/10,t2[1]))

