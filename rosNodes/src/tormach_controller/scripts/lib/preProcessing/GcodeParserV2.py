import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import numpy as np
# from DataTypes import ToolPose, WayPoint
import DataTypes

# x = ToolPose()


class GcodeParserV2:
    def __init__(self, feedRate=1.0, rapidFeed=2.0, defaultLengthUnits="mm", toolFrameOffset=[0.0,0.0,0.0]):
        self.setParameters(feedRate, rapidFeed, defaultLengthUnits, toolFrameOffset)

    
    def setParameters(self, feedRate=1.0, rapidFeed=2.0, defaultLengthUnits="mm", toolFrameOffset=[0.0,0.0,0.0]):
        self.motionMode = 1
        self.lengthUnits = defaultLengthUnits
        self.toolPose = DataTypes.ToolPose()
        self.newToolPose = DataTypes.ToolPose()
        self.circCenter = [0,0,0]
        if defaultLengthUnits=="in":
            self.toolFrameOffset = np.array(toolFrameOffset)*25.4
            self.rapidFeed = rapidFeed*25.4
            self.feedRate = feedRate*25.4
        else:
            self.toolFrameOffset = np.array(toolFrameOffset)
            self.rapidFeed = rapidFeed 
            self.feedRate = feedRate


    def parseFile(self, file):
        #import the gcode
        try:
            with open(file, 'r') as f:
                gcode = f.read()
        except:
            print("failed to open file\n\r")
            return 1

        self.parsedGcode = self.parseAllLines(gcode)
        return 0


    def evaluateGcode(self):
        wayPoints = []
        for block in self.parsedGcode:
            if self.evaluateGcodeBlock(block):
                # botPose = self.calcBotPose(self.newToolPose, self.toolOffset)
                pos=np.array([self.newToolPose.x, self.newToolPose.y, self.newToolPose.z])
                if self.lengthUnits == "in":
                    pos = pos*25.4
                pos=pos+self.toolFrameOffset
                toolVec=np.array([self.newToolPose.i, self.newToolPose.j, self.newToolPose.k])
                point = DataTypes.WayPoint(pos=pos, toolVec=toolVec)
                if self.motionMode == 0:
                    point.circijk=np.array([0.0,0.0,0.0])
                    point.vel=self.rapidFeed 
                    point.rotAxis=np.array([0.0,0.0,0.0])
                if self.motionMode == 1:
                    point.circijk=np.array([0,0,0])
                    point.vel=self.feedRate if self.lengthUnits == "mm" else self.feedRate*25.4/60.0
                    point.rotAxis=np.array([0.0,0.0,0.0])
                if self.motionMode == 2:
                    point.circijk=np.array(self.circCenter)
                    point.vel=self.feedRate if self.lengthUnits == "mm" else self.feedRate*25.4/60.0
                    point.rotAxis=np.array([0.0,0.0,-1.0])
                if self.motionMode == 3:
                    point.circijk=np.array(self.circCenter)
                    point.vel=self.feedRate if self.lengthUnits == "mm" else self.feedRate*25.4/60.0
                    point.rotAxis=np.array([0.0,0.0,1.0])

                

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
        # line = (''.join(line.split())).replace(";", "").upper()
        line = (''.join(line.split(';')[0].split())).upper()
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
            elif block[i][0] == 'F':
                self.feedRate = block[i][1]
            elif block[i][0] == 'X':
                newPose = True
                self.newToolPose.x = block[i][1]
                # self.newToolPose.y = -block[i][1]
            elif block[i][0] == 'Y':
                newPose = True
                self.newToolPose.y = block[i][1]
                # self.newToolPose.z = block[i][1]
            elif block[i][0] == 'Z':
                newPose = True
                self.newToolPose.z = block[i][1]
                # self.newToolPose.x = -block[i][1]
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
            elif block[i] == ['G', 20]:
                self.lengthUnits = "in"
            elif block[i] == ['G', 21]:
                self.lengthUnits = "mm"
            elif block[i][0] == 'N': #line numbers
                pass
            ###TODO: G17, 18, 19, ?(G40, G49)?, G90, G91
            else:
                print("Gcode Parser Error: " + str(block[i]) + " not found in block " + i)
        
        return newPose


#interp = GcodeParser_custom("G01 XX1.1 Y1. Z1.;\n\n(asdfasd_)\n(asdf\nX1Y1.").parseAllLines()
# print(GcodeParser_custom.parseLine("G01"))

