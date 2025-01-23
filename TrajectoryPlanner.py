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



def genpath(hz, amax=1, ta = 0.25, vmax = 0.3, tm = 5, overshoot=2):
    """generates a 1d path using trapizoidal acceleration at a specified frequency hz


     """
    # amax=3 #rad/s/s
    # ta=.075 #s
    # vmax= .3 #rad/s
    # tm =.5 #s

    # amax=.3 #rad/s/s
    # ta=.25 #s
    # vmax= .3 #rad/s
    # tm =5 #s

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

    # alpha=2 #how much overshoot in position
    velprev=0
    for t in time:
        vel=voft(amax,vmax,ta,tv,tm,t)
        v[c-1]=vel
        pos[c]=pos[c-1]+vel/hz*overshoot-velprev/hz*(overshoot-1)
        c+=1
        velprev=vel
    pos[-1]=pos[-2]-velprev/hz*(overshoot-1)
    return pos[1:], v