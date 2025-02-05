import general_robotics_toolbox as grtb
from ik_geo import Robot
import numpy as np

H=np.array([[.0,.0,.0,1.0,.0,1.0],[.0,1.0,1.0,.0,1.0,.0],[1.0,.0,.0,.0,.0,.0]])
# H=np.transpose(H)
P=np.array([[.0,.025,.0,.123,.2965,.1,.1175],[.0,.0,.0,.0,.0,.0,.0],[.279,.171,.454,.035,.0,.0,.0]])*1000.0 #approximated without 1mm offsets
# P=np.transpose(P)
# print(np.shape(P))
robotfk=grtb.Robot(H,P,[0,0,0,0,0,0])

P=np.array([[.0,.025,.0,.123+.2965,.0,.0,.2175],[.0,.0,.0,.0,.0,.0,.0],[.279,.171,.454,.035,.0,.0,.0]])*1000.0 #approximated without 1mm offsets
H=np.transpose(H)
#approximated without 1mm offsets
P=np.transpose(P)
print(P)
# print(H)
robotik=Robot.spherical_two_parallel(H,P)

theta=[90.0,20.0,20.0,0.0,-40.0,0.0]
theta=[.0,.0,10.0,.0,-0.000005,.0]

theta=np.array(theta)*np.pi/180.0
fwdkin=grtb.fwdkin(robotfk,theta)
print(theta)
# print(robotik.get_ik_sorted(fwdkin.R,fwdkin.p))
print(robotik.get_ik_sorted(np.transpose(fwdkin.R),fwdkin.p))