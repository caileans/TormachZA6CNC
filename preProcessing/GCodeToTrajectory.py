import GcodeParserV2
import TrajectoryPlanner
import sys



def genTrajectory(file):
    '''call necessary functions to plan a trajectory from gcode'''
    parser = GcodeParserV2()

    if not parser.parseFile(file):
        return 0

    wayPoints = parser.evaluateGcode()

    trajectory = planTrajectory(wayPoints)

    return trajectory



def saveTrajectory(file, trajectory):
    '''write the trajectory to a file'''
    with open(file, "w") as f:
        for trajPoint in trajectory:
            f.write(trajPoint)



if __name__=="__main__":
    print("generating trajectory")
    traj = genTrajectory(sys.argv[1])

    plotTrajectory(traj)

    print("saving trajectory")
    saveTrajectory(sys.argv[2], traj)