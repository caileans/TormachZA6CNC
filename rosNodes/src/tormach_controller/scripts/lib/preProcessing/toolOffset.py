import numpy as np
import DataTypes 
from math import pi
sys.path.append(os.path.abspath(__file__.split("preProcessing")[0]))
sys.path.append(os.path.abspath(__file__.split("preProcessing")[0]+'preProcessing'))
# sys.path.append(os.path.abspath(__file__.split("TormachZA6CNC")[0]+'TormachZA6CNC/Gcode/'))

def applyOffset(point, toolOffset):

	abc=point.rot*pi/180
	j6=np.matmul(ik.abc2R(abc),np.array([[1],[0],[0]]))[:,0]
	toolVec=point.toolVec/np.linalg.norm(point.toolVec)