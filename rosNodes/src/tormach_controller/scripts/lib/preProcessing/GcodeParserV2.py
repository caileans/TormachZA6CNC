import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import numpy as np
# from DataTypes import ToolPose, WayPoint
import DataTypes

# x = ToolPose()


class GcodeParserV2:
    '''
    A class which can be used to pass a single block of Gcode or a Gcode file. General use has three steps:
    1) define an instance of the class, pass in default parameters, feedrates, etc
    2) call a parse____ function. ***parseFile() is the only one of these function to have been fully tested***
    3) call the evaluateGcode function, this will return an array of WayPoint dataTypes
    '''
    def __init__(self, feedRate=1.0, rapidFeed=2.0, defaultLengthUnits="mm", toolFrameOffset=[0.0,0.0,0.0]):
        '''initialization function. see setParameters for inputs'''
        self.setParameters(feedRate, rapidFeed, defaultLengthUnits, toolFrameOffset)

    
    def setParameters(self, feedRate=1.0, rapidFeed=2.0, defaultLengthUnits="mm", toolFrameOffset=[0.0,0.0,0.0]):
        '''
        used by the __init__ function to initilize default parameters. can also be used to reinitilize these parameters

        Inputs:
            feedRate: the default linear/circular motion feed rate, in defaultLengthUnits units
            rapidFeed: the default rapid feed rate, in defaultLengthUnits units
            defaultLengthUnits: units to expect Gcode in, as well as the feed rate inputs. can be "mm" or "in"
            toolFrameOffset: X, Y, Z offsets of the Gcode frame w.r.t. the machine coordinate system
        '''
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
        '''
        parses a Gcode file. Parsing is just reading the file into an internal array. does not output waypoints (see evaulate____ functions)

        Inputs:
            file: the file name/path to read the Gcode from

        Outputs:
            returns 0 if sucessful, 1 if the file failed to open
        '''
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
        '''
        evaluates whatever is currently stored as the Gcode in the class instance. returns an array of WayPoints

        Outputs:
            wayPoints: an array of WayPoint data types, one for each movement Gcode command
        '''
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
        '''
        parses a string (can be multiple blocks) of Gcode into an array of Gcode commands. For internal use only

        Inputs:
            gcode: a string of Gcode

        Outputs:
            parsedLines: an array (multiple blocks) of Gcode commands ready to be run through the evaluateGcodeBlock function
        '''
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
        '''
        translates a line/ block of text gcode into an array of commands

        Inputs:
            line: a string (single line) of Gcode

        Outputs:
            commands: an array of the commands found in the string. array is of the format: [[letter, number], [letter, number],...etc]
            unrecognizedCommands: an array of text not regognized as Gcode or a comment
        '''
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
        '''
        evaluates a parsed Gcode block array. this includes setting parameters and updating new movement positions

        Inputs:
            block: the array of a parsed Gcode block
        
        Outputs:
            newPose: true if the Gcode block contained a movement command, false otherwise
        '''
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

