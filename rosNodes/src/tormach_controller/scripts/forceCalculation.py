
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__).split("controller.py")[0]+"/lib")))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__).split("controller.py")[0]+"/lib/__init__.py")))
# print(os.path.dirname(os.path.dirname('/scripts/lib')))
# print(os.path.abspath(__file__.split("controller.py")[0]+"/lib"))
sys.path.append(os.path.abspath(__file__.split("force")[0]))
sys.path.append(os.path.abspath(__file__.split("force")[0]+"/lib"))
sys.path.append(os.path.abspath(__file__.split("force")[0]+"/lib/preProcessing"))

import rospy 
from tormach_controller.msg import pose, forceTorque, MovePoseAction, MovePoseGoal,MovePoseResult,MovePoseFeedback
from sensor_msgs.msg import JointState
import numpy as np
import lib.InverseKinematics as ik
import lib.publisher31 as pub
import preProcessing.DataTypes
import gravityIsolation as grav
import general_robotics_toolbox as grtb
from math import sin, cos, pi,exp
import csv
import frictionIsolation as fric


def jointStateCallback(msg,gravity,friction):
    # print("h")
    # rospy.loginfo(msg.effort);
    #print(np.array(msg.position)[0:6])
    tau=friction(msg.velocity[0:6],gravity(msg.position[0:6],msg.effort[0:6]))
    jac=grtb.robotjacobian(ik.tormachZA6fk(),np.array(msg.position)[0:6])

    # print(jac)

    #force=np.array([0,0,0,0,0,0])
    force=np.matmul(jac,tau)
    pubmsg=forceTorque()
    pubmsg.forcex=force[3];
    pubmsg.forcey=force[4];
    pubmsg.forcez=force[5];
    pubmsg.momenti=force[1];
    pubmsg.momentj=force[2];
    pubmsg.momentk=force[3];
    forcePub.publish(pubmsg)
    # rospy.loginfo(force)

if __name__=='__main__':
    # run calibration code
    adjuster=grav.calibrate("gravityIsolationData.csv")
    a,b=fric.getFrictionModel()
    friction=lambda v,tau:fric.frictionModel(v,tau,a,b=b)
    #start the buffer_node node
    rospy.init_node("forceCalculation")
    #subscribe to the "/tormach/movePose" topic which has a pose msg type
    # sub=rospy.Subscriber("/tormach/movePose", pose, callback=pose_callback)
    #with open('data.csv','w',newline='') as csvfile:
    #	writer=csv.writer(csvfile)
    currentPoseSub=rospy.Subscriber("/joint_states", JointState,queue_size=1, callback=lambda msg:jointStateCallback(msg,adjuster,friction))
    forcePub=rospy.Publisher('eeforce', forceTorque, queue_size=1,latch=True)
    #keep node running until shutdown request
    while not  rospy.is_shutdown():
    	1==1
        # if not moveBuffer.empty():
            # result=movepose_client();