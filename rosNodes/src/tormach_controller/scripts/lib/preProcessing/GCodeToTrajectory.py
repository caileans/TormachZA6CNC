import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import GcodeParserV2
import TrajectoryPlanner
import DOFConversion
import toolOffset
import DataTypes
import numpy as np
import sys
import general_robotics_toolbox as grtb



def genTrajectory(file, a=9, hz=50, feedRate=1.0, rapidFeed=2.0, defaultLengthUnits="mm", toolFrameOffset=[0.0,0.0, 0.0], origin=[562.0,0.0,866.0], toolIJKInit=[0.0,0.0,1.0], pureRotVel = np.pi/2, tOffset=[0,0]):
    '''
    call necessary functions to plan a trajectory from gcode
    
    Inputs:
        file: the gcode file/file path
        a: the maximum acceleration to use in trajectory planning
        hz: the frequency to plan the trajectory points at
        feedRate: the default feedrate to use for Gcode parsing
        rapidFeed: the default rapid feedrate to use for Gcode parsing
        defaultLengthUnits: the default length units ("in" or "mm") to use for Gcode parsing
        toolFrameOffset: the offset from the global coordinent system to the Gcode coordinant system
        origin: the end effector starting and ending location
        toolIJKInit: the initial tool orientation
        pureRotVel: the rotational velocity to use for movements with only a tool orientation change
        tOffset: the tooloffset from the end effector center

    Outputs:
        trajectory: an array of TrajPoint data types; the trajectory that follows the gcode, with moves from and back to origin added in
    '''
    parser = GcodeParserV2.GcodeParserV2(feedRate=feedRate, rapidFeed=rapidFeed, defaultLengthUnits=defaultLengthUnits, toolFrameOffset=toolFrameOffset)
    # print(os.getcwd())
    if parser.parseFile(file):
        return 0 

    wayPoints = parser.evaluateGcode()

    wayPoints.append(DataTypes.WayPoint(pos=origin, toolVec=toolIJKInit, vel=(rapidFeed if defaultLengthUnits=="mm" else rapidFeed*25.4/60.0))) #add the origin to the end

    trajectory = TrajectoryPlanner.planTrajectory(wayPoints, a=a, hz=hz, pInit=origin, ijkInit=toolIJKInit, pureRotVel = pureRotVel)

    trajectory = toolOffset.toolOffset(trajectory, [0, tOffset[1]], nFadeIn=20)

    ### uncomment whichever one you want to use. Fixed will keep tool upright
    # trajectory = DOFConversion.AddFixed6DOF(trajectory)
    trajectory = DOFConversion.Add6DofFrom5(trajectory, quadrant=2)

    trajectory = toolOffset.toolOffset(trajectory, [tOffset[0], 0], nFadeIn=20)

    return trajectory



def saveTrajectory(file, trajectory):
    '''
    write the trajectory to a file
    
    Inputs:
        file: the file to save the trajectory to
        trajectory: an array of TrajPoint data points
    '''
    with open(file, "w") as f:
        for trajPoint in trajectory:
            f.write(str(trajPoint)+"\n")


def plotTrajectory(trajectory, hz=50):
    '''
    plot information about the trajectory in 2D. for testing/verification. modify what is plotted as needed
    '''
    import matplotlib.pyplot as plt
    num = len(trajectory)
    x = np.zeros(num)
    y = np.zeros(num)
    z = np.zeros(num)
    i = np.zeros(num)
    j = np.zeros(num)
    k = np.zeros(num)
    a = np.zeros(num)
    b = np.zeros(num)
    c = np.zeros(num)
    i_j6 = np.zeros(num)
    j_j6 = np.zeros(num)
    k_j6 = np.zeros(num)
    time = np.zeros(num)
    lastTime = 0.0
    for n in range(num):
        point = trajectory[n]
        x[n] = point.pos[0]
        y[n] = point.pos[1]
        z[n] = point.pos[2]
        i[n] = point.toolVec[0]
        j[n] = point.toolVec[1]
        k[n] = point.toolVec[2]
        a[n] = point.rot[0]
        b[n] = point.rot[1]
        c[n] = point.rot[2]
        lastTime = lastTime + 1.0/hz
        time[n] = lastTime


    # plt.figure(2)
    # plt.plot(i, k, '.')

    plt.figure(3)
    plt.plot(time, a, '+')
    plt.plot(time, b, 'x')
    plt.plot(time, c, '.')

    plt.show()

def plot3DTrajectory(trajectory, hz=50, nmin=0, nmaxOffset=0):
    '''
    plots the trajectory in 3D, including tool vectors and j6 vectors. this plotting can be hard on a graphics card if nmin and nmaxOffset are not set appropriately

    Inputs:
        trajectory: an array of TrajPoint data types; the trajectory
        hz: the frequency the trajectory was generated at (to plot against time)
        nmin: the trajectory index to start plotting at
        nmaxOffset: the number data points on the end of the trajectory to not plot
    '''
    import matplotlib.pyplot as plt
    num = len(trajectory)
    x = np.zeros(num)
    y = np.zeros(num)
    z = np.zeros(num)
    i = np.zeros(num)
    j = np.zeros(num)
    k = np.zeros(num)
    i_j6 = np.zeros(num)
    j_j6 = np.zeros(num)
    k_j6 = np.zeros(num)
    ijk_fromabc = np.zeros([num, 3])
    time = np.zeros(num)
    lastTime = 0.0
    for n in range(num):
        point = trajectory[n]
        x[n] = point.pos[0]
        y[n] = point.pos[1]
        z[n] = point.pos[2]
        i[n] = point.toolVec[0]
        j[n] = point.toolVec[1]
        k[n] = point.toolVec[2]
        lastTime = lastTime + 1.0/hz
        time[n] = lastTime

        # yaw = point.rot[2]
        # pitch = point.rot[1]

        yaw = np.deg2rad(point.rot[2])
        pitch = np.deg2rad(point.rot[1])
        roll = np.deg2rad(point.rot[0])

        
        # print(f"ti: {i[n]}    tj: {j[n]}    tk: {k[n]}   roll: {point.rot[2]}   pitch: {point.rot[1]}   yaw: {point.rot[0]}")
        
        i_j6[n] = np.cos(yaw)*np.cos(pitch)
        j_j6[n] = np.sin(yaw)*np.cos(pitch)
        k_j6[n] = -np.sin(pitch)

        # i_t[n] = np.sin(pitch)*np.
        # j_t[n] = 
        # k_t[n] = 

        ijk_fromabc[n, :] = np.matmul(grtb.rpy2R(np.deg2rad(point.rot)), np.array([0,0,1.0]))
        # angle = np.acos(np.dot(ijk_fromabc[n], [i[n], j[n], k[n]])/np.linalg.norm([i[n], j[n], k[n]]))
        # if angle > 0.0001:
        #     print(f"ijk_fromabc: {ijk_fromabc[n, :]}    ijk: {i[n], j[n], k[n]} angle: {angle}")



    ax = plt.figure(4).add_subplot(projection='3d')

    # nmin = 350
    nmax = len(x)-nmaxOffset
    ax.quiver(x[nmin:nmax], y[nmin:nmax], z[nmin:nmax], i[nmin:nmax], j[nmin:nmax], k[nmin:nmax], length=10, normalize=True, color='b')
    ax.quiver(x[nmin:nmax], y[nmin:nmax], z[nmin:nmax], i_j6[nmin:nmax], j_j6[nmin:nmax], k_j6[nmin:nmax], length=10, normalize=True, color='r')
    ax.quiver(x[nmin:nmax], y[nmin:nmax], z[nmin:nmax], ijk_fromabc[nmin:nmax, 0], ijk_fromabc[nmin:nmax, 1], ijk_fromabc[nmin:nmax, 2], length=8, normalize=True, color='g')
    
    ax.set_aspect('equal', adjustable='box')
    plt.show()


if __name__=="__main__":
    '''
    for testing
    '''
    import matplotlib.pyplot as plt
    print("generating trajectory")
    traj = genTrajectory(sys.argv[1], a=30, hz=7, feedRate=30, rapidFeed=30, toolFrameOffset=[400.0, 0.0, 400.0], pureRotVel=np.pi/5, tOffset=[10, 20])

    plotTrajectory(traj, hz=7)
    plot3DTrajectory(traj, hz=7)

    # print("saving trajectory")
    # saveTrajectory(sys.argv[2], traj)

    print("done")