import os, sys
sys.path.append(os.path.abspath(__file__.split("script")[0]+"/scripts/lib"))
sys.path.append(os.path.abspath(__file__.split("script")[0]+"/scripts/lib/preProcessing"))

from time import sleep
import numpy as np
from math import pi
from general_robotics_toolbox import fwdkin, R2rpy
import keyboard
import rospy

from InverseKinematics import runIK, tormachZA6fk, tormachZA6
import publisher31 as pub

robot_fwd = tormachZA6fk()
robot_IK = tormachZA6()

def keyboardMove(publisher, q, hz):
    # Function that jogs the robot in x y z and sets the zero position
    # q is the start configuration
    # EE_pos is the current end effector Cartesian position
    # hz is the frequency (50 Hz)

    pose = fwdkin(robot_fwd,q)  #Get joint angles from  position / Cartesian position of robot flange
    EE_rot = pose.R
    EE_pos = pose.p

    #Change this to euler angles
    rot_euler = R2rpy(EE_rot)
    #Set Increment
    max_inc = .05

    inc = float(input("Set motion increment (mm): "))

    while inc > max_inc:
        inc = float(input("Increment must be less than 0.5! Give new incrmement: "))
    while type(inc) != float or type(inc) != int:
        inc = float(input("Increment must be a number! Give new increment: "))

    print("increment is ", inc)

    print("Use x,y,z keys to change position. Use a,s,d for negative resepctive increment. Hit esc to stop movement and return final position")

    rot_euler = np.array(rot_euler)

    print("Initial euler angles are: ", rot_euler)
    print("Initial EE_pos is: ", EE_pos)

    rate = rospy.rate(hz)

    while True:

        if keyboard.is_pressed("x"):
            change_dir = 0
            increment = inc
        elif keyboard.is_pressed("y"):
            change_dir = 1
            increment = inc
        elif keyboard.is_pressed("z"):
            change_dir = 2
            increment = inc
        elif keyboard.is_pressed("a"):
            change_dir = 0
            increment = -inc
        elif keyboard.is_pressed("s"):
            change_dir = 1
            increment = -inc
        elif keyboard.is_pressed("d"):
            change_dir = 2
            increment = -inc
        elif keyboard.is_pressed("esc"):
            break
        else:
            continue

        #Updates and moves the robot's Cartesian position
        EE_pos[change_dir] += increment  #Update new position's axis
        print("Current Euler Angles: ", rot_euler)
        print("Current Position: ", EE_pos)
        r = np.append(EE_pos, rot_euler)
        print("r array is : ", r)
        new_EE_joints = runIK(r, q, robot_IK)  #Return new joints in joint space
        q = new_EE_joints
        pub.pubMove(publisher,q,1,hz)  #Publish new position to robot      
        rate.sleep()
        print(EE_pos)

    print("Final position is : ", EE_pos)

    return EE_pos, q


  