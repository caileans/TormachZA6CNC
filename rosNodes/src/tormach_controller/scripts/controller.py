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
    filepath ='/home/pathpilot/Downloads/TormachZA6CNC/Gcode/'
    publisher=pub.startPublisher()
    overshoot=2.0
    robot=ik.tormachZA6()

    while True:
        userfile=input("file name:").strip()
        file=filepath
        offset=[0,0,0]
        print(userfile)
        if userfile==0:
            break
        elif userfile =='1':
            file=file+"circleTest.nc"
        elif userfile =='2':
            file=file+"TormachR.nc"
            offset=[426.7,110,528.6]
        else:
            file=file+userfile
            offset=[float(input("offset x").strip()),float(input("offset y").strip()),float(input("offset z").strip())]
        jprev = np.zeros(6)
        jprev[2]=np.pi/18;
        jprev[4]=-np.pi/18
        jcur =np.zeros(6)
        jpub=np.zeros(6)
        hz=50
        moveBuffer=Queue(maxsize=0)

        pointList=gct.genTrajectory(file, a=30,hz=hz,feedRate=30,rapidFeed=30,toolFrameOffset=offset)
        for point in pointList:
            moveBuffer.put(point)

        rate=rospy.Rate(hz)

        while not rospy.is_shutdown():

            if moveBuffer.empty():
                pub.pubMove(publisher,jprev, 1,hz)
                sleep(3)
                
                break
                
            else:
                # print(np.append(np.array(point.pos[0:3]),point.rot[0:3], axis=0))
                point=moveBuffer.get()
                # print(point)
                jcur=ik.runIK(np.append(np.array(point.pos[0:3]),point.rot[0:3], axis=0),jprev,robot)
                # print(jcur)
                jpub=pub.applyOvershoot(jprev,jcur,overshoot)
                # jpub=jcur
                # print(jpub)
                pub.pubMove(publisher,jpub,overshoot,hz)
                jprev=jcur;
            # pub.pubMove(publisher,[0,0,np.pi/18,0,-np.pi/18,0],1,)

            rate=rospy.Rate(hz)
            rate.sleep()
        pub.home(publisher)
        # break