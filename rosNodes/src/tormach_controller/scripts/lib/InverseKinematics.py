import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ik_geo import Robot # pip install ik-geo
import numpy as np
import general_robotics_toolbox as grtb
from math import pi, cos, acos, sin, copysign, atan2, asin
import copy



def getIK(position, Rotation,robot):
    """ calculates the set of IK solutions using the ik_geo toolbox

    Inputs:
        position - an array of length 3 that contains the desired x, y, z corrdinates of the end effector
        Rotation - the rotation matrix that describes the orientation of the end effector
        robot - an ik_geo Robot type describing the robot arm
    Output:
        the set of ik solutions calculated by ik_geo""" 

    sols = robot.get_ik_sorted(Rotation,[position[0],position[1],position[2]])

    sols = applyJointLimits(sols, 6, 360)
    
    
    # sols = applyJointLimits(sols, 4, 270) tormach doesn't throw error, but just moves to 180 and won't move past


    return  sols

def applyJointLimits(sols, joint, limit):

    limit = limit*np.pi/180

    if limit == 180*np.pi/180:
        return sols

    numSols = len(sols)

    #TODO: test this part
    if limit < 180*np.pi/180: 
        for i in range(numSols):
            if abs(sols[i][0][joint-1]) > limit:
                sols[i][0][joint-1].pop(i)
        
        return sols

    #######this version creats duplicate entries, so is less efficient to sort later.
    # # double the number of sols to account for >180 limits
    # newSols = copy.deepcopy(sols)
    # newSols.extend(sols)
    # # print(newSols)
    # # newSols[numSols+7][0][5] -= 360*np.pi/180
    # # print(newSols)
    # for i in range(numSols):
    #     if newSols[numSols+i][0][joint-1] > 0:
    #         if abs(newSols[numSols+i][0][joint-1]-360*np.pi/180) < limit:
    #             newSols[numSols+i][0][joint-1] -= 360*np.pi/180
    #     elif newSols[numSols+i][0][joint-1] < 0:
    #         if abs(newSols[numSols+i][0][joint-1]+360*np.pi/180) < limit:
    #             newSols[numSols+i][0][joint-1] += 360*np.pi/180

    # return newSols

    ########this version is more efficient, but can be hard to plot due to different numbers of solutions at each point
    for i in range(numSols):
        if sols[i][0][joint-1] > 0:
            newSol = sols[i][0][joint-1] - 360*np.pi/180
        elif sols[i][0][joint-1] < 0:
            newSol = sols[i][0][joint-1] + 360*np.pi/180
        else:
            continue

        if abs(newSol) < limit:
            sols.append(copy.deepcopy(sols[i]))
            sols[-1][0][joint-1] = newSol
    return sols

def abcToR(abc):
    """uses the general robotics toolbox from rpi to calculate the rotation matrix from the static euler angles

    Inputs:
        abc - an array of length 3 that contains the alpha, beta, and gamma euler angles in radians
    Output:
        a 3x3 rotation matrix describing the orientation"""
    # return (grtb.rpy2R([abc[-1],abc[-2],abc[-3]]))
    return np.matmul(grtb.rot(np.array([0,0,1.0]),abc[2]),np.matmul(grtb.rot(np.array([0,1.0,0]),abc[1]),grtb.rot(np.array([1.0,0,0]),abc[0])))

def chooseIK(r0, sols, w):
    """chooses the best ik solution by minimizing the error in the solution and change from joint position r0

    Inputs:
        r0 - an np array of length 6 that describes the previous joint state
        sols - the solution set returned by ik_geo
        w - an array of legnth 13 that contains the weighing factors for each state
    Output:
        a np array of length 6 containing the best IK solution"""
        
    minerror=sols[0][1];
    i=0;
    minindex=0;
    minval=102390239023
    # print(r0)
    # fkrobot=tormachZA6fk();

    for col in sols:
        newsol=np.array(col[0])
        # newvalue=w[-1]*(col[1]-minerror)
        newvalue=0
        # print(np.shape(newsol)[0])

        for j in range(np.shape(newsol)[0]):
            # if (j==3 or j==5) and newsol[4]**2<.0004:
                # print(newsol)
                # w[7+j]=100
            newvalue+=w[j]**((newsol[j]-r0[j])**2)+w[7+j]**(newsol[j]**2)
        # print(newvalue)
        # newvalue=(newsol[0]-r0[0])**2+(newsol[5]-r0[5])**2
        if newvalue<minval:
            minval=newvalue
            minindex=i;
        i+=1
    return np.array(sols[minindex][0])


def runIK (r, r0, ikrobot, w=[20,20,20,20,20,20,0,2,2,2,2,2,0]):
    """ calculates and chooses the best inverse kinematics solution 

    inputs: 
        r - a numpy array of length 6 with the entries [x pose, y pose, z pose, a, b, c] where a b and c are the static frame roll, pitch, and yaw orientation in degrees
        r0 - a np array of length 6 containing the previous joint angles in radians
        ikrobot - an ik_geo Robot type describing the robot arm
        w - the weighting factor of the deviations 1x13 array of change in j1-j6 then ik solution error then absolute j1-j6
    output:
        a np array of length 6 containing the selected joint angles"""

    w=np.array(w)
    abc=[r[-3]*pi/180,r[-2]*pi/180,r[-1]*pi/180];
    # print(r0)
    R=abcToR(abc)
    # print(R)
    sols=getIK(r,np.transpose(R), ikrobot)
    return chooseIK(r0,sols,w)#-np.array([0,0,0,0,0,10*np.pi/180.0])


def tormachZA6():
    """initializes the IK solver for the tormach ZA6 robotic arm

    Inputs:
    Output:
        an ik_geo Robot type describing the robot arm """
    H=np.array([[0,0,0,1,0,1],[0,1,1,0,1,0],[1,0,0,0,0,0]])
    H=np.transpose(H)
    P=np.array([[.0,.025,.0,.123+.2965,.0,.0,.2175-.1],[.0,.0,.0,.0,.0,.0,.0],[.279,.171,.454,.035,.0,.0,.0]])*1000.0 
    P=np.transpose(P)
    # print(P)
    robot=Robot.spherical_two_parallel(H,P)
    return robot


def tormachZA6fk():
    """initializes the IK solver for the tormach ZA6 robotic arm

    Inputs:
    Output:
        an general robotics toolbox Robot type describing the robot arm """
    H=np.array([[0,0,0,1,0,1],[0,1,1,0,1,0],[1,0,0,0,0,0]])
    # H=np.transpose(H)
    P=np.array([[0,.025,0,.123+.2965,0,0,.1+.1175-.1],[0,0,0,0,0,0,0],[.279,.171,.454,.035,0,0,0]])*1000 #approximated without 1mm offsets
    # P=np.transpose(P)
    # print(np.shape(P))
    robot=grtb.Robot(H,P,[0,0,0,0,0,0])
    return robot


# def j62R(j6):

#     j6/=np.linalg.norm(j6)
#     x=np.array([1,0,0])
#     theta=acos(np.dot(j6,x))
#     axis=np.cross(x,j6)
#     R=cos(theta)*np.eye(3)+sin(theta)*np.cross(np.eye(3),axis)+(1-cos(theta))*np.outer(axis,axis)
#     return R
# def tool2R(j6,tool,rj6):
#     tool/=np.linalg.norm(tool)
#     # print(tool)
#     z=np.matmul(rj6,np.array([[0],[0],[1]]))
#     # print(z)
#     z=np.array(z[:,0])
#     # print(z)
#     # z=np.array([0,0,1])
#     theta=acos(np.dot(tool,z))
#     # print(theta)
#     # axis=np.array([1,0,0])*copysign(1,np.dot(np.cross(z,tool),j6))
#     # R=cos(theta)*np.eye(3)+sin(theta)*np.cross(np.eye(3),axis)+(1-cos(theta))*np.outer(axis,axis)
#     return theta*copysign(1,np.dot(np.cross(z,tool),j6))

# def R2rpy(R):
#     # print(R)
#     # print(np.linalg.norm(R[0:2,0]))
#     # print(R[0:2,0])
#     abc=grtb.R2rpy(R)
#     # b=asin(-R[0,2])
#     # print(abc)
#     # assert np.linalg.norm(R[0:2,0]) > np.finfo(float).eps * 10.0, "Singular rpy requested"
#     return np.array([abc[-1],abc[-2],abc[-3]])

# def j62rpy(j6,toolVector):
#     j6/=np.linalg.norm(j6)
#     x=np.array([1,0,0])
#     theta=acos(np.dot(j6,x))
#     axis=np.cross(x,j6)
#     bc=axang2bg(axis,theta)
#     rj6=j62R(j6)
#     # c=R2rpy(rj6)
#     return np.array([tool2R(j6,toolVector,rj6), bc[0],bc[1]])*180/pi

def getR(axis, angle):
    theta=angle
    R=cos(theta)*np.eye(3)+sin(theta)*np.cross(np.eye(3),axis)+(1-cos(theta))*np.outer(axis,axis)
    return grtb.rot(axis,angle)
# def axang2bg(axis,angle):

#     b=asin(-axis[1]*sin(angle)+(1-cos(angle))*axis[0]*axis[2])
#     g=0;
#     if b==np.pi/2 or b==-np.pi/2:
#         g=0;
#     else:
#         g=atan2(-1*(axis[2]*sin(angle)+(1-cos(angle))*axis[0]*axis[1]), 1-(1-cos(angle))*(axis[2]*axis[2]+axis[1]*axis[1]))
#     return [b,g]
# ----- Testing -----

# H=np.array([[0,0,0,1,0,1],[0,1,1,0,1,0],[1,0,0,0,0,0]])
# H=np.transpose(H)
# P=np.array([[0,.025,0,.123,.2965,.1,.1175],[0,0,0,0,0,0,0],[.279,.171,.454,.035,0,0,0]])*1000 #approximated without 1mm offsets
# P=np.transpose(P)
# # print(np.shape(P))
# robot=Robot.spherical_two_parallel(H,P)

# r=np.array([500,50,500,90,0,0])
# r0=np.array([0,1.6,-2.08,-1.9,2.2,1.0])
# print(runIK(r,r0, ikrobot))

# print(tool2R(np.array([1.0,0,0]),np.array([0,0,1.0]),np.array([[1.0,0,0],[0,1.0,0],[0,0,1.0]])))
# print(tool2R(np.array([0,0,1.0]),np.array([1.0,0,0]),np.array([[0,0,1.0],[0,1.0,0],[-1.0,0,0]])))
