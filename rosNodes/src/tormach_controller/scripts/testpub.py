import rospy 
from time import sleep
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
    
# NOTE THIS NODE IS IN RADIANS!!!!!!!!!!!!!
#publishing a new position will overwrite the current move
if __name__=='__main__':
    
    #start the test node
    rospy.init_node("testpub")

    forcePub=rospy.Publisher('/position_trajectory_controller/command', JointTrajectory, queue_size=1)
    sleep(60)
    print("prob conected")
    rate=rospy.Rate(10)
    pnt=JointTrajectoryPoint()
    # pnt.positions=[0.15,.22,-.17,.63,.3,.97,25.88,-9.25]
    pnt.positions=[.1,.1,.1,.1,.1,.1,.1,.1];
    pnt.effort=[];
    pnt.velocities=[];
    # pnt.velocities=[1,0,0,0,0,0,0,0]
    pnt.accelerations=[];
    pnt.time_from_start.secs=1
    rospy.loginfo(pnt)

    pubmsg=JointTrajectory();
    pubmsg.points=[pnt];
    pubmsg.joint_names=['joint_1','joint_2','joint_3','joint_4','joint_5','joint_6','tcp_lin','tcp_rot']

    pubmsg.header.stamp=rospy.Time.now()
    forcePub.publish(pubmsg)
    print("done")
    sleep(.9)
    pnt.positions=[.3,.1,.1,.1,.1,.1,.1,.1];
    pubmsg.points=[pnt];
    pnt.time_from_start.secs=1
    pubmsg.header.stamp=rospy.Time.now()
    forcePub.publish(pubmsg)
    sleep(.9)
    # pnt.positions=[.3,.22,-.17,.63,.3,.97,25.88,-9.25]
    pnt.positions=[.3,-.2,.1,.1,.1,.1,.1,.1];
    pubmsg.points=[pnt];
    pnt.time_from_start.secs=1
    pubmsg.header.stamp=rospy.Time.now()
    forcePub.publish(pubmsg)
    sleep(.9)
    pnt.positions=[.1,-.2,.1,.1,.1,.1,.1,.1];
    pubmsg.points=[pnt];
    pnt.time_from_start.secs=1
    pubmsg.header.stamp=rospy.Time.now()
    forcePub.publish(pubmsg)
    sleep(.9)
    pnt.positions=[.1,.1,.1,.1,.1,.1,.1,.1];
    pubmsg.points=[pnt];
    pnt.time_from_start.secs=1
    pubmsg.header.stamp=rospy.Time.now()
    forcePub.publish(pubmsg)
    sleep(5)
    #keep node running until shutdown request
    while not  rospy.is_shutdown():
        
        break