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

hz = 80
robot=ik.tormachZA6();
pointList=gct.genTrajectory(__file__.split("TormachZA6CNC")[0]+'TormachZA6CNC/Gcode/5DOFTest.nc', a=30,hz=hz,feedRate=30,rapidFeed=30,toolFrameOffset=np.array([500,0,500]),pureRotVel=np.pi/5)

# set up arrays to save data here
jprev = np.zeros(6)
jprev[2]=np.pi/18;
jprev[4]=-np.pi/18

sols=[np.zeros(6)]
pick=[jprev];
c=0
for point in pointList:
	c+=1
	# returns all solutions
	newsol=ik.getIK(np.array(point.pos[0:3]),ik.abcToR(np.array(np.deg2rad(point.rot[0:3]))),robot)
	# pick.append(ik.chooseIK(pick[c-1],newsol,[2,2,2,2,2,2,0,6,6,6,6,6,6]))
	# pick.append(ik.chooseIK(pick[c-1],newsol,[2,2,2,2,2,2,0,4,4,4,4,4,4]))
	pick.append(ik.chooseIK(pick[c-1],newsol,[4,4,4,4,4,4,0,4,4,4,2,4,2]))
	# pick.append(ik.chooseIK(pick[c-1],newsol,[2,2,2,2,2,2,0,0,0,0,0,0,0]))
	temp=[]
	for j in newsol:
		temp.append(j[0])
	sols.append(np.array(temp))

pick=np.array(pick[1:])
# sols=np.array(sols[1:])

plt.figure(3)
# plt.plot(sols[:,:,5], '.k')
plt.plot(pick[:,:], '+-')
plt.legend(['1', '2', '3', '4', '5', '6'])

# gct.plotTrajectory(pointList, hz)

plt.show()
