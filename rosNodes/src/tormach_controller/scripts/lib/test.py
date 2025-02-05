import os, sys
import general_robotics_toolbox as grtb
import InverseKinematics as ik
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(__file__.split("test.py")[0]+"/preProcessing"))
import preProcessing.DataTypes
import preProcessing.GCodeToTrajectory as gct


# n=358
# output=np.zeros((n,6))
# output[-1]=np.array([-179,20,20,0,-40,0])*np.pi/180
# p=np.zeros((n,3))
# pout=np.zeros((n,3))
# H=np.array([[0,0,0,1,0,1],[0,1,1,0,1,0],[1,0,0,0,0,0]])
# P=np.array([[0,.025,0,.123,.2965,.1,.1175],[0,0,0,0,0,0,0],[.279,.171,.454,.035,0,0,0]])*1000
# robot= grtb.Robot(H,P,[0,0,0,0,0,0])
# robot2=ik.tormachZA6()
# abc=np.zeros((n,3))
# abcout=np.zeros((n,3))
# j1=[]

# for i in range(n):
# 	# print(grtb.fwdkin(robot,[i,i,i,i,i,i]))
# 	print(i)
# 	print(i*np.pi/180)
# 	r=grtb.fwdkin(robot,np.array([i-179,20,20,0,-40,0])*np.pi/180)
# 	print(ik.getIK(r.p,r.R,robot2))
# 	p[i,:]=np.array(r.p)
# 	# print(r.R)
# 	# print(grtb.rpy2R([0,-np.pi/2,-np.pi]))
# 	# print(r.p)
# 	sols=ik.getIK(r.p,r.R,robot2)
# 	for col in sols:
# 		j1.append(col[0][0])
# 	# output[i,:]=np.array(ik.getIK(r.p,r.R,robot2)[0][0])
# 	abc[i,:]=grtb.R2rpy(np.transpose(r.R))
# 	# abc[i,:]=grtb.R2rpy(r.R)
# 	print(abc)
# 	# output[i,:]=ik.runIK([r.p[0],r.p[1],r.p[2],abc[i,:][0]*180/np.pi,abc[i,:][1]*180/np.pi,abc[i,:][2]*180/np.pi],np.array([i,20,20,0,-40,0])*np.pi/180,robot2)
# 	output[i,:]=ik.runIK([r.p[0],r.p[1],r.p[2],abc[i,:][2]*180/np.pi,abc[i,:][1]*180/np.pi,abc[i,:][0]*180/np.pi],output[i-1,:],robot2)
# 	pout[i,:]=grtb.fwdkin(robot,np.array(output[i,:])).p
# 	abcout[i,:]=grtb.R2rpy(np.transpose(grtb.fwdkin(robot,np.array(output[i,:])).R))
# 	# abcout[i,:]=grtb.R2rpy(grtb.fwdkin(robot,np.array(output[i,:])).R)
# 	# output[i,:]-=np.array([i,20,20,0,-40,0])*np.pi/180
# print(output)

# plt.figure(1)
# plt.plot(output[:,0])
# plt.plot(output[:,1])
# plt.plot(output[:,2])
# plt.plot(output[:,3])
# plt.plot(output[:,4])
# plt.plot(output[:,5])
# plt.legend(['j1','j2','j3','j4','j5','j6'])

# plt.figure(2)
# plt.plot(p[:,0])
# plt.plot(p[:,1])
# plt.plot(p[:,2])
# plt.plot(pout[:,0])
# plt.plot(pout[:,1])
# plt.plot(pout[:,2])
# plt.legend(['x','y','z','cx','cy','cz'])
# # plt.show()


# plt.figure(3)
# plt.plot(abc[:,0])
# plt.plot(abc[:,1])
# plt.plot(abc[:,2])
# plt.plot(abcout[:,0])
# plt.plot(abcout[:,1])
# plt.plot(abcout[:,2])
# plt.legend(['x','y','z','cx','cy','cz'])
# plt.show()

j=[[0,0,0,0,0,0]]
pointList=gct.genTrajectory('../../../../../Gcode/circleTest.nc', a=1,hz=50,feedRate=.3,rapidFeed=.6)
i=1;
print(j[0])
for point in pointList:
	j.append(ik.runIK(np.append(np.array(point.pos[0:3]),point.rot[0:3], axis=0),j[i-1],robot2))
	i+=1
	# print(j)

plt.figure(4)
plt.plot(j[:][0])
plt.plot(j[:][1])
plt.plot(j[:][2])
plt.plot(j[:][3])
plt.plot(j[:][4]-np.ones(6)*.1)
plt.plot(j[:][5]+np.ones(6)*.1)
plt.legend(['j1','j2','j3','j4','j5','j6'])


plt.figure(5)
plt.plot(j1,".")

plt.show()