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
from sensor_msgs.msg import JointState
import csv


def pose_callback(msg):
    return np.array([msg.forcex,    msg.forcey,    msg.forcez,    msg.momenti,    msg.momentj,    msg.momentk])

def getParams(file,default):
    params=default
    # print(file)
    # print(params)
    # print(file.split('.')[0]+'.csv')
    try:
        with open(file.split('.')[0]+'.csv', 'r') as csvfile:
            # print("opened file")
            reader = csv.reader(csvfile)
            # print("read file")
            for row in reader:
                try:
                    # print(row)
                    # temp1=row[1].split(',')
                    temp2=0
                    # print(row)
                    # print(temp1)
                    if len(row)>2:
                        temp=[];
                        for i in range(len(row)-1):
                            temp.append(float(row[i+1].split(']')[0].split('[')[-1]))
                        temp2=temp
                    elif len(row)==2:
                        temp2=float(row[1])
                    if row[0]=='rotate':
                        temp3=[]
                        for i in range(3):
                            temp4=[]
                            for j in range(3):
                                temp4.append(temp2[3*i+j])
                            temp3.append(temp4)
                        temp2=temp3

                    print(temp2)
                    params[row[0]]=temp2
                except:
                    print('unknown input')
    except:
        print("no file")
    finally:
        return params["hz"],params["offset"],params["velocity"], params["jprev"],params["overshoot"],params["rotate"],params["a"],params["tOffset"]

# NOTE THIS NODE IS IN RADIANS!!!!!!!!!!!!!
#publishing a new position will overwrite the current move
#Note: this doesnt work for cartesian space
if __name__=='__main__':
    
    #start the test node
    rospy.init_node("controller")
    # os.system("xterm -e rosrun tormach_controller forceCalculation.py")
    # feedback=False
    # myargv = rospy.myargv(argv=sys.argv)
    # if len(myargv) == 2:
    #     feedback=myargv[1]
    # print(myargv)
    # x=DataTypes.TrajPoint()
    filepath ='/home/pathpilot/Downloads/TormachZA6CNC/Gcode/'
    publisher=pub.startPublisher()
    overshoot=2.0
    robot=ik.tormachZA6()

    while True:
        userfile=input("file name:").strip()
        pub.home(publisher)
        sleep(5)
        default=dict(hz=50,offset=[550,0,550], velocity=[30,30,20],jprev=np.array([0,0,10,0,-10,0]),overshoot=1.2,rotate=np.eye(3),a=30,tOffset=[0,50])
        jprev = np.zeros(6)
        jprev[2]=np.pi/18;
        jprev[4]=-np.pi/18
        
        file=""
        # print(userfile)
        # hz=float(input("hz: ").strip())
        # overshoot=float(input("overshoot: ").strip())
        if userfile=='0':
            exit()
        elif userfile =='1':
            file=filepath+"circleTest.nc"
            default["offset"]=[0,0,0]
        elif userfile =='2':
            file=filepath+"TormachR.nc"
            default["offset"]=[432.1,89,427]
        elif userfile=='jog':
            eePositon, jprev=jog.keyboardMove(publisher,jprev,hz)
        elif userfile=='calibrateGravity':
            import csv
            q=np.zeros((1,6))
            tau=np.zeros((1,6))
            time=20.5
            file=os.path.abspath(__file__.split("controller.py")[0]+"/lib/gravityIsolationData.csv")
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    temp=np.array([[float(row[0].split('(')[1]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5].split(')')[0])]])
                    # print(temp)
                    q=np.append(q,temp, axis=0)
                    temp=[[float(row[6].split('(')[1]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11].split(')')[0])]]
                    tau=np.append(tau,temp, axis=0)
            print("moving")
            data=[]
            for point in q:
                pub.pubBigMove(publisher,point,time);
                sleep(time+.25);
                msg=rospy.wait_for_message("/joint_states", JointState, timeout=1)
                pose=msg.position[0:6]
                effort=msg.effort[0:6]
                data.append(str(pose)+','+str(effort))
                sleep(.01)
            print("printing")
            f=open(file,'w')
            c=0
            for d in data:
                f.write(d+'\n')
                print(str(c)+':'+d)
                c+=1


        elif userfile=='forcePoint':
            hz=50
            jprev=np.array([0,41,37,0,-77.887,0])*np.pi/180
            sub=rospy.Subscriber("eeforce", forceTorque, callback=pose_callback)
            direct=np.array([float(input("dir x").strip()),float(input("dir y").strip()),float(input("dir z").strip())])
            pose=np.array(grtb.fwdkin(ik.tormachZA6fk(),jprev).p)
            direct/=np.linalg.norm(direct)
            c=0
            flag=False
            pub.pubBigMove(publisher,jprev,5)
            sleep(5.25)
            bound=-18000
            kp=.1**6.5
            while c<=10**10:
                msg=rospy.wait_for_message('eeforce',forceTorque,.1)
                force=np.array([msg.forcex,msg.forcey,msg.forcez])
                c+=1
                force=np.dot(force,direct)
                if force<bound:
                    pose+=.05*direct*max(abs(abs(force)-abs(bound))*kp,1)
                    flag=True
                elif not flag:
                    pose-=.05*direct
                else:
                    pose-=.05*direct*max(abs(abs(force)-abs(bound))*kp,1)
                jprev=ik.runIK(np.array([pose[0],pose[1],pose[2],0,0,0]),jprev,robot)
                pub.pubMove(publisher,jprev,1,hz)
                sleep(1.0/hz)
        elif userfile=='getForce':
            sub=rospy.Subscriber("eeforce", forceTorque, callback=pose_callback)
            n=int(input("Number of samples: "))
            while True:
                input("press enter when  ready")
                force=np.zeros(3)
                for i in range(n):  
                    msg=rospy.wait_for_message('eeforce',forceTorque,.1)
                    force+=np.array([msg.forcex,msg.forcey,msg.forcez])
                print((force/n))
        elif userfile=='complianceDemo':
            sleep(1)
            hz=20
            rate=rospy.Rate(hz)
            threshold=[.06,.06,.06];
            sub=rospy.Subscriber("eeforce", forceTorque, callback=pose_callback)
            n=3
            force=np.zeros((n,3));
            c=0
            avg=0
            movemax=7
            movemin=0
            k=.1**(3.5-4-.5-.75-.15)
            pose=np.array(grtb.fwdkin(ik.tormachZA6fk(),jprev).p)
            while True:
                msg=rospy.wait_for_message('eeforce',forceTorque,.2)
                force[c,:]=np.array([msg.forcex,msg.forcey,msg.forcez])
                for i in range(3):
                    avg=np.mean(force[:,i])
                    if abs(avg)>threshold[i]:
                        # print(0)
                        pose[i]-=(avg/abs(avg))*max(movemin,min(movemax,k*(abs(avg)-abs(threshold[i]))))

                jprev=ik.runIK(np.array([pose[0],pose[1],pose[2],0,0,0]),jprev,robot)
                pub.pubMove(publisher,jprev,1.05,hz)
                c=(c+1)%n
                rate.sleep()

        else:
            file=filepath+userfile

            # offset=[float(input("offset x").strip()),float(input("offset y").strip()),float(input("offset z").strip())]
            # velocity=[float(input("linear vel").strip()),float(input("rapid vel").strip()),float(input("rot vel").strip())]
            # initPose=np.array([float(input("Initial Pose x").strip()),float(input("Initial Pose y").strip()),float(input("Initial Pose z").strip())])
            # initPose/=np.linalg.norm(initPose)
            # for i in range(6):
            #     jprev[i]=float(input("Joint "+str(i+1)).strip())
            # origin=[562.0,0.0,866.0]
        

        jcur =np.zeros(6)
        jpub=np.zeros(6)
        # hz=50
        moveBuffer=Queue(maxsize=0)
        pointList=0

        if len(file)>0:
            hz,offset, velocity, jprev,overshoot,rotate,a,tOffset=getParams(file,default)
            jprev=np.array(jprev)*np.pi/180
            fwdkin=grtb.fwdkin(ik.tormachZA6fk(),jprev)

            pub.pubBigMove(publisher,jprev,3.5)
            sleep(3.5)
            # print(fwdkin.p)
            print(np.matmul(fwdkin.R,np.array([0,0,1])))
            pointList=gct.genTrajectory(file, a=a,hz=hz,feedRate=velocity[0],rapidFeed=velocity[1],toolFrameOffset=offset,pureRotVel=np.pi/velocity[2], tOffset=tOffset,origin=fwdkin.p,toolIJKInit=np.matmul(fwdkin.R,np.array([0,0,1])),toolFrameRot=rotate)
        
        if not pointList==0:
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
                # jpub[5] -= 10*np.pi/180.0
                pub.pubMove(publisher,jpub,overshoot,hz)
                jprev=jcur;
            # pub.pubMove(publisher,[0,0,np.pi/18,0,-np.pi/18,0],1,)

            # rate=rospy.Rate(hz)
            rate.sleep()
        
        # break