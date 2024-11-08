import rospy 
from tormach_controller.msg import pose, forceTorque, MovePoseAction, MovePoseGoal,MovePoseResult,MovePoseFeedback
from sensor_msgs.msg import JointState
from queue import Queue
import actionlib
import numpy as np
import math


#---------My code starts here----------------

#H=np.array([[0,0,0,1,0,1],[0,1,1,0,1,0],[1,0,0,0,0,0]])
#P=np.array([[0,.025,0,.123,.2965,.1,.1175],[0,0,-.001,0,.001,0,0],[.279,.171,.454,.035,0,0,0]])
#jointtype=np.array([0,0,0,0,0,0])
#print(H)
#print(P)
#tormach = Robot(H,P,jointtype)
#moveBuffer=Queue(maxsize=0)

def movepose_client():
#create action client
    client=actionlib.SimpleActionClient('movepose', MovePoseAction)
    #wait for action to boot up
    client.wait_for_server()
    #get next pose
    nextMove=moveBuffer.get()
    #set goal
    goal=MovePoseGoal(nextMove[0],nextMove[1],nextMove[2],nextMove[3],nextMove[4],nextMove[5])
    #send goal
    client.send_goal(goal)
    #wait for fininshing
    client.wait_for_result()
    #return results
    return client.get_result()
    
def pose_callback(msg):
    rospy.loginfo(msg)
    moveBuffer.put(np.array([msg.x,msg.y,msg.z,msg.i,msg.j,msg.k]))
    
def jointStateCallback(msg):
    print("h")
    rospy.loginfo(msg.effort);
    #print(np.array(msg.position)[0:6])
    #jac=robotjacobian(tormach,np.array(msg.position)[0:6])
    #print(jac)
    #in1=np.transpose(np.array(msg.effort)[0:6])
    #print(in1.shape)
    #in2=np.linalg.pinv(np.transpose(jac))
    #print(in2)
    #force=np.matmul(in2,in1)
    force=np.array([0,0,0,0,0,0])
    pubmsg=forceTorque()
    pubmsg.forcex=force[0];
    pubmsg.forcey=force[1];
    pubmsg.forcez=force[2];
    pubmsg.momenti=force[3];
    pubmsg.momentj=force[4];
    pubmsg.momentk=force[5];
    forcePub.publish(pubmsg)
    rospy.loginfo(force)
    #writer.writerow(msg.effort)

if __name__=='__main__':
    #start the buffer_node node
    rospy.init_node("buffer_node")
    #subscribe to the "/tormach/movePose" topic which has a pose msg type
    sub=rospy.Subscriber("/tormach/movePose", pose, callback=pose_callback)
    #with open('data.csv','w',newline='') as csvfile:
    #	writer=csv.writer(csvfile)
    currentPoseSub=rospy.Subscriber("/joint_states", JointState, callback=jointStateCallback)
    forcePub=rospy.Publisher('eeforce', forceTorque, queue_size=10)
    #keep node running until shutdown request
    while not  rospy.is_shutdown():
        if not moveBuffer.empty():
            result=movepose_client();
            
    #csvfile.close()


    
