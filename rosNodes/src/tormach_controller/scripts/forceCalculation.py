
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
from math import sin, cos, pi,exp
import csv

def getFrictionModel():
	with open(__file__.split("Tormach")[0]+"TormachZA6CNC/data/jointvel/"+'velFrictionGains.csv', 'r', newline='') as csvfile:
		reader = csv.reader(csvfile)
		a=np.zeros(36)
		for row in reader:
			c=0
			# print(c)
			# print(row)
			for val in row:
				a[c]=float( val)
				c+=1
	with open(__file__.split("Tormach")[0]+"TormachZA6CNC/data/jointvel/"+'velFrictionConst.csv', 'r', newline='') as csvfile:
		reader = csv.reader(csvfile)
		b=np.zeros(6)
		for row in reader:
			c=0
			# print(c)
			# print(row)
			for val in row:
				b[c]=float( val)
				c+=1
	return a,b

def frictionModel(v,tau,a,b=[0,0,0,0,0,0]):
	A=np.zeros((6,6));
	for i in range(6):
		for j in range(6):
			A[i][j]=a[6*i+j]
	v=np.array(v)[0:6]
	# print(v)
	tau=np.array(tau)[0:6]
	# print(tau)
	tau=tau-np.matmul(A,v)
	# print(tau)
	# print(np.shape(v))
	for val in range(6):
		# print(b[val]*np.sign(v[val]))
		k=1
		barrier=.005
		if np.sign(v[val])*v[val]<barrier:
			k=np.sign(v[val])*v[val]/barrier
		tau[val]+=k*b[val]*np.sign(v[val])
	# print(tau)
	return tau

def jointStateCallback(msg,grav,fric):
    # print("h")
    # rospy.loginfo(msg.effort);
    #print(np.array(msg.position)[0:6])
    tau=fric(msg.velocity[0:6],grav(msg.position[0:6],msg.effort[0:6]))
    jac=robotjacobian(ik.tormachZA6FK(),np.array(msg.position)[0:6])

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
    adjuster=grav.calibrate("data.csv")
    a,b=getFrictionModel()
    friction=lambda v,tau:frictionModel(v,tau,a,b=b)
    #start the buffer_node node
    rospy.init_node("forceCalculation")
    #subscribe to the "/tormach/movePose" topic which has a pose msg type
    sub=rospy.Subscriber("/tormach/movePose", pose, callback=pose_callback)
    #with open('data.csv','w',newline='') as csvfile:
    #	writer=csv.writer(csvfile)
    currentPoseSub=rospy.Subscriber("/joint_states", JointState,queue_size=1, callback=lambda msg:jointStateCallback(msg,adjuster,friction))
    forcePub=rospy.Publisher('eeforce', forceTorque, queue_size=1,latch=true)
    #keep node running until shutdown request
    while not  rospy.is_shutdown():
    	1==1
        # if not moveBuffer.empty():
            # result=movepose_client();