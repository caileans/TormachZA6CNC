import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(__file__.split("data\\RGcode_020425\\nikplot.py")[0]+"\\rosNodes\\src\\tormach_controller\\scripts\\lib\\preProcessing"))
sys.path.append(os.path.abspath(__file__.split("data\\RGcode_020425\\nikplot.py")[0]+"\\rosNodes\\src\\tormach_controller\\scripts\\lib"))
# print(sys.path)

import matplotlib.pyplot as plt
import numpy as np
import InverseKinematics as ik
import general_robotics_toolbox as grtb
import gravityIsolation as grav
import ReadROSLogFile as readlog
# import seaborn as sns



jointState=readlog.JointState([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])


gravModle=grav.calibrate(__file__.split("data\\RGcode_020425\\nikplot.py")[0]+"/rosNodes/src/tormach_controller/scripts/lib/gravityIsolationData.csv")

readlog.readJointStatesFile("states020425.txt", jointState, 1738724484)
robotFK=ik.tormachZA6fk()


jpose=[];
tau=[];
tauAdjust=[];
time=[];
force=[];
forceAdjust=[];
rpose=[];
c=0;

for i in range(len(jointState.time)):
	if c==0:
		c=1;
	else:

		jpose.append(np.array(jointState.pos[i][0:6]))
		tau.append(np.array(jointState.eff[i][0:6]))
		tauAdjust.append(np.array(gravModle(jpose[-1],tau[-1])))
		time.append(np.array(jointState.time[i]))
		jac=grtb.robotjacobian(robotFK,jpose[-1])
		force.append(np.matmul(jac,tau[-1]))
		forceAdjust.append(np.matmul(jac,tauAdjust[-1]))
		rpose.append(np.array(grtb.fwdkin(robotFK,jpose[-1]).p))

jpose=np.transpose(np.array(jpose))
tau=np.transpose(np.array(tau))
tauAdjust=np.transpose(np.array(tauAdjust))
force=np.transpose(np.array(force))
forceAdjust=np.transpose(np.array(forceAdjust))
rpose=np.transpose(np.array(rpose))
# print(jpose[0])
plt.figure(1)
# with plt.style.context('Solarize_Light2'):
plt.plot(time,tau[0], 'r1')
plt.plot(time,tau[1], 'g1')
plt.plot(time,tau[2], 'b1')
plt.plot(time,tau[3], 'c1')
plt.plot(time,tau[4], 'm1')
plt.plot(time,tau[5], 'y1')

# sns.set_palette("coolwarm")
# with plt.style.context('seaborn-v0_8-dark-palette'):
plt.plot(time,tauAdjust[0],'rD',markersize=2)
plt.plot(time,tauAdjust[1],'gD',markersize=2)
plt.plot(time,tauAdjust[2],'bD',markersize=2)
plt.plot(time,tauAdjust[3],'cD',markersize=2)
plt.plot(time,tauAdjust[4],'mD',markersize=2)
plt.plot(time,tauAdjust[5],'yD',markersize=2)

# plt.plot(time,jpose[0], 'r.')
# plt.plot(time,jpose[1], 'g.')
# plt.plot(time,jpose[2], 'b.')
# plt.plot(time,jpose[3], 'c.')
# plt.plot(time,jpose[4], 'm.')
# plt.plot(time,jpose[5], 'y.')

plt.legend(['j1 tau','j2 tau','j3 tau','j4 tau','j5 tau','j6 tau','j1 tau Adjusted','j2 tau Adjusted','j3 tau Adjusted','j4 tau Adjusted','j5 tau Adjusted','j6 tau Adjusted','j1 pose','j2 pose','j3 pose','j4 pose','j5 pose','j6 pose'])

plt.figure(2)

plt.plot(time,force[3],'r1')
plt.plot(time, force[4],'g1')
plt.plot(time,force[5],'c1')

plt.plot(time,forceAdjust[3],'rD',markersize=2)
plt.plot(time,forceAdjust[4],'gD',markersize=2)
plt.plot(time,forceAdjust[5],'cD',markersize=2)

plt.legend(['force x','force y','force z','adjusted force x','adjusted force y','adjusted force z'])

fig=plt.figure(3)
# fig,ax=plt.subplots(3)

ax=fig.add_subplot(2,2,1,projection='3d')
scatter = ax.scatter(rpose[0],rpose[1],rpose[2],c=force[5],cmap='PRGn')
fig.colorbar(scatter,ax=ax)
ax.set_title("force Z")
ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")
ax.set_zlabel("Z (mm)")
ax=fig.add_subplot(2,2,2,projection='3d')
scatter = ax.scatter(rpose[0],rpose[1],rpose[2],c=force[4],cmap='PRGn')
fig.colorbar(scatter,ax=ax)
ax.set_title("force Y")
ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")
ax.set_zlabel("Z (mm)")
ax=fig.add_subplot(2,2,3,projection='3d')
scatter = ax.scatter(rpose[0],rpose[1],rpose[2],c=force[3],cmap='PRGn')
fig.colorbar(scatter,ax=ax)
ax.set_title("force X")
ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")
ax.set_zlabel("Z (mm)")


fig=plt.figure(4)
# fig,ax=plt.subplots(3)

ax=fig.add_subplot(2,2,1,projection='3d')
scatter = ax.scatter(rpose[0],rpose[1],rpose[2],c=forceAdjust[5],cmap='PRGn')
fig.colorbar(scatter,ax=ax)
ax.set_title("Adjusted force Z")
ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")
ax.set_zlabel("Z (mm)")
ax=fig.add_subplot(2,2,2,projection='3d')
scatter = ax.scatter(rpose[0],rpose[1],rpose[2],c=forceAdjust[4],cmap='PRGn')
fig.colorbar(scatter,ax=ax)
ax.set_title("Adjusted force Y")
ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")
ax.set_zlabel("Z (mm)")
ax=fig.add_subplot(2,2,3,projection='3d')
scatter = ax.scatter(rpose[0],rpose[1],rpose[2],c=forceAdjust[3],cmap='PRGn')
fig.colorbar(scatter,ax=ax)
ax.set_title("Adjusted force X")
ax.set_xlabel("X (mm)")
ax.set_ylabel("Y (mm)")
ax.set_zlabel("Z (mm)")


plt.show()
