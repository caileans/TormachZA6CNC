import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt


import TrajectoryPlanner as tp
import ReadROSLogFile as rFile


######## Read the data from the files
test1command = rFile.JointState([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
test1states  = rFile.JointState([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
test2command = rFile.JointState([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
test2states  = rFile.JointState([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
# test3command = rFile.JointState([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
# test3states  = rFile.JointState([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
# test4command = rFile.JointState([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
# test4states  = rFile.JointState([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])

test1InitTime = 1737602693.0
test2InitTime = 1737602888.0
# test3InitTime = 1737603596.0
# test4InitTime = 1737603821.0

rFile.readJointCommandFile('data/velocitytesting/test1command_2_6_25_OS_1.txt', test1command, initialTime=test1InitTime)
rFile.readJointCommandFile('data/velocitytesting/test1command_2_6_25_OS_2.txt', test2command, initialTime=test2InitTime)
# rFile.readJointCommandFile('data/test1joints_2_6_25_OS_1.txt', test3command, initialTime=test3InitTime)
# rFile.readJointCommandFile('data/test1joints_2_6_25_OS_1.txt', test4command, initialTime=test4InitTime)

rFile.readJointStatesFile('data/velocitytesting/test1joints_2_6_25_OS_1.txt', test1states, initialTime=test1InitTime)
rFile.readJointStatesFile('data/velocitytesting/test1joints_2_6_25_OS_2.txt', test2states, initialTime=test2InitTime)
# rFile.readJointStatesFile('data/1_22_25_test3_states.txt', test3states, initialTime=test3InitTime)
# rFile.readJointStatesFile('data/1_22_25_test4_states.txt', test4states, initialTime=test4InitTime)


######## Generate desired velocity profile:
# hz = 20
# amax=8#rad/s/s
# ta=.25 #s
# vmax= 2 #rad/s
# tm =1.2 #s
# overshoot = 1
# test1vel=np.array([]);
# for i in range(9):
# 	i+=2
# 	_, vel = tp.genpath(10*i, amax, ta, vmax, tm, overshoot)
# 	vel=np.append(vel,[0,0])
# 	test1vel=np.append(test1vel,vel)
# amax = 0.3
# ta = 0.25
# vmax = 0.3
# tm = 5
# overshoot = 1
# test3vel=np.array([]);
# for i in range(9):
# 	i+=2
# 	_, vel = tp.genpath(10*i, amax, ta, vmax, tm, overshoot)
# 	vel=np.append(vel,[0,0])
# 	test3vel=np.append(test3vel,vel)
# print(test1vel)

plotLineWidth = 0.5

######## First Plot
fig1 = plt.figure(1)
plt.plot(test1command.time[1:], test1command.pos[1:, 0], 'k.-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.pos[1:,0],'b.-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.pos[1:,1],'g.-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],-test1states.pos[1:,2],'r.-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.pos[1:,3],'c.-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.pos[1:,4],'m.-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.pos[1:,5],'y.-', linewidth=plotLineWidth)
#plt.plot(test1command.time[1:], test1vel, 'k+-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.vel[1:,0],'b+-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.vel[1:,1],'g+-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],-test1states.vel[1:,2],'r+-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.vel[1:,3],'c+-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.vel[1:,4],'m+-', linewidth=plotLineWidth)
plt.plot(test1states.time[1:],test1states.vel[1:,5],'y+-', linewidth=plotLineWidth)
# plt.axis((11.5,16.5,-.2,.3))
plt.ylabel('Joint Postition (rad) / Velocity (rad/s)')
plt.xlabel('Time (s)')
plt.legend(['Commanded pos', 'Joint 1 pos', 'Joint 2 pos', 'Joint 3 pos', 'Joint 4 pos', 'Joint 5 pos', 'Joint 6 pos', 'Theoretical vel', 'Joint 1 vel', 'Joint 2 vel', 'Joint 3 vel', 'Joint 4 vel', 'Joint 5 vel', 'Joint 6 vel'])
plt.title('Test 1: 8rad/sec2, 2rad/s, no overshoot')
#fig1.show()



######## Second Plot
fig2 = plt.figure(2)
plt.plot(test2command.time[1:], test1command.pos[1:, 0], 'k.-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],test2states.pos[1:,0],'b.-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],test2states.pos[1:,1],'g.-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],-test2states.pos[1:,2],'r.-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],test2states.pos[1:,3],'c.-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],test2states.pos[1:,4],'m.-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],test2states.pos[1:,5],'y.-', linewidth=plotLineWidth)
#plt.plot(test2command.time[1:], test1vel, 'k+-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],test2states.vel[1:,0],'b+-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],test2states.vel[1:,1],'g+-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],-test2states.vel[1:,2],'r+-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],test2states.vel[1:,3],'c+-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],test2states.vel[1:,4],'m+-', linewidth=plotLineWidth)
plt.plot(test2states.time[1:],test2states.vel[1:,5],'y+-', linewidth=plotLineWidth)
# plt.axis((11.5,16.5,-.2,.3))
plt.ylabel('Joint Postition (rad) / Velocity (rad/s)')
plt.xlabel('Time (s)')
plt.legend(['Commanded pos', 'Joint 1 pos', 'Joint 2 pos', 'Joint 3 pos', 'Joint 4 pos', 'Joint 5 pos', 'Joint 6 pos', 'Theoretical vel', 'Joint 1 vel', 'Joint 2 vel', 'Joint 3 vel', 'Joint 4 vel', 'Joint 5 vel', 'Joint 6 vel'])
plt.title('Test 2: 8rad/sec2, 2rad/s, 2x overshoot')
#fig2.show()

plt.show()


# ######## Third Plot
# fig3 = plt.figure(3)
# plt.plot(test3command.time[1:], test3command.pos[1:, 0], 'k.-', linewidth=plotLineWidth)
# plt.plot(test3states.time[1:],test3states.pos[1:,0],'b.-', linewidth=plotLineWidth)
# plt.plot(test3states.time[1:],test3states.pos[1:,1],'g.-', linewidth=plotLineWidth)
# plt.plot(test3states.time[1:],-test3states.pos[1:,2],'r.-', linewidth=plotLineWidth) 
# plt.plot(test3states.time[1:],test3states.pos[1:,3],'c.-', linewidth=plotLineWidth)
# plt.plot(test3states.time[1:],test3states.pos[1:,4],'m.-', linewidth=plotLineWidth)
# plt.plot(test3states.time[1:],test3states.pos[1:,5],'y.-', linewidth=plotLineWidth)
# plt.plot(test3command.time[1:], test3vel, 'k+-', linewidth=plotLineWidth)
# plt.plot(test3states.time[1:],test3states.vel[1:,0],'b+-', linewidth=plotLineWidth)
# plt.plot(test3states.time[1:],test3states.vel[1:,1],'g+-', linewidth=plotLineWidth)
# plt.plot(test3states.time[1:],-test3states.vel[1:,2],'r+-', linewidth=plotLineWidth)
# plt.plot(test3states.time[1:],test3states.vel[1:,3],'c+-', linewidth=plotLineWidth)
# plt.plot(test3states.time[1:],test3states.vel[1:,4],'m+-', linewidth=plotLineWidth)
# plt.plot(test3states.time[1:],test3states.vel[1:,5],'y+-', linewidth=plotLineWidth)
# # plt.axis((11.5,16.5,-.2,.3))
# plt.ylabel('Joint Postition (rad) / Velocity (rad/s)')
# plt.xlabel('Time (s)')
# plt.legend(['Commanded pos', 'Joint 1 pos', 'Joint 2 pos', 'Joint 3 pos', 'Joint 4 pos', 'Joint 5 pos', 'Joint 6 pos', 'Theoretical vel', 'Joint 1 vel', 'Joint 2 vel', 'Joint 3 vel', 'Joint 4 vel', 'Joint 5 vel', 'Joint 6 vel'])
# plt.title('Test 3: 0.3rad/sec2, 0.3rad/s, no overshoot')
# fig3.show()




# ######## Forth Plot
# fig4 = plt.figure(4)
# plt.plot(test4command.time[1:], test3command.pos[1:, 0], 'k.-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],test4states.pos[1:,0],'b.-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],test4states.pos[1:,1],'g.-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],-test4states.pos[1:,2],'r.-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],test4states.pos[1:,3],'c.-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],test4states.pos[1:,4],'m.-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],test4states.pos[1:,5],'y.-', linewidth=plotLineWidth)
# plt.plot(test4command.time[1:], test3vel, 'k+-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],test4states.vel[1:,0],'b+-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],test4states.vel[1:,1],'g+-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],-test4states.vel[1:,2],'r+-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],test4states.vel[1:,3],'c+-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],test4states.vel[1:,4],'m+-', linewidth=plotLineWidth)
# plt.plot(test4states.time[1:],test4states.vel[1:,5],'y+-', linewidth=plotLineWidth)
# # plt.axis((11.5,16.5,-.2,.3))
# plt.ylabel('Joint Postition (rad) / Velocity (rad/s)')
# plt.xlabel('Time (s)')
# plt.legend(['Commanded pos', 'Joint 1 pos', 'Joint 2 pos', 'Joint 3 pos', 'Joint 4 pos', 'Joint 5 pos', 'Joint 6 pos', 'Theoretical vel', 'Joint 1 vel', 'Joint 2 vel', 'Joint 3 vel', 'Joint 4 vel', 'Joint 5 vel', 'Joint 6 vel'])
# plt.title('Test 2: 0.3rad/sec2, 0.3rad/s, 2x overshoot')
# fig4.show()



# while True:
# 	pass



