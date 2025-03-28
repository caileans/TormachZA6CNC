import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))+"/../"))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))+"/../preProcessing"))
# print(str(__file__))
sys.path.append(os.path.abspath(__file__.split("test")[0]+'lib'))
sys.path.append(os.path.abspath(__file__.split("test")[0]+'lib/preProcessing'))
sys.path.append(os.path.abspath(__file__.split("TormachZA6CNC")[0]+'TormachZA6CNC/Gcode/'))
from ik_geo import Robot # pip install ik-geo
import InverseKinematics as ik
import matplotlib.pyplot as plt
import GCodeToTrajectory as gct
import numpy as np
import general_robotics_toolbox as grtb

'''Script for "previewing" (in a plot) the joint and cartesian space trajectory generated from a gcode file'''


# file = 'F360Test1.nc'
# file = '5DOFTest.nc'
file = 'WAAM_wall_2025.nc'
hz = 1
robot=ik.tormachZA6();
# pointList=gct.genTrajectory(__file__.split("TormachZA6CNC")[0]+'TormachZA6CNC/Gcode/'+file, a=30,hz=hz,feedRate=5,rapidFeed=5,toolFrameOffset=np.array([500,100,500]),pureRotVel=np.pi/20, tOffset=[0, 20])
pointList=gct.genTrajectory(__file__.split("TormachZA6CNC")[0]+'TormachZA6CNC/Gcode/'+file, a=30,hz=hz,feedRate=30,rapidFeed=10,toolFrameOffset=np.array([500,0,500]),pureRotVel=np.pi/20, tOffset=[0, 20])
# pointList=gct.genTrajectory(__file__.split("TormachZA6CNC")[0]+'TormachZA6CNC/Gcode/'+file, a=30,hz=hz,feedRate=5,rapidFeed=5,toolFrameOffset=np.array([500,0,500]),pureRotVel=np.pi/20, tOffset=[0, 20])

# set up arrays to save data here
jprev = np.zeros(6)
jprev[2]=np.pi/18;
jprev[4]=-np.pi/18

sols=[np.zeros(6)]
pick=[jprev];
c=0
for point in pointList:
	c+=1
	# returns all solutions np.transpose(ik.abcToR(np.array(np.deg2rad(point.rot[0:3]))))
	newsol=ik.getIK(point.pos,np.transpose(grtb.rpy2R(np.deg2rad(point.rot))),robot)
	# pick.append(ik.chooseIK(pick[c-1],newsol,[2,2,2,2,2,2,0,6,6,6,6,6,6]))
	# pick.append(ik.chooseIK(pick[c-1],newsol,[2,2,2,2,2,2,0,4,4,4,4,4,4]))
	# pick.append(ik.chooseIK(pick[c-1],newsol,[2,2,2,2,2,2,0,2,2,2,2,2,2]))
	# pick.append(ik.chooseIK(pick[c-1],newsol,[0,0,0,0,0,0,0,0,0,0,100000000000,0,0]))
	pick.append(ik.chooseIK(pick[c-1],newsol,[20,20,20,20,20,20,0,0,2,2,20,2,20]))
	# pick.append(ik.runIK(np.array([point.pos[0],point.pos[1],point.pos[2],point.rot[0],point.rot[1],point.rot[2]]),pick[c-1],robot))
	temp=[]
	for j in newsol:
		temp.append(j[0])
	sols.append(np.array(temp))

pick=np.array(pick[0:])
# sols=np.array(sols[1:])

plt.figure(3)
# plt.plot(sols[:,:,3], '.k', label='_nolegend_')
plt.plot(pick[:,:], '+-')
plt.legend(['1', '2', '3', '4', '5', '6'])
plt.xlabel("trajectory point")
plt.ylabel("joint angle (rad)")
plt.title("ik-geo solutions for "+file)

gct.plot3DTrajectory(pointList, hz, nmin=10, nmaxOffset=10, step=1, titleFile = file)

plt.show()
