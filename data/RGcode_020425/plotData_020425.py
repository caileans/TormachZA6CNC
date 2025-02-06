import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))+"/../../")) #this is so cursed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))+"/../../rosNodes/src/tormach_controller/scripts/lib/preProcessing/")) #this is so much more cursed

import numpy as np
import matplotlib.pyplot as plt
import general_robotics_toolbox as grt
import GcodeParserV2

# import TrajectoryPlanner as tp
import ReadROSLogFile as rFile

# import general_robotics_toolbox as grtb




######## Read the data from the files
test1command = rFile.JointState([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
test1states  = rFile.JointState([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])

test1InitTime = 1738724486

rFile.readJointCommandFile('./data/RGcode_020425/pub020425.txt', test1command, initialTime=test1InitTime)

rFile.readJointStatesFile('./data/RGcode_020425/states020425.txt', test1states, initialTime=test1InitTime)



######## Calculate the velocities and account for latency:
latency = 0.01
hz = 80
vel = [0.,0.,0.,0.,0.,0.,0.,0.]

H=np.array([[.0,.0,.0,1.0,.0,1.0],[.0,1.0,1.0,.0,1.0,.0],[1.0,.0,.0,.0,.0,.0]])
P=np.array([[.0,.025,.0,.123,.2965,.1,.0175],[.0,.0,.0,.0,.0,.0,.0],[.279,.171,.454,.035,.0,.0,.0]])*1000.0 #approximated without 1mm offsets
bot=grt.Robot(H,P,[0,0,0,0,0,0])

cartPosesCommand = []
cartPosesStates = []

# test1command.vel = np.append(test1command.vel, [np.array([0.,0.,0.,0.,0.,0.,0.,0.], dtype=float)],axis=0)
for i in range(1, len(test1command.time)-1):
	test1command.time[i] += latency
	# print(i)
	for j in range(8):
		# print(j)
		vel[j] = (test1command.pos[i+1,j] - test1command.pos[i-1,j])/(2.0/80.0)
	test1command.vel = np.append(test1command.vel, [np.array(vel, dtype=float)],axis=0)


######## Run FKin to get to cartesian
	cartPose = grt.fwdkin(bot, test1command.pos[i])
	cartPosesCommand.append(cartPose.p)

test1command.vel = np.append(test1command.vel, [np.array([0.,0.,0.,0.,0.,0.,0.,0.], dtype=float)],axis=0)

for i in range(1, len(test1states.time)-1):
	cartPose = grt.fwdkin(bot, test1states.pos[i])
	cartPosesStates.append(cartPose.p)

cartPosesCommand = np.array(cartPosesCommand)
cartPosesStates = np.array(cartPosesStates)



######## Get the gcode points
parser = GcodeParserV2.GcodeParserV2(toolFrameOffset=[432.1,89,427])
# print(os.getcwd())
if parser.parseFile('./Gcode/TormachR.nc'):
	exit()

wayPoints = parser.evaluateGcode()

GcodePoints = []
for point in wayPoints:
	GcodePoints.append(point.pos)

GcodePoints = np.array(GcodePoints)

plotLineWidth = 0.5

######## First Plot
fig1 = plt.figure(1)
plt.plot(test1command.time[1:-1], test1command.pos[1:-1, 0], 'k.-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1command.time[1:-1], test1command.pos[1:-1, 1], 'k.-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1command.time[1:-1], test1command.pos[1:-1, 2], 'k.-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1command.time[1:-1], test1command.pos[1:-1, 3], 'k.-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1command.time[1:-1], test1command.pos[1:-1, 4], 'k.-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1command.time[1:-1], test1command.pos[1:-1, 5], 'k.-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1states.time[1:],test1states.pos[1:,0],'b.-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.pos[1:,1],'g.-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.pos[1:,2],'r.-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.pos[1:,3],'c.-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.pos[1:,4],'m.-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.pos[1:,5],'y.-', linewidth=plotLineWidth)
# plt.axis((11.5,16.5,-.2,.3))
plt.ylabel('Joint Postition (rad)')
plt.xlabel('Time (s)')
plt.legend(['Joint 1 pos', 'Joint 2 pos', 'Joint 3 pos', 'Joint 4 pos', 'Joint 5 pos', 'Joint 6 pos'])
plt.title('R gcode 02-04-2025')


######## Second Plot
fig1 = plt.figure(2)
plt.plot(test1command.time[2:-2], test1command.vel[2:-2,0], 'k+-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1command.time[2:-2], test1command.vel[2:-2,1], 'k+-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1command.time[2:-2], test1command.vel[2:-2,2], 'k+-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1command.time[2:-2], test1command.vel[2:-2,3], 'k+-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1command.time[2:-2], test1command.vel[2:-2,4], 'k+-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1command.time[2:-2], test1command.vel[2:-2,5], 'k+-', linewidth=plotLineWidth, label='_nolegend_')
plt.plot(test1states.time[1:],test1states.vel[1:,0],'b+-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.vel[1:,1],'g+-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.vel[1:,2],'r+-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.vel[1:,3],'c+-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.vel[1:,4],'m+-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.vel[1:,5],'y+-', linewidth=plotLineWidth)
# plt.axis((11.5,16.5,-.2,.3))
plt.ylabel('Joint Velocity (rad/s)')
plt.xlabel('Time (s)')
plt.legend(['Joint 1 vel', 'Joint 2 vel', 'Joint 3 vel', 'Joint 4 vel', 'Joint 5 vel', 'Joint 6 vel'])
plt.title('R gcode 02-04-2025')


######## Third Plot
fig1 = plt.figure(3)
plt.plot(cartPosesCommand[:,0], cartPosesCommand[:,1],'b+-', linewidth=plotLineWidth)
plt.plot(cartPosesStates[:,0], cartPosesStates[:,1],'r+-', linewidth=plotLineWidth*0.25)
plt.plot(GcodePoints[:,0], GcodePoints[:,1], 'go')
# plt.axis((11.5,16.5,-.2,.3))
plt.ylabel('y (mm)')
plt.xlabel('x (mm)')
plt.legend(['commanded', 'actual (forward Kin)', 'Gcode'])
plt.title('R gcode 02-04-2025')


plt.show()






