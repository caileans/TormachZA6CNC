import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))+"/../"))


import numpy as np
import math
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
        toolIJK = toolIJK/np.linalg.norm(toolIJK)

        toolPos = trajectory[i].pos


############ quadrant based method:
        if toolIJK[2] == 0: #if the tool is horizontal
            j6IJK = np.array([0,0,-1.0])

            j6ProjAngle_prev = 0

        else:
            if toolIJK[0] >= 0:
                j6ProjAngle = 90*np.pi/180.0*toolIJK[1]

            else:
                j6ProjAngle = -180*np.pi/180.0*toolIJK[0] + 90*np.pi/180.0*toolIJK[1]

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

############ z axis alignment method:
            # j6ProjAngle =  np.atan2(toolPos[1], toolPos[0])


############ nik method:
        # j6ProjAngle =  np.atan2(toolPos[1], toolPos[0])

        # z=np.array([0,0,1])
        # r=np.array([math.cos(j6ProjAngle),math.sin(j6ProjAngle),0])
        # j6IJK=np.cross(toolIJK,np.cross(r,z))

            



        print(f"tool vec = {str(toolIJK)}    pos = {str(toolPos)}    proj angle = {str(j6ProjAngle)}   j6ijk  = {str(j6IJK)}   abcCailean = {str(calcABC(j6IJK, toolIJK))}")

        # trajectory[i].rot=InverseKinematics.j62rpy(j6IJK, toolIJK)
        trajectory[i].rot=calcABC(j6IJK, toolIJK)

    return trajectory


def calcJ6IJK(toolIJK, angle):
    j6IJK = np.array([0, 0, 0.0])
    j6IJK[0] = np.cos(angle)
    j6IJK[1] = np.sin(angle)
    j6IJK[2] = (-toolIJK[0] * j6IJK[0] - toolIJK[1] * j6IJK[1])/toolIJK[2]

    j6IJK = j6IJK/np.linalg.norm(j6IJK)

    return j6IJK

def calcABC(j6IJK, toolIJK):
    C = math.atan2(j6IJK[1], j6IJK[0])

    B = math.atan2(-j6IJK[2], np.sqrt(j6IJK[0]**2 + j6IJK[1]**2))

    q0 = np.array([0.0, 0.0, 0.0])
    q0[2] = math.cos(B)
    q0ij = math.sin(B)
    q0[0] = q0ij*math.cos(C)
    q0[1] = q0ij*math.sin(C)
    cross = np.cross(q0, toolIJK) #, q0)
    # print(f"q0: {str(q0)}   tijk: {str(toolIJK)}   dot: {str(np.dot(q0/np.linalg.norm(q0), toolIJK/np.linalg.norm(toolIJK)))}")
    A = math.acos(np.dot(q0/np.linalg.norm(q0), toolIJK/np.linalg.norm(toolIJK))*0.999999) * (np.sign(cross.dot(j6IJK)))
    # -.000000000000002
    # A = np.pi - np.copysign(math.asin(np.linalg.norm(cross)/(np.linealg.norm(q)*np.linalg.norm(q0))), -cross.dot(np.array([toolPose.i, toolPose.j, toolPose.k])))

    abc =  np.rad2deg(np.array([A, B, C]))
    # abc = np.array([A, B, C])
    return abc
