import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__).split("controller.py")[0]+"/lib")))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__).split("controller.py")[0]+"/lib/__init__.py")))
# print(os.path.dirname(os.path.dirname('/scripts/lib')))
# print(os.path.abspath(__file__.split("controller.py")[0]+"/lib"))
sys.path.append(os.path.abspath(__file__.split("gatherJointVelData.py")[0]))
sys.path.append(os.path.abspath(__file__.split("gatherJointVelData.py")[0]+"/lib"))
sys.path.append(os.path.abspath(__file__.split("gatherJointVelData.py")[0]+"/lib/preProcessing"))
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
from math import pi


# NOTE THIS NODE IS IN RADIANS!!!!!!!!!!!!!
#publishing a new position will overwrite the current move
#Note: this doesnt work for cartesian space
if __name__=='__main__':
    
    #start the test node
    rospy.init_node("controller")
    publisher=pub.startPublisher()
    hz=50
    jup=np.array([0,0,-pi/2,0,0,0]);
    speeds=[.3,.6,.9,1.2,1.5]
                # hz=50

    rate=rospy.Rate(hz)
    for i in range(6):
        for v in speeds:
            offset=v/hz
            jprev=jup
            jpub=jprev
            flag=0;
            while not rospy.is_shutdown():
                if flag==0:
                    jcur=jprev
                    jcur[i]+=offset
                    if jcur[i]>=pi/2+jup[i]:
                        flag==1
                elif flag==1:
                    jcur=jprev
                    jcur[i]-=offset
                    if jcur[i]>=-pi/2+jup[i]:
                        flag==2
                elif flag==2:
                    jcur=jprev
                    jcur[i]+=offset
                    if jcur[i]>=jup[i]:
                        pub.pubMove(publisher,jup,overshoot,hz)
                        break
                jpub=pub.applyOvershoot(jprev,jcur,overshoot)
                pub.pubMove(publisher,jpub,overshoot,hz)
                jprev=jcur;
                rate.sleep()
            sleep(1)
        