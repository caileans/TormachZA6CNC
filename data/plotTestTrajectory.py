import numpy as np
import matplotlib.pyplot as plt
time=np.array([])
pose=np.array([[0,0]])
vel=np.array([[0,0]])
eff=np.array([[0,0]])
initialTime=0;


def voft(amax, vmax, ta, tv, tmove, t):
    """Returns the instantanious velocity at time t for a move that take tmove, a max veloctiy vmax, and a trapizoidal acceleration profile with a max amax, ramp time ta, and total tim tv


    """

    if t<= ta:
        return amax*t*t/2/ta;
    elif t<= tv-ta:
        return amax*(t-ta/2);
    elif t<=tv:
        return vmax-amax*((t-tv)**2)/2/ta
    elif t<=tmove-tv:
        return vmax;
    elif t<=tmove-tv+ta:
        return vmax-amax*((t+tv-tmove)**2)/2/ta;
    elif t<=tmove-ta:
        return vmax -amax*(ta/2+t-tmove+tv-ta);
    elif t<=tmove:
        return amax*((tmove-t)**2)/2/ta;
    else:
        return 0;

def genpath(hz):
    """ """
    amax=8#rad/s/s
    ta=.25 #s
    vmax= 2 #rad/s
    tm =1.2 #s

    tv= vmax/amax+ta;   #rad/s

    
    time=np.linspace(0,tm,num=int(hz*tm));
    v=np.zeros(int(hz*tm))
    pos=np.zeros(int(hz*tm)+1)
    c=1;

    alpha=1; #how much overshoot in position

    for t in time:
        vel=voft(amax,vmax,ta,tv,tm,t);
        v[c-1]=vel
        pos[c]=pos[c-1]+vel/hz*alpha
        c+=1
    plt.plot(time,v)
    plt.plot(time,pos[1:])
    plt.show()
    print(pos[1:])

genpath(20)