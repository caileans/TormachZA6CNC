import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__).split("controller.py")[0]+"/lib")))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__).split("controller.py")[0]+"/lib/__init__.py")))
# print(os.path.dirname(os.path.dirname('/scripts/lib')))
# print(os.path.abspath(__file__.split("controller.py")[0]+"/lib"))
sys.path.append(os.path.abspath(__file__.split("controller.py")[0]))
sys.path.append(os.path.abspath(__file__.split("controller.py")[0]+"/lib"))
sys.path.append(os.path.abspath(__file__.split("controller.py")[0]+"/lib/preProcessing"))
# sys.path.append(os.path.abspath(__file__.split("controller.py")[0]+"../../../../preProcessing"))
# print(sys.path)
import rospy 
from time import sleep
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np
import lib.InverseKinematics as ik
import lib.publisher31 as pub
import preProcessing.DataTypes
import preProcessing.GCodeToTrajectory as gct
from queue import Queue



# NOTE THIS NODE IS IN RADIANS!!!!!!!!!!!!!
#publishing a new position will overwrite the current move
#Note: this doesnt work for cartesian space
if __name__=='__main__':
    
    #start the test node
    rospy.init_node("controller")
    # x=DataTypes.TrajPoint()
    file ='/home/pathpilot/Downloads/TormachZA6CNC/Gcode/circleTest.nc'
    publisher=pub.startPublisher()
    overshoot=1.0
    robot=ik.tormachZA6()

    jprev = np.zeros(6)
    jcur =np.zeros(6)
    jpub=np.zeros(6)
    hz=10
    moveBuffer=Queue(maxsize=0)

    pointList=gct.genTrajectory(file, a=180,hz=hz,feedRate=200,rapidFeed=400)
    for point in pointList:
        moveBuffer.put(point)

    rate=rospy.Rate(hz)

    while not rospy.is_shutdown():

        if moveBuffer.empty():
            pub.pubMove(publisher,jprev, 1,hz)
        else:
            # print(np.append(np.array(point.pos[0:3]),point.rot[0:3], axis=0))
            point=moveBuffer.get()
            jcur=ik.runIK(np.append(np.array(point.pos[0:3]),point.rot[0:3], axis=0),jprev,robot)
            # print(jcur)
            jpub=pub.applyOvershoot(jprev,jcur,overshoot)
            # print(jpub)
            pub.pubMove(publisher,jpub,overshoot,hz)
            jprev=jcur;

        rate=rospy.Rate(hz)
        rate.sleep()