import rospy import rospy
from tormach_controller import pose
from sensor_msgs import JointState

def pose_callback(msg):
	rospy.loginfo(msg)
def jointStateCallback(msg):
	rospy.loginfo(msg.effort);
	writer.writerow(msg.effort)

if __name__=='__main__':
	#start the buffer_node node
	rospy.init_node("buffer_node")
	
	#subscribe to the "/tormach/movePose" topic which has a pose msg type
	sub=rospy.Subscriber("/tormach/movePose", pose, callback=pose_callback)
	
	with open('data.csv','w',newline='') as csvfile:
		writer=csv.writer(csvfile)
	currentPoseSub=rospy.Subscriber("/joint_states", JointState, callback=jointStateCallback)
	
	#keep node running until shutdown request
	while not rospy.is_shutdown():
	
csvfile.close()
