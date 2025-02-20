import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))+"/../"))

import numpy as np
import math
import DataTypes
import CircleFunctions
import InverseKinematics



def planTrajectory(wayPoints, a=1, hz=50, pInit=[562.0,0.0,866.0], ijkInit=[0.0,0.0,1.0], pureRotVel = np.pi/2):
    traj = []

    for i in range(len(wayPoints)):
        ### get the v and p information from the wayPoint
        if i == 0:
            vi = 0
            p0 = np.array(pInit)
            ijk0 = np.array(ijkInit)
        else:
            vi = (wayPoints[i-1].vel+wayPoints[i].vel)/2.0
            p0 = wayPoints[i-1].pos
            ijk0 = wayPoints[i-1].toolVec

        if i == len(wayPoints)-1:
            vf = 0.0
        else:
            vf = (wayPoints[i+1].vel+wayPoints[i].vel)/2.0
        
        vm = wayPoints[i].vel
        pf = wayPoints[i].pos
        ijkf = wayPoints[i].toolVec

        ### if it's linear motion
        if (wayPoints[i].rotAxis == np.array([0.0,0.0,0.0])).all():
            points = genLinPath(hz, a, vi, vm, vf, p0, pf, ijk0, ijkf, pureRotVel)
        else:
            points = genCircPath(hz, a, vi, vm, vf, p0, pf, wayPoints[i])
        # points = genLinPath(hz, a, vi, vm, vf, p0, pf, ijk0, ijkf)

        traj.extend(points)

    return traj

def genLinPath(hz, a, vi, vm, vf, p0, pf, ijk0, ijkf, rotVel):
    dp = pf - p0
    dijk = ijkf - ijk0

    distance = np.linalg.norm(dp)

    ijkCross = np.cross(ijk0, ijkf)
    if not all(ijkCross == 0):
        ijkCross = ijkCross/np.linalg.norm(ijkCross)
    rotDist = math.acos(np.dot(ijkf/np.linalg.norm(ijkf), ijk0/np.linalg.norm(ijk0))*0.9999) #*np.sign(ijkCross)

    # print(f"rotdist: {str(rotDist)}   cross: {str(ijkCross)}")

    if distance == 0:
        if not rotDist == 0:
            distance = rotDist
            vi = vm = vf = rotVel
        else:
            print("neither ijk or p change. can't generate trajectory")
            return []

    path = genPath(hz, a, vi, vm, vf, 0.0, distance)/distance

    points = []
    for point in path:
        pos = p0+dp*point
        # ijk = ijk0+dijk*point
        ijk = np.matmul(InverseKinematics.getR(ijkCross, rotDist*point), ijk0)
        R = InverseKinematics.getR(ijkCross, rotDist*point)
        # ijk = np.array([R[0,0]*ijk0[0] + R[0,1]*ijk0[1] + R[0,2]*ijk0[2],
        # R[1,0]*ijk0[0] + R[1,1]*ijk0[1] + R[1,2]*ijk0[2],
        # R[2,0]*ijk0[0] + R[2,1]*ijk0[1] + R[2,2]*ijk0[2]])

        # print(f"ijk: {str(ijk)}   pos: {str(pos)}   point: {str(point)}   rot: {str(math.acos(np.dot(ijk/np.linalg.norm(ijk), ijk0/np.linalg.norm(ijk0))))}   R: {str(R)}")

        points.append(DataTypes.TrajPoint(pos=pos, toolVec=ijk))

    return points
    

def genCircPath(hz, a, vi, vm, vf, p0, pf, wayPoint):
    rad = np.linalg.norm(wayPoint.circijk)
    vi_angular = vi/rad
    vm_angular = vm/rad
    vf_angular = vf/rad
    a_angular = a/rad

    c=p0+wayPoint.circijk

    theta,rcs,ar,zm = CircleFunctions.getTheta(c,p0,pf,wayPoint.rotAxis)

    path = genPath(hz, a_angular, vi_angular, vm_angular, vf_angular, 0, theta[1])

    points = []
    for t in path:
        # compute the cart point at each theta along the circle
        # xyz = pCenter +r*r2dx*cos(thetaA2)+r*r2dy*sin(thetaA2)+ahat.dot(pFinal-pInitial)*ahat/2
        pos = c + CircleFunctions.getPoint(rcs,ar,zm,t,theta[1])
        points.append(DataTypes.TrajPoint(pos=pos, toolVec=wayPoint.toolVec))

    return points

# def voft(amax, vi, vm, vf, ta, tv1, tm, tv2, t):
#     """Returns the instantanious velocity at time t for a move that take tmove, a max veloctiy vmax, and a trapizoidal acceleration profile with a max amax, ramp time ta, and total tim tv


#     """

#     # if t<= ta:
#     #     return amax*t*t/2/ta
#     if t<= tv1-ta:
#         return np.sign(vm-vi)*amax*(t-ta/2) + vi
#     # elif t<=tv:
#     #     return vmax-amax*((t-tv)**2)/2/ta
#     elif t<=tm:
#         return vm
#     # elif t<=tmove-tv+ta:
#     #     return vmax-amax*((t+tv-tmove)**2)/2/ta
#     elif t<=tv2:
#         # return vmax -amax*(ta/2+t-tmove+tv-ta)
#         return vm + np.sign(vf-vm)*amax*(t-tm)
#     # elif t<=tmove:
#     #     return amax*((tmove-t)**2)/2/ta
#     else:
#         return 0

def genPath(hz, a=1, vi=0, vm=0.3, vf=0, p0=0, pf=1):
    """generates a 1d path using trapizoidal acceleration at a specified frequency hz


     """
    ta = abs(vm - vi)/a #time to go from vi to vm
    tc = abs(vf - vm)/a #time to go from vm to vf
    tb = (pf - p0 - 0.5*(vi+vm)*ta - 0.5*(vm+vf)*tc)/vm #time to stay at vm
    t1 = ta
    t2 = ta + tb
    t3 = ta + tb + tc

    if tb < 0:
        print(f"Trajectory Planner Error: Not enough time to move from {p0} to {pf}")

    time=np.linspace(0,t3,num=int(hz*t3))
    pos=np.zeros(int(hz*t3))

    for i in range(0, len(time)):
        pos[i] = pOft(a, vi, vm, vf, p0, pf, t1, t2, t3, time[i])

    return pos

def pOft(a, vi, vm, vf, p0, pf, t1, t2, t3, t):
    c1 = np.sign(vm-vi)*a
    c2 = np.sign(vf-vm)*a
    if t <= t1:
        return 0.5*c1*t**2 + vi*t + p0
    elif t <= t2:
        return (vi + c1*t1)*t - 0.5*c1*t1**2 + p0
    elif t <= t3:
        return 0.5*c2*t**2 + (vi + c1*t1 - c2*t2)*t - 0.5*c1*t1**2 + 0.5*c2*t2**2 + p0
    else:
        return 0



if __name__=="__main__":
    # genpath(200, 4, 1, 2, 1, 1, 5)
    # genpath(200, 4, 0, 2, 3, 1, 5)
    # genpath(200, 4, 5, 2, 1, 1, 5)
    # genpath(200, 4, 5, 2, 4, 1, 5)
    import matplotlib.pyplot as plt

    vi = 3.0
    vm = 3.0
    vf = 3.0
    a = 9.0
    p0 = np.array([0, 0, 0])
    pf = np.array([0.0, 5.8531, 0.0])
    dp = pf-p0

    hz = 50

    ta = abs(vm - vi)/a #time to go from vi to vm
    tc = abs(vf - vm)/a #time to go from vm to vf
    tb = (np.linalg.norm(dp) - 0 - 0.5*(vi+vm)*ta - 0.5*(vm+vf)*tc) #time to stay at vm
    # t1 = ta
    # t2 = ta + tb
    t3 = ta + tb + tc

    time=np.linspace(0,t3,num=int(hz*t3))
    # pos=np.zeros(int(hz*t3))
    # pos1 = genPath(hz, a, vi, vm, vf, p0, pf)
    pos2 = genPath(hz, a, vi, vm, vf, 0.0, np.linalg.norm(dp))/np.linalg.norm(dp)

    # for i in range(0, len(time)):
    #     pos[i] = pOft(a, vi, vm, vf, p0, pf, t1, t2, t3, time[i])

    # plt.plot(time, pos1)
    plt.plot(time, pos2)
    plt.show()

