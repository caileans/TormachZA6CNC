import rospy 
from time import sleep
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np



def voft(amax, vmax, ta, tv, tmove, t):
    """Returns the instantanious velocity at time t for a move that take tmove, a max veloctiy vmax, and a trapizoidal acceleration profile with a max amax, ramp time ta, and total tim tv


    """

    if t<= ta:
        return amax*t*t/2/ta
    elif t<= tv-ta:
        return amax*(t-ta/2)
    elif t<=tv:
        return vmax-amax*((t-tv)**2)/2/ta
    elif t<=tmove-tv:
        return vmax
    elif t<=tmove-tv+ta:
        return vmax-amax*((t+tv-tmove)**2)/2/ta
    elif t<=tmove-ta:
        return vmax -amax*(ta/2+t-tmove+tv-ta)
    elif t<=tmove:
        return amax*((tmove-t)**2)/2/ta
    else:
        return 0



def genpath(hz, alpha):
    """generates a 1d path using trapizoidal acceleration at a specified frequency hz


     """
    # amax=3 #rad/s/s
    # ta=.075 #s
    # vmax= .3 #rad/s
    # tm =.5 #s

    amax=.3 #rad/s/s
    ta=.25 #s
    vmax= .3 #rad/s
    tm =5 #s

    # amax=1#rad/s/s
    # ta=.25 #s
    # vmax= .6 #rad/s
    # tm =2.5 #s


    # amax=2#rad/s/s
    # ta=.25 #s
    # vmax= .9 #rad/s
    # tm =2 #s

    # amax=5#rad/s/s
    # ta=.25 #s
    # vmax= .9 #rad/s
    # tm =1.5 #s

    # amax=8#rad/s/s
    # ta=.25 #s
    # vmax= 2 #rad/s
    # tm =1.2 #s

    tv= vmax/amax+ta   #rad/s


    time=np.linspace(0,tm,num=int(hz*tm))
    v=np.zeros(int(hz*tm))
    pos=np.zeros(int(hz*tm)+2)
    c=1

    #how much overshoot in position
    velprev=0;
    for t in time:
        vel=voft(amax,vmax,ta,tv,tm,t)
        v[c-1]=vel
        pos[c]=pos[c-1]+vel/hz*alpha-velprev/hz*(alpha-1)
        c+=1
        velprev=vel
    # plt.plot(time,v)
    # plt.plot(time,pos[1:])
    # plt.show()
    pos[-1]=pos[-2]-velprev/hz*(alpha-1)
    return pos[1:]



def movepath(hz):

    alpha=2
    pos=genpath(hz,alpha)

    rate=rospy.Rate(hz)
    pnt=JointTrajectoryPoint()
    # pnt.positions=[0.15,.22,-.17,.63,.3,.97,25.88,-9.25]
    pnt.positions=[0.0,0.0,0.0,0.0,0.0,0.0,0.1,0.1]
    # pnt.positions=[600,60,830,-146,-70,-28]
    pnt.effort=[]
    pnt.velocities=[]
    # pnt.velocities=[1,0,0,0,0,0,0,0]
    pnt.accelerations=[]
    pnt.time_from_start.nsecs=int(alpha*(10**9)/hz)
    # rospy.loginfo(pnt)
    pubmsg=JointTrajectory()
    pubmsg.joint_names=['joint_1','joint_2','joint_3','joint_4','joint_5','joint_6','tcp_lin','tcp_rot']
        # pubmsg.joint_names=['X','Y','Z','A','B','C']
    c=0
    while not  rospy.is_shutdown():
        if c>= np.size(pos):
            break
        pnt.positions=[pos[c],pos[c],-1*pos[c],pos[c],pos[c],pos[c],.1,.1]
        pubmsg.points=[pnt]
        pubmsg.header.stamp=rospy.Time.now()
        forcePub.publish(pubmsg)
        c+=1
        # break
        rate.sleep()



# NOTE THIS NODE IS IN RADIANS!!!!!!!!!!!!!
#publishing a new position will overwrite the current move
#Note: this doesnt work for cartesian space
if __name__=='__main__':
    
    #start the test node
    rospy.init_node("testpub")

    forcePub=rospy.Publisher('/position_trajectory_controller/command', JointTrajectory, queue_size=1)
    sleep(60)
    print("prob conected")
    # put movement/publish rate here
    # movepath(20)

    for i in range(9):
        i+=2
        # print
        movepath(10*i)
        sleep(1)
        pnt=JointTrajectoryPoint()
        # pnt.positions=[0.15,.22,-.17,.63,.3,.97,25.88,-9.25]
        pnt.positions=[0.0,0.0,0.0,0.0,0.0,0.0,0.1,0.1]
        # pnt.positions=[600,60,830,-146,-70,-28]
        pnt.effort=[]
        pnt.velocities=[]
        # pnt.velocities=[1,0,0,0,0,0,0,0]
        pnt.accelerations=[]
        # pnt.time_from_start.nsecs=int(2*(10**9)/hz)
        # rospy.loginfo(pnt)
        pubmsg=JointTrajectory()
        pubmsg.joint_names=['joint_1','joint_2','joint_3','joint_4','joint_5','joint_6','tcp_lin','tcp_rot']
        pnt.time_from_start.secs=3
        pubmsg.points=[pnt]
        pubmsg.header.stamp=rospy.Time.now()
        forcePub.publish(pubmsg)
        sleep(5)
        # pubmsg.joint_names=['X','Y','Z','A','B','C']


    # rate=rospy.Rate(10)
    # pnt=JointTrajectoryPoint()
    # # pnt.positions=[0.15,.22,-.17,.63,.3,.97,25.88,-9.25]
    # pnt.positions=[.1,.1,.1,.1,.1,.1,.1,.1]
    # # pnt.positions=[600,60,830,-146,-70,-28]
    # pnt.effort=[]
    # pnt.velocities=[]
    # # pnt.velocities=[1,0,0,0,0,0,0,0]
    # pnt.accelerations=[]
    # pnt.time_from_start.secs=1
    # rospy.loginfo(pnt)

    # pubmsg=JointTrajectory()
    # pubmsg.points=[pnt]
    # pubmsg.joint_names=['joint_1','joint_2','joint_3','joint_4','joint_5','joint_6','tcp_lin','tcp_rot']
    # # pubmsg.joint_names=['X','Y','Z','A','B','C']
    # pubmsg.header.stamp=rospy.Time.now()
    # forcePub.publish(pubmsg)
    # print("done")
    # sleep(.9)
    # pnt.positions=[.3,.1,.1,.1,.1,.1,.1,.1]
    # pubmsg.points=[pnt]
    # pnt.time_from_start.secs=1
    # pubmsg.header.stamp=rospy.Time.now()
    # forcePub.publish(pubmsg)
    # sleep(.9)
    # # pnt.positions=[.3,.22,-.17,.63,.3,.97,25.88,-9.25]
    # pnt.positions=[.3,-.2,.1,.1,.1,.1,.1,.1]
    # pubmsg.points=[pnt]
    # pnt.time_from_start.secs=1
    # pubmsg.header.stamp=rospy.Time.now()
    # forcePub.publish(pubmsg)
    # sleep(.9)
    # pnt.positions=[.1,-.2,.1,.1,.1,.1,.1,.1]
    # pubmsg.points=[pnt]
    # pnt.time_from_start.secs=1
    # pubmsg.header.stamp=rospy.Time.now()
    # forcePub.publish(pubmsg)
    # sleep(.9)
    # pnt.positions=[.1,.1,.1,.1,.1,.1,.1,.1]
    # pubmsg.points=[pnt]
    # pnt.time_from_start.secs=1
    # pubmsg.header.stamp=rospy.Time.now()
    # forcePub.publish(pubmsg)
    # sleep(5)
    # #keep node running until shutdown request
    # while not  rospy.is_shutdown():
        
    #     break
