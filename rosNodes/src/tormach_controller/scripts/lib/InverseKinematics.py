import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ik_geo import Robot # pip install ik-geo
import numpy as np
import general_robotics_toolbox as grtb
from math import pi



def getIK(position, Rotation,robot):
    """ calculates the set of IK solutions using the ik_geo toolbox

    Inputs:
        position - an array of length 3 that contains the desired x, y, z corrdinates of the end effector
        Rotation - the rotation matrix that describes the orientation of the end effector
        robot - an ik_geo Robot type describing the robot arm
    Output:
        the set of ik solutions calculated by ik_geo""" 

    return robot.get_ik_sorted(Rotation,[position[0],position[1],position[2]])

def abcToR(abc):
    """uses the general robotics toolbox from rpi to calculate the rotation matrix from the static euler angles

    Inputs:
        abc - an array of length 3 that contains the alpha, beta, and gamma euler angles in radians
    Output:
        a 3x3 rotation matrix describing the orientation"""
    return grtb.rpy2R([abc[-1],abc[-2],abc[-3]])

def chooseIK(r0, sols, w):
    """chooses the best ik solution by minimizing the error in the solution and change from joint position r0

    Inputs:
        r0 - an np array of length 6 that describes the previous joint state
        sols - the solution set returned by ik_geo
        w - an array of legnth 7 that contains the weighing factors for each state
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
            newvalue+=w[j]*(newsol[j]-r0[j])**2
        # print(newvalue)
        # newvalue=(newsol[0]-r0[0])**2+(newsol[5]-r0[5])**2
        if newvalue<minval:
            minval=newvalue
            minindex=i;
        i+=1
    return np.array(sols[minindex][0])


def runIK (r, r0, ikrobot, w=[1,1,1,1,1,1,0]):
    """ calculates and chooses the best inverse kinematics solution 

    inputs: 
        r - a numpy array of length 6 with the entries [x pose, y pose, z pose, a, b, c] where a b and c are the static frame roll, pitch, and yaw orientation in degrees
        r0 - a np array of length 6 containing the previous joint angles in radians
        ikrobot - an ik_geo Robot type describing the robot arm
        w - the weighting factor of the deviations 1x7 array of j1-j6 then ik solution error
    output:
        a np array of length 6 containing the selected joint angles"""

    w=np.array(w)
    abc=[r[-3]*pi/180,r[-2]*pi/180,r[-1]*pi/180];
    # print(r0)
    R=abcToR(abc)
    # print(R)
    sols=getIK(r,np.transpose(R), ikrobot)
    return chooseIK(r0,sols,w)


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
    P=np.array([[0,.025,0,.123,.2965,.1,.1175-.1],[0,0,0,0,0,0,0],[.279,.171,.454,.035,0,0,0]])*1000 #approximated without 1mm offsets
    # P=np.transpose(P)
    # print(np.shape(P))
    robot=grtb.Robot(H,P,[0,0,0,0,0,0])
    return robot



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