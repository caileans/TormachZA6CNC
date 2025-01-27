import numpy as np
import matplotlib.pyplot as plt

def planTrajectory(wayPoints, a=9.0, hz=50):
    for i in range(len(wayPoints)):
        if i == 0:
            vi = 0
            p0 = pInit
        else:
            vi = (wayPoints[i-1].vel+wayPoints[i].vel)/2.0
            p0 = wayPoints[i-1].pos

        if i == len(wayPoints)-1:
            vf = 0
        else:
            vf = (wayPoints[i+1].vel+wayPoints[i].vel)/2.0
        
        vm = wayPoints[i].vel
        pf = wayPoints[i].pos

        genLinPath(hz, a, vi, vm, vf, p0, pf)


def lambdaOfK(amax, vi, vm, vf, ta, tv1, tm, tv2, k):
    ta = abs(vm - vi)/amax #time to go from vi to vm
    tc = abs(vf - vm)/amax #time to go from vm to vf
    tb = (pf - p0 - 0.5*(vi+vm)*t1 - 0.5*(vm+vf)*t3) #time to stay at vm
    t1 = ta
    t2 = ta + tb
    t3 = ta + tb + tc
    if k <= t1:
        return

def voft(amax, vi, vm, vf, ta, tv1, tm, tv2, t):
    """Returns the instantanious velocity at time t for a move that take tmove, a max veloctiy vmax, and a trapizoidal acceleration profile with a max amax, ramp time ta, and total tim tv


    """

    # if t<= ta:
    #     return amax*t*t/2/ta
    if t<= tv1-ta:
        return np.sign(vm-vi)*amax*(t-ta/2) + vi
    # elif t<=tv:
    #     return vmax-amax*((t-tv)**2)/2/ta
    elif t<=tm:
        return vm
    # elif t<=tmove-tv+ta:
    #     return vmax-amax*((t+tv-tmove)**2)/2/ta
    elif t<=tv2:
        # return vmax -amax*(ta/2+t-tmove+tv-ta)
        return vm + np.sign(vf-vm)*amax*(t-tm)
    # elif t<=tmove:
    #     return amax*((tmove-t)**2)/2/ta
    else:
        return 0



def genpath(hz, amax=1, vi = 0, vm = 0.3, vf = 0, p0 = 0, pf= 1):
    """generates a 1d path using trapizoidal acceleration at a specified frequency hz


     """
    ta = 0
    t1 = abs(vm - vi)/amax #time to go from vi to vm
    t3 = abs(vf - vm)/amax #time to go from vm to vf
    t2 = (pf - p0 - 0.5*(vi+vm)*t1 - 0.5*(vm+vf)*t3) #time to stay at vm
    tv1 = t1 
    tm = t1+t2
    tv2 = t1+t2+t3
    # tv= vmax/amax+ta   #rad/s

    if t2 < 0:
        print("WARNING: NOT ENOUGH TIME TO CREATE TRAJECTORY WITH GIVEN PARAMETERS")


    time=np.linspace(0,tv2,num=int(hz*tm))
    v=np.zeros(int(hz*tm))
    pos=np.zeros(int(hz*tm)+1)
    c=1

    # alpha=2 #how much overshoot in position
    velprev=0
    for t in time:
        vel=voft(amax, vi, vm, vf, ta, tv1, tm, tv2, t)
        v[c-1]=vel
        pos[c]=pos[c-1]+vel/hz #*overshoot-velprev/hz*(overshoot-1)
        c+=1
        velprev=vel
    # pos[-1]=pos[-2]-velprev/hz*(overshoot-1)
    plt.plot(time,v)
    plt.plot(time,pos[1:])
    plt.show()
    return pos[1:], v



if __name__=="__main__":
    genpath(200, 4, 1, 2, 1, 1, 5)
    genpath(200, 4, 0, 2, 3, 1, 5)
    genpath(200, 4, 5, 2, 1, 1, 5)
    genpath(200, 4, 5, 2, 4, 1, 5)

