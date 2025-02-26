import os, sys
sys.path.append(os.path.abspath(__file__.split("preProcessing")[0]))
sys.path.append(os.path.abspath(__file__.split("preProcessing")[0]+'preProcessing'))
sys.path.append(os.path.abspath(__file__.split("TormachZA6CNC")[0]+'TormachZA6CNC/Gcode/'))
import GCodeToTrajectory as gct
import numpy as np
import DataTypes 
from math import pi
import InverseKinematics as ik

def applyOffset(point, toolOffset):

	abc=point.rot*pi/180
	j6=np.matmul(ik.abcToR(abc),np.array([[1],[0],[0]]))[:,0]
	# print(j6)
	toolVec=point.toolVec/np.linalg.norm(point.toolVec)
	point.pos+=toolVec*toolOffset[1]
	point.pos-=toolOffset[0]*j6
	return point

def toolOffset(points, toolOffset, nFadeIn = 0, nFadeOut = 0):
	nPoints = len(points)
	toolOffset = np.array(toolOffset)
	for i in range(len(points)):
		if i < nFadeIn:
			points[i]=applyOffset(points[i],toolOffset*(i*1.0/nFadeIn))
		elif i > (nPoints - nFadeOut):
			points[i]=applyOffset(points[i],toolOffset*(1-(i-(nPoints-nFadeOut*1.0))/nFadeOut))
		else:
			points[i]=applyOffset(points[i],toolOffset)
	return points

# pointList=gct.genTrajectory(__file__.split("TormachZA6CNC")[0]+'TormachZA6CNC/Gcode/5DOFTest.nc', a=30,hz=.5,feedRate=30,rapidFeed=30,toolFrameOffset=np.array([500,0,500]),pureRotVel=np.pi/5)
# print(pointList)
# pointList=toolOffset(pointList,[1,23])
# print(pointList)