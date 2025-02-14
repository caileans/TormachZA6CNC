import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import GcodeParserV2
import TrajectoryPlanner
import DOFConversion
import DataTypes
import numpy as np
import sys



def genTrajectory(file, a=9, hz=50, feedRate=1.0, rapidFeed=2.0, defaultLengthUnits="mm", toolFrameOffset=[0.0,0.0, 0.0], origin=[562.0,0.0,866.0], toolIJKInit=[0.0,0.0,1.0]):
    '''call necessary functions to plan a trajectory from gcode'''
    parser = GcodeParserV2.GcodeParserV2(feedRate=feedRate, rapidFeed=rapidFeed, defaultLengthUnits=defaultLengthUnits, toolFrameOffset=toolFrameOffset)
    # print(os.getcwd())
    if parser.parseFile(file):
        return 0 

    wayPoints = parser.evaluateGcode()

    wayPoints.append(DataTypes.WayPoint(pos=origin, toolVec=toolIJKInit, vel=(rapidFeed if defaultLengthUnits=="mm" else rapidFeed*25.4/60.0))) #add the origin to the end

    trajectory = TrajectoryPlanner.planTrajectory(wayPoints, a=a, hz=hz, pInit=origin, ijkInit=toolIJKInit)

    ### uncomment whichever one you want to use. Fixed will keep tool upright
    # trajectory = DOFConversion.AddFixed6DOF(trajectory)
    trajectory = DOFConversion.Add6DofFrom5(trajectory, quadrant=2)

    return trajectory



def saveTrajectory(file, trajectory):
    '''write the trajectory to a file'''
    with open(file, "w") as f:
        for trajPoint in trajectory:
            f.write(str(trajPoint)+"\n")


def plotTrajectory(trajectory):
    x = []
    y = []
    time = []
    lastTime = 0.0
    for point in trajectory:
        x.append(point.pos[0])
        y.append(point.pos[1])
        lastTime = lastTime + 1.0/50
        time.append(lastTime)
        # vel = np.linalg.norm
    plt.plot(x, y, '.')


    plt.figure(2)
    plt.plot(time, x, '.')
    plt.plot(time, y, '.')

    plt.show()

def plot3DTrajectory(trajectory, hz=50):
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

        yaw = np.deg2rad(point.rot[0])
        pitch = np.deg2rad(point.rot[1])
        
        i_j6[n] = np.cos(yaw)*np.cos(pitch)
        j_j6[n] = np.sin(yaw)*np.cos(pitch)
        k_j6[n] = -np.sin(pitch)



    ax = plt.figure().add_subplot(projection='3d')

    nmin = 0
    nmax = len(x)
    ax.quiver(x[nmin:nmax], y[nmin:nmax], z[nmin:nmax], i[nmin:nmax], j[nmin:nmax], k[nmin:nmax], length=10, normalize=True, color='b')
    ax.quiver(x[nmin:nmax], y[nmin:nmax], z[nmin:nmax], i_j6[nmin:nmax], j_j6[nmin:nmax], k_j6[nmin:nmax], length=10, normalize=True, color='r')

    plt.show()


if __name__=="__main__":
    import matplotlib.pyplot as plt
    print("generating trajectory")
    traj = genTrajectory(sys.argv[1], hz=1, feedRate=10, rapidFeed=10, toolFrameOffset=[0.0, 20.0, 0.0])

    # plotTrajectory(traj)
    plot3DTrajectory(traj, hz=1)

    # print("saving trajectory")
    # saveTrajectory(sys.argv[2], traj)

    print("done")