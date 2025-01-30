import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import GcodeParserV2
import TrajectoryPlanner
import DOFConversion
import DataTypes
import numpy as np
import matplotlib.pyplot as plt
import sys



def genTrajectory(file, a=9, hz=50, feedRate=1.0, rapidFeed=2.0, defaultLengthUnits="mm", toolFrameOffset=[0.0,0.0, 0.0]):
    '''call necessary functions to plan a trajectory from gcode'''
    parser = GcodeParserV2.GcodeParserV2(feedRate=feedRate, rapidFeed=rapidFeed, defaultLengthUnits=defaultLengthUnits, toolFrameOffset=toolFrameOffset)

    if parser.parseFile(file):
        return 0

    wayPoints = parser.evaluateGcode()

    trajectory = TrajectoryPlanner.planTrajectory(wayPoints, a=a, hz=hz)

    trajectory = DOFConversion.AddFixed6DOF(trajectory)

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

if __name__=="__main__":
    print("generating trajectory")
    traj = genTrajectory(sys.argv[1], toolFrameOffset=[0.0, 20.0, 0.0])

    plotTrajectory(traj)

    print("saving trajectory")
    saveTrajectory(sys.argv[2], traj)