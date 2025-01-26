import GcodeParserV2



def genTrajectory():
    parser = GcodeParserV2()

    if not parser.parseFile(file):
        return 0

    wayPoints = parser.evaluateGcode()

    trajectory = planTrajectory(wayPoints)

    return trajectory


