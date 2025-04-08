import os, sys
sys.path.append(os.path.abspath(__file__.split("preProcessing")[0]))
sys.path.append(os.path.abspath(__file__.split("preProcessing")[0]+'preProcessing'))
sys.path.append(os.path.abspath(__file__.split("TormachZA6CNC")[0]+'TormachZA6CNC/Gcode/'))
import GCodeToTrajectory as gct
import numpy as np
import DataTypes 
from math import pi
import InverseKinematics as ik

'''
functions to apply offset to an array of TrajPoint data types between the tool tip and the "default" end effector 0 position
'''

def applyOffset(point, toolOffset):
	'''
	applies offset to single TrajPoint data type between the tool tip and the "default" end effector 0 position

	Inputs:
		point: a TrajPoint data type
		toolOffset: an 2 element array containing the offset along the j6 vector and the tool vector

	Outputs:
		point: a TrajPoint data type, but adjusted with the toolOffset
	'''
	abc=point.rot*pi/180
	j6=np.matmul(ik.abcToR(abc),np.array([[1],[0],[0]]))[:,0]
	# print(j6)
	toolVec=point.toolVec/np.linalg.norm(point.toolVec)
	point.pos+=toolVec*toolOffset[1]
	point.pos-=toolOffset[0]*j6
	return point

def toolOffset(points, toolOffset, nFadeIn = 0, nFadeOut = 0):
	'''
	applies offset to an array of TrajPoint data types between the tool tip and the "default" end effector 0 position

	Inputs:
		points: an array of TrajPoint data types
		toolOffset: an 2 element array containing the offset along the j6 vector and the tool vector
		nFadeIn: allows the offset to "fade in" over the first n points of the trajectory
		nFadeOut: allows the offset to "fade out" over the last n points of the trajectory

	Outputs:
		points: the same array as input, but adjusted with the toolOffset
	'''
	nPoints = len(points)
	toolOffset = np.array(toolOffset)
	for i in range(len(points)):
		if i < nFadeIn:
			points[i]=applyOffset(points[i],toolOffset*(i*1.0/nFadeIn))
			points[i].toolVec[1] += .176*(i*1.0/nFadeIn)
		elif i > (nPoints - nFadeOut):
			points[i]=applyOffset(points[i],toolOffset*(1-(i-(nPoints-nFadeOut*1.0))/nFadeOut))
			points[i].toolVec[1] += .176*(1-(i-(nPoints-nFadeOut*1.0))/nFadeOut)
		else:
			points[i]=applyOffset(points[i],toolOffset)
			points[i].toolVec[1] += .176
	return points

# pointList=gct.genTrajectory(__file__.split("TormachZA6CNC")[0]+'TormachZA6CNC/Gcode/5DOFTest.nc', a=30,hz=.5,feedRate=30,rapidFeed=30,toolFrameOffset=np.array([500,0,500]),pureRotVel=np.pi/5)
# print(pointList)
# pointList=toolOffset(pointList,[1,23])
# print(pointList)