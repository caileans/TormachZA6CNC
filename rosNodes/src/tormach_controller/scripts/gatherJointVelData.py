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
import copy

# NOTE THIS NODE IS IN RADIANS!!!!!!!!!!!!!
#publishing a new position will overwrite the current move
#Note: this doesnt work for cartesian space
if __name__=='__main__':
    
    #start the test node
    rospy.init_node("controller")
    publisher=pub.startPublisher()
    hz=5
    jup=np.array([0,0,-pi/2,0,0,0]);
    speeds=[.1,.3,.4,.5,.6]
    overshoot=1.2
    jprev = np.zeros(6)
    jcur =np.zeros(6)
    jpub=np.zeros(6)
                # hz=50
    pub.straightUp(publisher)
    sleep(5)
    input("thing")
    rate=rospy.Rate(hz)
    for i in range(6):
        for v in speeds:
            offset=v/hz
            jprev=copy.deepcopy(jup)
            jpub=jprev
            flag=0;
            while not rospy.is_shutdown():
                jcur=copy.deepcopy(jprev)
                if flag==0:
                    jcur[i]+=offset
                    # print(jcur)
                    # print(pi/2+jup[i])
                    if jcur[i]>=pi/10+jup[i]:
                        flag=1
                        print(flag)
                elif flag==1:
                    jcur[i]-=offset
                    if jcur[i]<=-pi/10+jup[i]:
                        flag=2
                        print(flag)
                elif flag==2:
                    jcur[i]+=offset
                    if jcur[i]>=jup[i]:
                        pub.pubMove(publisher,jup,1,hz)
                        print(flag)
                        flag=3
                        break
                if flag!=3:
                    jpub=pub.applyOvershoot(jprev,jcur,overshoot)
                    pub.pubMove(publisher,jpub,overshoot,hz)
                    jprev=jcur;
                rate.sleep()
            sleep(1)
        