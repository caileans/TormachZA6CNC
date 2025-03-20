import os, sys
sys.path.append(os.path.abspath(__file__.split("script")[0]+"/scripts/lib"))
sys.path.append(os.path.abspath(__file__.split("script")[0]+"/scripts/lib/preProcessing"))

from time import sleep
import numpy as np
from math import pi
from general_robotics_toolbox import fwdkin, R2rpy
import keyboard

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
    inc = float(input("Set motion increment (mm): "))      #Max increment?
    print("increment is ", inc)


    input("Use x,y,z keys to change position. Use with shift for negative increment. Hit esc to stop movement and return final position")

    print(rot_euler)

    rot_euler = np.array(rot_euler).reshape(1,3)
    EE_pos = EE_pos.reshape(1,3)

    print(rot_euler)
    print(EE_pos)



    moveRobotx(EE_pos, rot_euler, q, hz, inc, publisher)

    #keyboard.add_hotkey('x', moveRobotx(EE_pos, rot_euler, q, hz, inc, publisher))
    #keyboard.add_hotkey('y', moveRoboty(EE_pos, rot_euler, q, hz, inc, publisher))
    #keyboard.add_hotkey('z', moveRobotz(EE_pos, rot_euler, q, hz, inc, publisher))
    #keyboard.add_hotkey('shift + x', moveRobotnegx(EE_pos, rot_euler, q, hz, inc, publisher))
    #keyboard.add_hotkey('shift + y', moveRobotnegy(EE_pos, rot_euler, q, hz, inc, publisher))
    #keyboard.add_hotkey('shift + z', moveRobotnegz(EE_pos, rot_euler, q, hz, inc, publisher))

    keyboard.wait("esc")
    print("The current EE position is ", EE_pos)
    print("The zerod")
    
    return EE_pos, q

def moveRobotx(position, q, rot_euler, hz, inc, publisher):
    #Updates and moves the robot's Cartesian position in the x direction
    position[0] += inc  #Update new position's axis
    print("rot_euler", rot_euler)
    print("position", position)
    r = np.append(position, rot_euler)
    print(r)
    new_EE_joints = runIK(r, q, robot_IK)  #Return new joints in joint space
    q = new_EE_joints
    pub.Move(publisher,q,1,hz)  #Publish new position to robot      
    sleep(1/hz)
    print(position)
    return position, q

def moveRoboty(position, q, rot_euler, hz, inc, publisher):
    #Updates and moves the robot's Cartesian position in the y direction
    position[1] += inc
    r = np.append(position, rot_euler)
    new_EE_joints = runIK(r, q, robot_IK)
    q = new_EE_joints
    pub.Move(publisher,q,1,hz)     
    sleep(1/hz)
    print(position)
    return position, q

def moveRobotz(position, q, rot_euler, hz, inc, publisher):
    #Updates and moves the robot'ss Cartesian position in the z direction
    position[2] += inc
    r = np.append(position, rot_euler)
    new_EE_joints = runIK(r, q, robot_IK) 
    q = new_EE_joints
    pub.Move(publisher,q,1,hz)   
    sleep(1/hz)
    print(position)
    return position, q

def moveRobotnegx(position, q, rot_euler, hz, inc, publisher):
    #Updates and moves the robot's Cartesian position in the x direction
    position[0] += -inc  #Update new position's axis
    r = np.append(position, rot_euler)
    new_EE_joints = runIK(r, q, robot_IK)  #Return new joints in joint space
    q = new_EE_joints
    pub.Move(publisher,q,1,hz)  #Publish new position to robot      
    sleep(1/hz)
    print(position)
    return position, q

def moveRobotnegy(position, q, rot_euler, hz, inc, publisher):
    #Updates and moves the robot's Cartesian position in the y direction
    position[1] += -inc
    r = np.append(position, rot_euler)
    new_EE_joints = runIK(r, q, robot_IK)
    q = new_EE_joints
    pub.Move(publisher,q,1,hz)     
    sleep(1/hz)
    print(position)
    return position, q

def moveRobotnegz(position, q, rot_euler, hz, inc, publisher):
    #Updates and moves the robot'ss Cartesian position in the z direction
    position[2] += -inc
    r = np.append(position, rot_euler)
    new_EE_joints = runIK(r, q, robot_IK) 
    q = new_EE_joints
    pub.Move(publisher,q,1,hz)   
    sleep(1/hz)
    print(position)
    return position, q
    






  