import rospy 
from tormach_controller.msg import pose, forceTorque, MovePoseAction, MovePoseGoal,MovePoseResult,MovePoseFeedback
from sensor_msgs.msg import JointState
import actionlib
import numpy as np



class TMovePoseAction (object):

    _feedback = MovePoseFeedback()
    _result=MovePoseResult()
    currentPose=np.array([0,0,0,0,0,0])
    gotpose=False;
    goalpose=np.array([0,0,0,0,0,0])
    currentForce=0
    
    def __init__(self, name):
        self._action_name=name
        self._as=actionlib.SimpleActionServer(self._action_name, MovePoseAction,execute_cb=self.execute_cb,auto_start=False)
        self._as.start()
        
    def execute_cb(self,goal):
        #start subscriber nodes
        currentPoseSub=rospy.Subscriber("/joint_states", JointState, callback=jointStateCallback)
        currentForceSub=rospy.Subscriber("/eeforce", forceTorque, callback=self.forceCallback)
        postol=goal.postol
        vel=goal.vel
        forcetol=goal.forcetol
        self.goalpose=np.array([goal.goalx,goal.goaly,goal.goalz,goal.goali,goal.goalj,goal.goalk])
        while not self.gotpose:
            x=0
        success=1
        while (not np.all(abs(goalpose-self.currentpose)<=postol)) or self.currentForce>forcetol:
            #check if user aborted the proccess
            if self._as.is_preempted_requested():
                self._as.set_preempted()
                success=0
                break
            # do work here
            
        #return successful info flag
        if success:
            self._result.success=1
            self._as.set_succeeded(self._result)
        
    def jointStateCallback(self,msg):
        self.gotpose=True
        self.currentpose=np.array(msg.position[0:6])
        
    def forceCallback(self,msg):
        self.currentForce=msg.forcex*self.goalpose[3]+ msg.forcey*self.goalpose[4]+msg.forcez*self.goalpose[5]

if __name__ =='__main__':
    rospy.init_node('MovePose')
    server=TMovePoseAction(rospy.get_name())
    rospy.spin()
