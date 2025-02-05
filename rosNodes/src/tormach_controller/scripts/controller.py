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
    jprev[2]=np.pi/18;
    jprev[4]=-np.pi/18
    jcur =np.zeros(6)
    jpub=np.zeros(6)
    hz=10
    moveBuffer=Queue(maxsize=0)

    pointList=gct.genTrajectory(file, a=30,hz=hz,feedRate=30,rapidFeed=120)
    for point in pointList:
        moveBuffer.put(point)

    rate=rospy.Rate(hz)

    while not rospy.is_shutdown():

        if moveBuffer.empty():
            pub.pubMove(publisher,jprev, 1,hz)
            sleep(3)
        else:
            # print(np.append(np.array(point.pos[0:3]),point.rot[0:3], axis=0))
            point=moveBuffer.get()
            # print(point)
            jcur=ik.runIK(np.append(np.array(point.pos[0:3]),point.rot[0:3], axis=0),jprev,robot)
            # print(jcur)
            jpub=pub.applyOvershoot(jprev,jcur,overshoot)
            # jpub=jcur
            print(jpub)
            pub.pubMove(publisher,jpub,overshoot,hz)
            jprev=jcur;
        # pub.pubMove(publisher,[0,0,np.pi/18,0,-np.pi/18,0],1,)
        pnt=JointTrajectoryPoint()
        pnt.positions=[0,0,np.pi/18,0,-np.pi/18,0,0.1,0.1]
        pnt.time_from_start.secs=3
        pubmsg=JointTrajectory()
        pubmsg.joint_names=['joint_1','joint_2','joint_3','joint_4','joint_5','joint_6','tcp_lin','tcp_rot']
        pubmsg.points=[pnt]
        pubmsg.header.stamp=rospy.Time.now()
        publisher.publish(pubmsg)
        rate=rospy.Rate(hz)
        rate.sleep()