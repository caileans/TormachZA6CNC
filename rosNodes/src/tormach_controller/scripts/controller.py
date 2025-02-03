import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import rospy 
from time import sleep
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np
import lib.InverseKinematics as ik
import lib.publisher31 as pub
import DataTypes
import GCodeToTrajectory as gct
from queue import Queue



# NOTE THIS NODE IS IN RADIANS!!!!!!!!!!!!!
#publishing a new position will overwrite the current move
#Note: this doesnt work for cartesian space
if __name__=='__main__':
    
    #start the test node
    rospy.init_node("controller")
    # x=DataTypes.TrajPoint()
    file ='./Gcode/circleTest.nc'
    publisher=pub.startPublisher()
    overshoot=2.0
    robot=ik.tormachZA6()

    jprev = np.zeros(6)
    jcur =np.zeros(6)
    jpub=np.zeros(6)
    hz=50
    moveBuffer=Queue(maxsize=0)

    pointList=gct.genTrajectory(file)
    for point in pointList:
    	moveBuffer.put(point)

    rate=rospy.Rate(hz)

    while not rospy.is_shutdown():

    	if moveBuffer.empty():
    		pub.pubMove(publisher,jprev, 1,hz)
    	else:
    		point=moveBuffer.get()
    		jcur=ik.runIK(np.array([point.pose[0:3],point.rot[0:3]]),jprev,robot)
    		jpub=applyOvershoot(jprev,jcur,overshoot)
    		pub.pubMove(publisher,jpub,overshoot,hz)
    		jprev=jcur;

    	rate=rospy.Rate(hz)
    	rate.sleep()