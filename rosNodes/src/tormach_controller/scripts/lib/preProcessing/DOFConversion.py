import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))+"/../"))


import numpy as np
import math
import DataTypes
import InverseKinematics


def AddFixed6DOF(trajectory):
    '''
    adds 6dof rotation information to an array of TrajPoint data types

    Inputs:
        trajectory: an array of TrajPoint data types

    Outputs:
        trajectory: the same array as the input, but with the .rot field filled out with a fixed upright orientation
    '''
    for i in range(len(trajectory)):
        trajectory[i].rot=np.array([0.0, 0.0,0.0])

    return trajectory

def Add6DofFrom5(trajectory, quadrant=2):
    '''
    adds 6dof rotation information to an array of TrajPoint data types

    Inputs:
        trajectory: an array of TrajPoint data types
        quadrant: experimental, used in computing the 6dof orientation. choses which qudrant the tool is working in. 1, 2, or 0 for automatic

    Outputs:
        trajectory: the same array as the input, but with the .rot field filled out with a computed 6dof orientation
    '''
    j6ProjAngle_prev = 0
    for i in range(len(trajectory)):
        toolIJK = trajectory[i].toolVec
        toolIJK = toolIJK/np.linalg.norm(toolIJK)

        toolPos = trajectory[i].pos


# ############ quadrant based method:
#         if toolIJK[2] == 0: #if the tool is horizontal
#             j6IJK = np.array([0,0,-1.0])

#             j6ProjAngle_prev = 0

#         else:
#             if toolIJK[0] >= 0:
#                 j6ProjAngle = 90*np.pi/180.0*toolIJK[1]

#             else:
#                 j6ProjAngle = -180*np.pi/180.0*toolIJK[0] + 90*np.pi/180.0*toolIJK[1]

#                 if quadrant == 2:
#                     pass
#                 elif quadrant == 1:
#                     j6ProjAngle = -j6ProjAngle
#                 elif quadrant == 0:
#                     if j6ProjAngle == 0: #use quadrant to decide
#                         if toolIJK[1] < 0:
#                             j6ProjAngle = -j6ProjAngle
#                     else: # use previous sign to decide
#                         if j6ProjAngle_prev < 0:
#                             j6ProjAngle = -j6ProjAngle
            
#             j6ProjAngle_prev = j6ProjAngle

#             j6IJK = calcJ6IJK(toolIJK, j6ProjAngle)


# ########### quadrant based method #2: WARNING: this method has discontinuities between certain poses
#         toolProjAngle = math.atan2(toolIJK[1], toolIJK[0])
#         toolProjMag = np.sqrt(toolIJK[1]**2+toolIJK[0]**2)
#         if toolIJK[2] == 0: # and toolIJK[1] == 0: #if the tool is horizontal
#             # print("tool horizontal")
#             j6IJK = np.array([abs(toolIJK[1])*np.sqrt(1-abs(toolIJK[0])**2),-toolIJK[0]*np.sign(toolIJK[1])*np.sqrt(1-abs(toolIJK[0])**2),-abs(toolIJK[0])])

#             j6ProjAngle_prev = 0

#         else:
#             # j6AnglePosComp = math.atan2(toolPos[1], toolPos[0])
#             j6AnglePosComp = math.atan2(toolPos[1], toolPos[0])
            

#             if toolIJK[0] >= 0:
#                 # j6ProjAngle = 90*np.pi/180.0*toolIJK[1]
#                 j6ProjAngle = j6AnglePosComp*(1-abs(toolIJK[1])) #(-1 if toolIJK[1] > 0 else 1)
#                 # j6ProjAngle = j6AnglePosComp*(1-abs(np.cos(toolProjAngle)))
#                 # j6ProjAngle = j6AnglePosComp*(np.sin(toolProjAngle))
#                 # j6ProjAngle = 0.0

#                 if toolIJK[2] < 0:
#                     j6ProjAngle -= np.pi*abs(toolIJK[0])*(1 if toolIJK[1]>0 else -1)


#             else:
#                 j6AngleIJKComp = -180*np.pi/180.0*toolIJK[0]# + 90*np.pi/180.0*toolIJK[1]
#                 # j6AngleIJKComp = -180*np.pi/180.0*np.cos(toolProjAngle)#*toolProjMag#toolIJK[0]# + 90*np.pi/180.0*toolIJK[1]

#                 if quadrant == 2:
#                     pass
#                 elif quadrant == 1:
#                     j6AngleIJKComp = -j6AngleIJKComp
#                 elif quadrant == 0:
#                     print("here1!")
#                     if j6ProjAngle == 0: #use quadrant to decide
#                         if toolIJK[1] < 0:
#                             j6AngleIJKComp = -j6AngleIJKComp
#                     else: # use previous sign to decide
#                         if j6ProjAngle_prev < 0:
#                             j6AngleIJKComp = -j6AngleIJKComp
            
#                 j6ProjAngle = (1-abs(toolIJK[0]))*j6AnglePosComp*(1-abs(toolIJK[1])) + j6AngleIJKComp*(1 if toolIJK[1]>=0 else -1)
#                 # j6ProjAngle = (1-abs(toolIJK[0]))*j6AnglePosComp*(1-abs(toolIJK[1])) + j6AngleIJKComp#*toolIJK[1]#(1 if toolIJK[1]>=0 else -1)
#                 # j6ProjAngle = j6AngleIJKComp#*toolIJK[1]#(1 if toolIJK[1]>=0 else -1)
#                 # j6ProjAngle = j6AngleIJKComp*(1 if toolIJK[2]>=0 else -1)*(1 if toolIJK[1]>=0 else -1)
#                 # j6ProjAngle = j6AngleIJKComp*(1 if toolIJK[1]>=0 else -1) #THIS ONE WORKS ish
#                 # j6ProjAngle = j6AngleIJKComp*np.sin(toolProjAngle)
#                 # j6ProjAngle = (1-abs(toolIJK[0]))*j6AnglePosComp*(1-abs(toolIJK[1])) + j6AngleIJKComp*np.sin(toolProjAngle)

#                 if toolIJK[2] < 0:
#                     # j6ProjAngle += np.pi *(1-abs(toolIJK[1]))#*(1 if toolIJK[2] == 0 else -np.sign(toolIJK[2]))
#                     j6ProjAngle -= np.pi*abs(toolIJK[0])*(1 if toolIJK[1]>0 else -1)
#                     # j6ProjAngle += np.pi *abs(toolIJK[0])

#             # if j6ProjAngle < 0:
#             #     j6ProjAngle += 2*np.pi

#             j6ProjAngle_prev = j6ProjAngle

#             j6IJK = calcJ6IJK(toolIJK, j6ProjAngle)


########### quadrant based method #3: does not "flip" j6 at q 3 and 4

        toolProjAngle = math.atan2(toolIJK[1], toolIJK[0])
        toolProjMag = np.sqrt(toolIJK[1]**2+toolIJK[0]**2)
        if toolIJK[2] == 0: # and toolIJK[1] == 0: #if the tool is horizontal
            # print("tool horizontal")
            j6IJK = np.array([abs(toolIJK[1])*np.sqrt(1-abs(toolIJK[0])**2),-toolIJK[0]*np.sign(toolIJK[1])*np.sqrt(1-abs(toolIJK[0])**2),-abs(toolIJK[0])])

            j6ProjAngle_prev = 0

        else:
            # j6AnglePosComp = math.atan2(toolPos[1], toolPos[0])
            j6AnglePosComp = math.atan2(toolPos[1], toolPos[0])
            

            # if toolIJK[0] >= 0:
                # j6ProjAngle = 90*np.pi/180.0*toolIJK[1]
            j6ProjAngle = j6AnglePosComp*(1-abs(toolIJK[1])) #(-1 if toolIJK[1] > 0 else 1)
                # j6ProjAngle = j6AnglePosComp*(1-abs(np.cos(toolProjAngle)))
                # j6ProjAngle = j6AnglePosComp*(np.sin(toolProjAngle))
                # j6ProjAngle = 0.0

                # if toolIJK[2] < 0:
                #     j6ProjAngle -= np.pi*abs(toolIJK[0])*(1 if toolIJK[1]>0 else -1)


            # else:
            #     j6AngleIJKComp = -180*np.pi/180.0*toolIJK[0]# + 90*np.pi/180.0*toolIJK[1]
            #     # j6AngleIJKComp = -180*np.pi/180.0*np.cos(toolProjAngle)#*toolProjMag#toolIJK[0]# + 90*np.pi/180.0*toolIJK[1]

            #     if quadrant == 2:
            #         pass
            #     elif quadrant == 1:
            #         j6AngleIJKComp = -j6AngleIJKComp
            #     elif quadrant == 0:
            #         print("here1!")
            #         if j6ProjAngle == 0: #use quadrant to decide
            #             if toolIJK[1] < 0:
            #                 j6AngleIJKComp = -j6AngleIJKComp
            #         else: # use previous sign to decide
            #             if j6ProjAngle_prev < 0:
            #                 j6AngleIJKComp = -j6AngleIJKComp
            
            #     j6ProjAngle = (1-abs(toolIJK[0]))*j6AnglePosComp*(1-abs(toolIJK[1])) + j6AngleIJKComp*(1 if toolIJK[1]>=0 else -1)
            #     # j6ProjAngle = (1-abs(toolIJK[0]))*j6AnglePosComp*(1-abs(toolIJK[1])) + j6AngleIJKComp#*toolIJK[1]#(1 if toolIJK[1]>=0 else -1)
            #     # j6ProjAngle = j6AngleIJKComp#*toolIJK[1]#(1 if toolIJK[1]>=0 else -1)
            #     # j6ProjAngle = j6AngleIJKComp*(1 if toolIJK[2]>=0 else -1)*(1 if toolIJK[1]>=0 else -1)
            #     # j6ProjAngle = j6AngleIJKComp*(1 if toolIJK[1]>=0 else -1) #THIS ONE WORKS ish
            #     # j6ProjAngle = j6AngleIJKComp*np.sin(toolProjAngle)
            #     # j6ProjAngle = (1-abs(toolIJK[0]))*j6AnglePosComp*(1-abs(toolIJK[1])) + j6AngleIJKComp*np.sin(toolProjAngle)

            #     # if toolIJK[2] < 0:
            #     #     # j6ProjAngle += np.pi *(1-abs(toolIJK[1]))#*(1 if toolIJK[2] == 0 else -np.sign(toolIJK[2]))
            #     #     j6ProjAngle -= np.pi*abs(toolIJK[0])*(1 if toolIJK[1]>0 else -1)
            #     #     # j6ProjAngle += np.pi *abs(toolIJK[0])


            j6ProjAngle_prev = j6ProjAngle

            j6IJK = calcJ6IJK(toolIJK, j6ProjAngle)

############ z axis alignment method:
            # j6ProjAngle =  np.atan2(toolPos[1], toolPos[0])


############ nik method:
        # j6ProjAngle =  np.atan2(toolPos[1], toolPos[0])

        # z=np.array([0,0,1])
        # r=np.array([math.cos(j6ProjAngle),math.sin(j6ProjAngle),0])
        # j6IJK=np.cross(toolIJK,np.cross(r,z))

            
        # j6IJK = np.array([0, 0, -1.0])


        # print(f"tool vec = {str(toolIJK)}    pos = {str(toolPos)}    proj angle = {str(j6ProjAngle)}   j6ijk  = {str(j6IJK)}   abcCailean = {str(calcABC(j6IJK, toolIJK))}")

        # trajectory[i].rot=InverseKinematics.j62rpy(j6IJK, toolIJK)
        trajectory[i].rot=calcABC(j6IJK, toolIJK)

    return trajectory


def calcJ6IJK(toolIJK, angle):
    '''
    calculates the vector along the j6 rotation axis from the tool vector and the projected j6 vector angle

    Inputs:
        toolIJK: the tool orientation vector (from the tool tip to the shank)
        angle: the angle (ccw from +x) of the j6 vector projected onto the XY plane

    Outputs:
        j6IJK: the vector along the j6 rotation axis (pointing towards the end effector)
    '''
    j6IJK = np.array([0, 0, 0.0])
    j6IJK[0] = np.cos(angle)
    j6IJK[1] = np.sin(angle)
    j6IJK[2] = (-toolIJK[0] * j6IJK[0] - toolIJK[1] * j6IJK[1])/toolIJK[2]

    j6IJK = j6IJK/np.linalg.norm(j6IJK)

    return j6IJK

def calcABC(j6IJK, toolIJK):
    '''
    calculates ABC Euler angles from the tool vector and the j6 vector

    Inputs:
        j6IJK: the vector along the j6 rotation axis
        toolIJK: the tool vector (from the tool tip to the shank)

    Outputs:
        abc: the Euler angles describing the rotation of the end effector
    '''
    C = math.atan2(j6IJK[1], j6IJK[0])
    if j6IJK[1] == 0 and j6IJK[0] == 0:
        C = math.atan2(toolIJK[1], toolIJK[0])

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
