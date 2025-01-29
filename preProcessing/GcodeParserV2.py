import re
import numpy as np
import DataTypes


class GcodeParserV2:
    def __init__(self, feedRate=0, rapidFeed=0, defaultLengthUnits="mm", defaultAngleUnits="deg", defaultTimeUnits="s", toolOffset=[0,0,0]):
        self.setParameters(feedRate, rapidFeed, defaultLengthUnits, defaultAngleUnits, defaultTimeUnits, toolOffset)

    
    def setParameters(self, feedRate=0, rapidFeed=0, defaultLengthUnits="mm", defaultAngleUnits="deg", defaultTimeUnits="s", toolOffset=[0,0,0]):
        self.rapidFeed = rapidFeed
        self.feedRate = feedRate
        self.motionMode = 1
        self.lengthUnits = defaultLengthUnits
        self.angleUnits = defaultAngleUnits
        self.timeUnits = defaultTimeUnits
        self.toolPose = ToolPose()
        self.newToolPose = ToolPose()
        self.circCenter = [0,0,0]
        # self.botPose = BotPose()
        self.toolOffset = toolOffset


    def parseFile(self, file):
        #import the gcode
        try:
            with open(file, 'r') as f:
                gcode = f.read()
        except:
            print("failed to open file\n\r")
            return 0

        self.parsedGcode = parseAllLines(gcode)


    def evaluateGcode(self):
        wayPoints = []
        for block in self.parsedGcode:
            if evaluateGcodeBlock(block):
                # botPose = self.calcBotPose(self.newToolPose, self.toolOffset)
                point = DataTypes.WayPoint(pos=np.array([self.newToolPose.x, self.newToolPose.y, self.newToolPose.z]), toolVec=np.array([self.newToolPose.i, self.newToolPose.j, self.newToolPose.k]))
                if self.motionMode == 0:
                    # TRPLCommand = self.constructTRPLLine(self.botPose, self.rapidFeed)
                    # pos.append(botPose)
                    # vel.append(self.rapidFeed)
                    point.circijk=np.array([0,0,0])
                    point.vel=self.rapidFeed
                    point.motion=MotionType.line
                    
                if self.motionMode == 1:
                    # TRPLCommand = self.constructTRPLLine(self.botPose, self.feedRate)
                    # pos.append(botPose)
                    # vel.append(self.feedRate)
                    point.circijk=np.array([0,0,0])
                    point.vel=self.feedRate
                    point.motion=MotionType.line
                if self.motionMode == 2:
                    # circInterToolPose = self.getMidPoint(self.toolPose, self.newToolPose, np.array([self.circCenter[0],self.circCenter[1],self.circCenter[2]]), a= np.array([0,0,-1]))
                    # circInterBotPose = self.calcBotPose(circInterToolPose)
                    # TRPLCommand = self.constructTRPLCirc(self.botPose, circInterBotPose, self.feedRate)
                    point.circijk=np.array(self.circCenter)
                    point.vel=self.feedRate
                    point.motion=MotionType.cw
                if self.motionMode == 3:
                    # circInterToolPose = self.getMidPoint(self.toolPose, self.newToolPose, np.array([self.circCenter[0],self.circCenter[1],self.circCenter[2]]), a= np.array([0,0,1]))
                    # circInterBotPose = self.calcBotPose(circInterToolPose)
                    # TRPLCommand = self.constructTRPLCirc(self.botPose, circInterBotPose, self.feedRate)
                    point.circijk=np.array(self.circCenter)
                    point.vel=self.feedRate
                    point.motion=MotionType.ccw

                wayPoints.append(point)

        return wayPoints

            


    def parseAllLines(self, gcode):
        self.parsedLines = []
        for line in gcode.splitlines():
            self.parsedLine, self.errors = self.parseLine(line)
            if self.parsedLine:
                self.parsedLines.append(self.parsedLine)
            if self.errors:
                print("did not recognize "+str(self.errors)+" in '"+line+"'")

        # print(self.parsedLines)
        return self.parsedLines

    @staticmethod
    def parseLine(line):
        #strip all whitespace,
        line = (''.join(line.split())).replace(";", "").upper()
        line = re.sub(r"[\(\[].*?[\)\]]", "", line) #remove comments
        if line == "":
            return [], []
        GcodeRegexString = r"[A-Z][\d|.|-]+"
        unrecognizedCommands = list(filter(None, re.split(GcodeRegexString, line)))
        commands = re.findall(GcodeRegexString, line)
        for i in range(len(commands)):
            commands[i] = [commands[i][0], float(commands[i][1:])]


        # print(self.unrecognizedCommands)
        return commands, unrecognizedCommands

    def evaluateGcodeBlock(self, block):
#        print(block)
        # self.toolPose = self.newToolPose
        self.toolPose.x=self.newToolPose.x
        self.toolPose.y=self.newToolPose.y
        self.toolPose.z=self.newToolPose.z
        self.toolPose.i=self.newToolPose.i
        self.toolPose.j=self.newToolPose.j
        self.toolPose.k=self.newToolPose.k
        # self.newToolPose=DOF5Pose()
        newPose = False
        for i in range(len(block)):
            if block[i] == ['G', 0]:
                self.motionMode = 0
            elif block[i] == ['G', 1]:
                self.motionMode = 1
            elif block[i] == ['G', 2]:
                self.motionMode = 2
            elif block[i] == ['G', 3]:
                self.motionMode = 3
            # elif block[i][0] == 'F':
            #     self.feedRate = block[i][1]
            elif block[i][0] == 'X':
                newPose = True
                # self.newToolPose.x = block[i][1]
                self.newToolPose.y = -block[i][1]
            elif block[i][0] == 'Y':
                newPose = True
                # self.newToolPose.y = block[i][1]
                self.newToolPose.z = block[i][1]
            elif block[i][0] == 'Z':
                newPose = True
                # self.newToolPose.z = block[i][1]
                self.newToolPose.x = -block[i][1]
            elif block[i][0] == 'I':
                if self.motionMode == 0 or self.motionMode == 1:
                    newPose = True
                    # print("different")
                    self.newToolPose.i = block[i][1]
                else:
                    # print("print statements")
                    self.circCenter[0] = block[i][1]
            elif block[i][0] == 'J':
                if self.motionMode == 0 or self.motionMode == 1:
                    newPose = True
                    self.newToolPose.j = block[i][1]
                else:
                    self.circCenter[1] = block[i][1]
            elif block[i][0] == 'K':
                if self.motionMode == 0 or self.motionMode == 1:
                    newPose = True
                    self.newToolPose.k = block[i][1]
                else:
                    self.circCenter[2] = block[i][1]
            else:
                print("Error: " + str(block[i]) + " not found")
        
        return newPose


#interp = GcodeParser_custom("G01 XX1.1 Y1. Z1.;\n\n(asdfasd_)\n(asdf\nX1Y1.").parseAllLines()
# print(GcodeParser_custom.parseLine("G01"))

