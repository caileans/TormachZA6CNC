import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))+"/../"))


import numpy as np
import DataTypes
import InverseKinematics


def AddFixed6DOF(trajectory):
    for i in range(len(trajectory)):
        trajectory[i].rot=np.array([0.0, 0.0,0.0])

    return trajectory

def Add6DofFrom5(trajectory, quadrant=2):
    j6ProjAngle_prev = 0
    for i in range(len(trajectory)):
        toolIJK = trajectory[i].toolVec
        print(toolIJK)
        toolIJK = toolIJK/np.linalg.norm(toolIJK)

        if toolIJK[2] == 0: #if the tool is horizontal
            j6IJK = np.array([0,0,-1.0])

            j6ProjAngle_prev = 0

        else:
            if toolIJK[0] >= 0:
                j6ProjAngle = 90*np.pi/180.0*toolIJK[1]

            else:
                j6ProjAngle = 180*np.pi/180.0*toolIJK[0] + 90*np.pi/180.0*toolIJK[1]

                if quadrant == 2:
                    pass
                elif quadrant == 1:
                    j6ProjAngle = -j6ProjAngle
                elif quadrant == 0:
                    if j6ProjAngle == 0: #use quadrant to decide
                        if toolIJK[1] < 0:
                            j6ProjAngle = -j6ProjAngle
                    else: # use previous sign to decide
                        if j6ProjAngle_prev < 0:
                            j6ProjAngle = -j6ProjAngle
            
            j6ProjAngle_prev = j6ProjAngle

            j6IJK = calcJ6IJK(toolIJK, j6ProjAngle)


        trajectory[i].rot=InverseKinematics.j62rpy(j6IJK)

    return trajectory


def calcJ6IJK(toolIJK, angle):
    j6IJK = np.array([0, 0, 0.0])
    j6IJK[0] = np.cos(angle)
    j6IJK[1] = np.sin(angle)
    j6IJK[2] = (-toolIJK[0] * j6IJK[0] - toolIJK[1] * j6IJK[1])/toolIJK[2]

    j6IJK = j6IJK/np.linalg.norm(j6IJK)

    return j6IJK

