import rospy 
from tormach_controller.msg import pose, forceTorque, MovePoseAction, MovePoseGoal,MovePoseResult,MovePoseFeedback
from sensor_msgs.msg import JointState
#need to do pip install read char before running
from readchar import readchar



pose=[0,0,0,0,0,0]
effort=[0,0,0,0,0,0]
f=open('data.csv','w')


def jointStateCallback(msg):
    #print("h")
    #rospy.loginfo(msg.effort);
    #print(np.array(msg.position)[0:6])
    #writer.writerow(msg.effort)
    pose=msg.position[0:6]
    effort=msg.effort[0:6]
    f.write(str(pose)+','+str(effort)+'\n')

def main():
    #start the buffer_node node
    rospy.init_node("buffer_node")    
    
    

    while not  rospy.is_shutdown():
        c=readchar()
        print(c)
        jointStateCallback(rospy.wait_for_message("/joint_states", JointState, timeout=5))
        if c=='e':
            break
    f.close()
    


if __name__=='__main__':
   main()
            
    #csvfile.close()


    
