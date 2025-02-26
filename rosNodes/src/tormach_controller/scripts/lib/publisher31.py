import rospy 
from time import sleep
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np
from math import pi

def pubMove(publisher, j, alpha, hz):
	"""publishes a move to the position_trajectory_controller/command topic

	Inputs:
		publisher - a rospy object describing the position_trajectory_controller/command publisher
		j - the desired joint pose (6 element np array)
		alpha - the overshoot multiplier (alpha=1 is just j, alpha=2 is double the distance)
		hz - the publishing frequency being used (1/time for move)
	Output:
		NONE"""
	# print(j)
	pnt=JointTrajectoryPoint()
	pnt.positions=[j[0],j[1],j[2],j[3],j[4],j[5],0.1,0.1]
	pnt.effort=[]
	pnt.velocities=[]
	pnt.accelerations=[]
	pnt.time_from_start.nsecs=int(alpha*(10**9)/hz)
	pubmsg=JointTrajectory()
	pubmsg.joint_names=['joint_1','joint_2','joint_3','joint_4','joint_5','joint_6','tcp_lin','tcp_rot']
	pubmsg.points=[pnt]
	pubmsg.header.stamp=rospy.Time.now()
	publisher.publish(pubmsg)


def applyOvershoot(j0, j, alpha):
	"""computes joint space overshoot

	Inputs:
		j0 - the current position of the arm (6 element np array)
		j - the desired resulting position of the arm (6 element np array)
		alpha - the overshoot multiplier (alpha=1 is just j, alpha=2 is double the distance)
	Output:
		the overshoot adjusted joint space pose"""
	j+=(alpha-1.0)*(j-j0)
	# for i in range(np.shape(j)[0]):
	# 	j[i]+=(alpha-1)*(j[i]-j0[i])
	return np.array(j)

def startPublisher():
	"""starts the /position_trajectory_controller/command publisher

	Inputs:
	Output:
		a rospy object describing the position_trajectory_controller/command publisher"""

	publisher=rospy.Publisher('/position_trajectory_controller/command', JointTrajectory, queue_size=1)
	sleep(60)
	print("prob conected")
	return publisher


def home(publisher):

	pnt=JointTrajectoryPoint()
	pnt.positions=[0,0,np.pi/18,0,-np.pi/18,0,0.1,0.1]
	pnt.time_from_start.secs=5
	pubmsg=JointTrajectory()
	pubmsg.joint_names=['joint_1','joint_2','joint_3','joint_4','joint_5','joint_6','tcp_lin','tcp_rot']
	pubmsg.points=[pnt]
	pubmsg.header.stamp=rospy.Time.now()
	publisher.publish(pubmsg)
	return