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
import touchoff2 as jog
from tormach_controller.msg import  forceTorque
import general_robotics_toolbox as grtb

def pose_callback(msg):
    return np.array([msg.forcex,    msg.forcey,    msg.forcez,    msg.momenti,    msg.momentj,    msg.momentk])
# NOTE THIS NODE IS IN RADIANS!!!!!!!!!!!!!
#publishing a new position will overwrite the current move
#Note: this doesnt work for cartesian space
if __name__=='__main__':
    
    #start the test node
    rospy.init_node("controller")
    os.system("rosrun tormach_controller forceCalculation.py &")
    # x=DataTypes.TrajPoint()
    filepath ='/home/pathpilot/Downloads/TormachZA6CNC/Gcode/'
    publisher=pub.startPublisher()
    overshoot=2.0
    robot=ik.tormachZA6()

    while True:

        userfile=input("file name:").strip()
        pub.home(publisher)
        jprev = np.zeros(6)
        jprev[2]=np.pi/18;
        jprev[4]=-np.pi/18
        file=filepath
        offset=[0,0,0]
        # print(userfile)
        hz=float(input("hz: ").strip())
        overshoot=float(input("overshoot: ").strip())
        if userfile=='0':
            exit()
        elif userfile =='1':
            file=file+"circleTest.nc"
        elif userfile =='2':
            file=file+"TormachR.nc"
            offset=[432.1,89,427]
        elif userfile=='jog':
            eePositon, jprev=jog.keyboardMove(publisher,jprev,hz)
        elif userfile=='forcePoint':
            sub=rospy.Subscriber("eeforce", forceTorque, callback=pose_callback)
            direct=np.array([float(input("dir x").strip()),float(input("dir y").strip()),float(input("dir z").strip())])
            pose=np.array(grtb.fwdkin(ik.tormachZA6fk(),jprev).p)
            direct/=np.linalg.norm(direct)
            c=0
            flag=False
            while c<=10**10:
                msg=rospy.wait_for_message('eeforce',forceTorque,.1)
                force=np.array([msg.forcex,msg.forcey,msg.forcez])
                c+=1
                if np.dot(force,direct)<-5000:
                    pose+=.05*direct
                    flag=True
                elif not flag:
                    pose-=.5*direct
                else:
                    pose-=.05*direct
                jprev=ik.runIK(np.array([pose[0],pose[1],pose[2],0,0,0]),jprev,robot)
                pub.pubMove(publisher,jprev,1,hz)
                sleep(1.0/hz)

        else:
            file=file+userfile
            offset=[float(input("offset x").strip()),float(input("offset y").strip()),float(input("offset z").strip())]
        jcur =np.zeros(6)
        jpub=np.zeros(6)
        # hz=50
        moveBuffer=Queue(maxsize=0)

        pointList=gct.genTrajectory(file, a=30,hz=hz,feedRate=30,rapidFeed=30,toolFrameOffset=offset,pureRotVel=np.pi/20, tOffset=[0,50])
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

            # rate=rospy.Rate(hz)
            rate.sleep()
        
        # break