import rospy 
from tormach_controller.msg import pose, forceTorque, MovePoseAction, MovePoseGoal,MovePoseResult,MovePoseFeedback
from sensor_msgs.msg import JointState
#need to do pip install read char before running
from readchar import readchar
import asyncio

pose=[0,0,0,0,0,0]
effort=[0,0,0,0,0,0]

async def pause(sec):
    await asyncio.sleep(sec)

def jointStateCallback(msg):
    #print("h")
    #rospy.loginfo(msg.effort);
    #print(np.array(msg.position)[0:6])
    #writer.writerow(msg.effort)
    pose=msg.position[0:6]
    effort=msg.effort

 def main():
    #start the buffer_node node
    rospy.init_node("buffer_node")    
    
    f=open('data.csv','w')
    
    #with open('data.csv','wb') as file:
    #	writer=csv.writer(csvfile)
    currentPoseSub=rospy.Subscriber("/joint_states", JointState,queue_size=1, callback=jointStateCallback)
    #keep node running until shutdown request
    while not  rospy.is_shutdown():
        c=readchar()
        task=loop.create_task(pause(1))
        loop.run_until_complete(task)
        f.write(str(pose)+','+str(effort)+'\n')
        if c=='e':
            break
    f.close()
    


if __name__=='__main__':
   main()
            
    #csvfile.close()


    
