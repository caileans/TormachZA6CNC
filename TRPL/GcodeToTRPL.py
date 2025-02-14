from GcodeParser_custom import GcodeParser_custom as GcodeParser
from math import pi, sin, cos, atan2, acos, asin, sqrt
import numpy as np
import os
from general_robotics_toolbox import rpy2R
# import rospy

# data type for tool pose representation as in Gcode: xyzijk
class ToolPose:
    def __init__(self, x=0, y=0, z=0, i=0, j=0, k=0):
        self.x = x
        self.y = y
        self.z = z
        self.i = i
        self.j = j
        self.k = k

# data type for bot pose as used in TRPL: xyzabc
class BotPose:
    def __init__(self, x=0, y=0, z=0, a=0, b=0, c=0):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c

# class to call appropriate TRPL ros services give gcode
class GcodeToTRPL:
    def __init__(self, feedRate=0, rapidFeed=0, defaultLengthUnits="mm", defaultAngleUnits="deg", defaultTimeUnits="s", toolOffset=[0,0,0]):
        self.rapidFeed = rapidFeed
        self.feedRate = feedRate
        self.motionMode = 1
        self.lengthUnits = defaultLengthUnits
        self.angleUnits = defaultAngleUnits
        self.timeUnits = defaultTimeUnits
        self.toolPose = ToolPose()
        self.newToolPose = ToolPose()
        self.circCenter = [0,0,0]
        self.botPose = BotPose()
        self.toolOffset = toolOffset


# Gcode parsing functions
    def runFile(self, file):
        #import the gcode
        with open(file + '.nc', 'r') as f:
            gcode = f.read()

        parsedGcode = GcodeParser(gcode).parseAllLines()

        self.constructTRPLFile(parsedGcode, file + ".py")

        self.runTRPLFile(file + ".py")


    def runBlock(self, block):
        print("WARNING: THIS FUNCTION HAS NO BUFFER. MULTIPLE CALLS CAN SKIP MOVEMENTS")
#        print(GcodeParser.parseLine(block))
        newPose = self.evaluateGcodeBlock(GcodeParser.parseLine(block)[0])
        
        if newPose:
            TRPLcommand = self.constructTRPLMoveCommand()
            self.sendMDICommand(TRPLcommand)
#            print(self.newToolPose)
            
            self.toolPose = self.newToolPose

    def evaluateGcodeBlock(self, block):
#        print(block)
        # self.toolPose = self.newToolPose
        self.toolPose.x=self.newToolPose.x
        self.toolPose.y=self.newToolPose.y
        self.toolPose.z=self.newToolPose.z
        self.toolPose.i=self.newToolPose.i
        self.toolPose.j=self.newToolPose.j
        self.toolPose.k=self.newToolPose.k
        # self.newToolPose=ToolPose()
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
        


    # def runLinearMotion(self, feed):
    #     print("executing linear motion")
    #     self.botPose = self.calcBotPose(self.newToolPose, [0,0,0])
    #     self.sendMDICommand(self.constructTRPLLine(self.botPose, feed))

    # def runCircularMotion(self, dir, feed):
    #     print("executing circular motion ASSUMES XY PLANE")
    #     self.circInterToolPose = 1 #dis anit' right
    #     self.circInterBotPose = self.calcBotPose(self.circInterToolPose)
    #     self.botPose = self.calcBotPose(self.toolPose)
    #     self.sendMDICommand(self.constructTRPLCirc(self.botPose, self.circInterBotPose, feed))
    
    



# Math Functions
    def calcBotPose(self,toolPose, toolOffset = [0.0,0.0,0.0]):
        """converts the 5dof tool pose into the 6 dof robot endpose for cartesian waypoint. 
        Note: this function assumes that the tool is mounted at 90 degrees to the J6 axis
        Note: zeroing between the tool and the part should be done prior to calling this function

        Inputs: toolPose- a ToolPose instance that has an x,y,z position and an i,j,k orrientation.
                toolOffset- a 3d array that describes the linear offset frm the tool to J6
                q0- a 3d array that describes how you want to optimize the J6 axis
        Output: a BotPose object describing the end effector pose of the tormach
        """
        # toolPose.i=0
        # toolPose.j=0
        # toolPose.k=1

        # calculate dot product of tool offset and orrientation vectors
        # dot=toolPose.i*toolOffset[0]+toolPose.j*toolOffset[1]+toolPose.k*toolOffset[2]
        
        # # calculate the position of the end effector
        # position=[toolPose.x-dot*toolPose.i,toolPose.y-dot*toolPose.j,toolPose.z-dot*toolPose.k]

        # mag=sqrt(position[0]*position[0]+position[1]*position[1]+position[2]*position[2])

        # q0=[0, -1*position[1], -1*position[2]]
        q0=[1,0,0]

        # # calculate the dot product of q0 and the toolPose
        magpose2=toolPose.i*toolPose.i+toolPose.j*toolPose.j+toolPose.k*toolPose.k
        magpose2=1

        dot =( toolPose.i*q0[0]+toolPose.j*q0[1]+toolPose.k*q0[2])/magpose2

        
        # # calculate the J6 orrientation i, j, k
        q=np.array([q0[0]-dot*toolPose.i,q0[1]-dot*toolPose.j,q0[2]-dot*toolPose.k])
        if q.all(0):
            q=np.array([0,0,-1])*copysign(1,toolPose.i)

#         # Let the J6 vector be in the plane orthoganal to the tool direction toolDirection
#         toolDirection=np.array([toolPose.i,toolPose.j,toolPose.k])
#         toolDirection=toolDirection/np.linalg.norm(toolDirection)

#         # Let the toolOffset be only in the x/z plane with z being in the j6 dirrection such that j6 must go througha point p
#         p=np.array([toolPose.x,toolPose.y,toolPose.z])+toolOffset[0]*toolDirection

#         #Let the J6 vector be in the z-r plane passing through p with a norm n
#         n=np.array([p[1],-1*p[0],0])
#         n=n/np.linalg.norm(n)
# #        print(n)
# #        print(toolDirection)
#         #Let the J6 vector be orthoganal to the toolDirection pose such that
#         J6=np.cross(toolDirection, n)
#         # print(J6)
#         #if the n and toolDirection are in the same direction, default to an orrientation in the z axis
#         if J6[0]==0 and J6[1]==0 and J6[2]==0:
#             J6=np.array([0,0,1])*np.copysign(1,p[0])
#             J6=J6-np.dot(J6,toolDirection)*toolDirection
#             print("c1")
#         if J6[0]==0 and J6[1]==0 and J6[2]==0:
#             J6=np.array([1,0,0])*np.copysign(1,p[0])
#             J6=J6-np.dot(J6,toolDirection)*toolDirection
#             print("c2")

#         # set q=J6
#         q=J6
        # print("J6")
        # print(q)
#        print('toolDirection')
#        print(toolDirection)
        # print(q0)
        # print([toolPose.i,toolPose.j,toolPose.k])
        # calculate A, B, C by calling the calcABC function
        # print(toolOffset)
        # print(np.array([toolOffset[0],toolOffset[1],toolOffset[2]]).transpose())
        abc=self.calcABC(q, toolPose)
        R=rpy2R(abc)
        # print(R)
        newtooloffset=np.matmul(R,np.array(toolOffset).transpose())
        # print(newtooloffset)
        position=[toolPose.x-newtooloffset[0],toolPose.y-newtooloffset[1],toolPose.z-newtooloffset[2]]
        # print(position)
        return BotPose(position[0],position[1],position[2], abc[0],abc[1],abc[2])


    def calcABC(self,q,toolPose):
        """determine the angles A, B, C from the 3 dimensional cartesion orientation

        Input: q- a 3d array of values corresponding to i, j, k direction of joint 6 (pointing from joint 5 to joint 6)
        Output: ABC- a 3d array of values coresponding to the A, B, C angles in degrees
        """
        # magpose=sqrt(toolPose.i*toolPose.i+toolPose.j*toolPose.j+toolPose.k*toolPose.k)

        # normalize the vector q
        # qprime = [q[0]/sqrt(q[0]*q[0]+q[1]*q[1]+q[2]*q[2]),q[1]/sqrt(q[0]*q[0]+q[1]*q[1]+q[2]*q[2]),q[2]/sqrt(q[0]*q[0]+q[1]*q[1]+q[2]*q[2])]
        # qprime2=[qprime[1]*toolPose.k-qprime[2]*toolPose.j,qprime[2]*toolPose.i-qprime[0]*toolPose.k,qprime[0]*toolPose.j-qprime[1]*toolPose.i]
        # # print(qprime)
        # # print(qprime2)
        # # calculate the angle A
        # A=atan2(-qprime[1],-qprime[2])

        # calculate the angle . down from xy plane
        # B=atan2((qprime[2]-cos(A)),qprime[0])
        B=atan2(-toolPose.k,sqrt(toolPose.i*toolPose.i+toolPose.j*toolPose.j))

        # calculate the angle C
        # C=atan2(-qprime[1],-(qprime[0]-cos(B)))
        C=atan2(toolPose.j,toolPose.i)


        q0 = np.array([0.0, 0.0, 0.0])
        q0[2] = cos(B)
        q0ij = sin(B)
        q0[0] = q0ij*cos(C)
        q0[1] = q0ij*sin(C)
        cross = np.cross(q, q0)
        # print((int((q.dot(q0)/(np.sqrt(q.dot(q))*np.sqrt(q0.dot(q0))))*10E12))/10.0E12)
#        A = np.copysign(acos(((int)(q.dot(q0)/(np.sqrt(q.dot(q))*np.sqrt(q0.dot(q0))))*10E12)/10.0E12), -cross.dot(np.array([toolPose.i, toolPose.j, toolPose.k])))
        A =pi- np.copysign(asin(np.sqrt(cross.dot(cross))/(np.sqrt(q.dot(q))*np.sqrt(q0.dot(q0)))), -cross.dot(np.array([toolPose.i, toolPose.j, toolPose.k])))
        # asin(np.sqrt(cross.dot(cross))/(np.sqrt(q.dot(q))*np.sqrt(q0.dot(q0))))

        # A=atan2(-qprime2[1],qprime2[2])

        # # calculate the angle B
        # B=atan2(qprime2[0],(qprime2[2]+cos(A)))

        # # calculate the angle C
        # C=atan2(-(qprime2[1]+sin(A)),-(qprime2[0]-cos(B)))
        # print(self.R2rpy([[qprime[0]*toolPose.i/magpose,qprime[1]*toolPose.i/magpose,qprime[2]*toolPose.i/magpose],[qprime[0]*toolPose.j/magpose,qprime[1]*toolPose.j/magpose,qprime[2]*toolPose.j/magpose],[qprime[0]*toolPose.k/magpose,qprime[1]*toolPose.k/magpose,qprime[2]*toolPose.k/magpose]]))
        
        # print(A*180.0/pi)
        # print(B*180.0/pi)
        # print(C*180.0/pi)
        A=-175*pi/180.0
        B=-6.5*pi/180.0
        C=-40*pi/180.0
        return [A*180.0/pi,B*180.0/pi,C*180.0/pi]


# TRLP interface functions
    def constructTRPLMoveCommand(self):
        self.botPose = self.calcBotPose(self.newToolPose, self.toolOffset)
        # print(self.toolPose)
        if self.motionMode == 0:
            TRPLCommand = self.constructTRPLLine(self.botPose, self.rapidFeed)
        if self.motionMode == 1:
            TRPLCommand = self.constructTRPLLine(self.botPose, self.feedRate)
        if self.motionMode == 2:
            circInterToolPose = self.getMidPoint(self.toolPose, self.newToolPose, np.array([self.circCenter[0],self.circCenter[1],self.circCenter[2]]), a= np.array([0,0,-1]))
            circInterBotPose = self.calcBotPose(circInterToolPose)
            TRPLCommand = self.constructTRPLCirc(self.botPose, circInterBotPose, self.feedRate)
        if self.motionMode == 3:
            circInterToolPose = self.getMidPoint(self.toolPose, self.newToolPose, np.array([self.circCenter[0],self.circCenter[1],self.circCenter[2]]), a= np.array([0,0,1]))
            circInterBotPose = self.calcBotPose(circInterToolPose)
            TRPLCommand = self.constructTRPLCirc(self.botPose, circInterBotPose, self.feedRate)


        return TRPLCommand

    def constructTRPLLine(self, pose, vel):
        #form the TRPL command
        TRPLCommand = "movel(p["+str(pose.x) +","+str(pose.y)+","+str(pose.z)+","+str(pose.a)+","+str(pose.b)+","+str(pose.c)+"], velocity="+str(vel)+")"

        # print(TRPLCommand)
        # _ = self.callRobotCommand(TRPLCommand)
        # self.sendMDICommand(TRPLCommand)
        return TRPLCommand

    def constructTRPLCirc(self, pose, interPose, vel):
        #form the TRPL command
        TRPLCommand = "movec(p["+str(interPose.x)+","+str(interPose.y)+","+str(interPose.z)+","+str(interPose.a)+","+str(interPose.b)+","+str(interPose.c)+"],p["+str(pose.x)+","+str(pose.y)+","+str(pose.z)+","+str(pose.a)+","+str(pose.b)+","+str(pose.c)+"])"

        # print(TRPLCommand)
        # _ = self.callRobotCommand(TRPLCommand)
        # self.sendMDICommand(TRPLCommand)
        return TRPLCommand

    def sendMDICommand(self, command):
        """send a trpl command to the tormach
        
        Input: a string of the command that is to be sent
        output: none
        """
        rosCommand = "rosservice call /robot_command/execute_mdi '" + command + "'"
        # system(rosCommand)

    def constructTRPLFile(self, code, fileName):
        f = open(fileName, "w")
        #USER FRAME IS SET HERE
        f.write("from robot_command.rpl import *\nset_units('"+str(self.lengthUnits)+"','"+str(self.angleUnits)+"','"+str(self.timeUnits)+"')\n#set_user_frame('table', p[500, 0, 500, 0, 0, 0])\nchange_user_frame('table')\ndef main():\n    set_path_blending(True, 0.0)\n")
        # f.write("from robot_command.rpl import *\nset_units('"+str(self.lengthUnits)+"','deg')\n#set_user_frame('table', p[500, 0, 500, 0, 0, 0])\n#change_user_frame('table')\ndef main():\n#    set_path_blending(True, 0.0)\n")
        for block in code:
            newPose = self.evaluateGcodeBlock(block)
            if newPose:
                f.write("    "+str(self.constructTRPLMoveCommand())+"\n")
        f.write("    sync()\n    exit()\n")

    def runTRPLFile(self, file):
        rosCommand = "rosservice call /robot_command/load_program " + os.getcwd()+"/" + file + " && rosservice call robot_command/run_command 2"
        os.system(rosCommand)

    def getMidPoint(self, toolPose, newToolPose, roc, a= np.array([0,0,1])):
        """determine midpoint for the movement of the end effector for the movec function moves counter clockwise around a (to go clockwise use -a)

        Inputs:
            toolPose-       the initial pose of the end effector (toolPose)
            newToolPose-    the final pose of the end effector (toolPose)
            rfc-            the relative position from the final pose to the center point of the circle (np.array)
            a-              the axis of rotation around the edge of the circle (np.array)
        Output:
            pMidpoint       the point the end effector reaches at theta/2 around the circle
        """
        # tool poses
        pFinal=np.array([newToolPose.x,newToolPose.y,newToolPose.z])
        pInitial=np.array([toolPose.x,toolPose.y,toolPose.z])
        # center of the circle of movement
        pCenter=pInitial+roc
        # normalize the rotation axis
        ahat= a/sqrt(a.dot(a))
        # relative position from center to inital pose
        rco=-roc
        rfc=pFinal-pCenter

        # in rotation plane rco
        r2dco=rco-rco.dot(ahat)*ahat
        # in rotation plane rcf
        r2dcf=rfc.dot(ahat)*ahat-rfc
        # print("rfc")
        # angle between rfc,rco
        # print(pInitial)
        # print(pCenter)
        # print(r2dco)
        thetaA= acos(r2dco.dot(r2dcf)/(sqrt(r2dco.dot(r2dco))*sqrt(r2dcf.dot(r2dcf))))
        thetaA2=thetaA/2

        # normalized in rotation plane rco (x axis)
        r2dx=r2dco/sqrt(r2dco.dot(r2dco))
        # normalized in rotation plane y axis
        r2dy=np.cross(ahat,r2dx)
        # radius of rotation
        r=sqrt(r2dco.dot(r2dco))
        # calculate and return point at r,theta/2, z/2 of rotation
        xyz= pCenter +r*r2dx*cos(thetaA2)+r*r2dy*sin(thetaA2)+ahat.dot(pFinal-pInitial)*ahat/2
        print(r2dx)
        print(r2dy)
        print(thetaA2)
        output=ToolPose()
        output.x=xyz[0]
        output.y=xyz[1]
        output.z=xyz[2]
        output.i=toolPose.i
        output.j=toolPose.j
        output.k=toolPose.k
        # newToolPose.i
        return output




#testing
parser = GcodeToTRPL(feedRate=12, rapidFeed=12, defaultLengthUnits="in", defaultAngleUnits="deg", defaultTimeUnits="min", toolOffset=[0,0,0])


#parser.runBlock("G01 x600.0 Y1 z600 I1.0 J0 K-1")
#parser.runBlock("G01 x500.0 Y1 z600")
# parser.runBlock("G01 x700.0 Y-50.0 z600 I1.0 J0 K-1")
# parser.runBlock("G01 x700.0 Y150.0 z600 I1.0 J0 K-1")
# parser.runBlock("G01 x900.0 Y150.0 z600 I1.0 J0 K-1")
# parser.runBlock("G01 x900.0 Y-50.0 z600 I1.0 J0 K-1")
# parser.runBlock("G01 x700.0 Y-50.0 z600 I1.0 J0 K-1")

# parser.runFile("circleTest")
parser.runFile("WAAM_wall_2025")
# parser.runFile("testGcode")

#tpose = ToolPose(1, 1, 1, 0, 0, 1)
#print(parser.calcABC(np.array([1, 0, 0]), tpose))
#print(parser.calcBotPose(tpose, [100.0,0.0,0.0]))
#tpose = ToolPose(1, 1, 1, 1, 0, 1)
#print(parser.calcABC(np.array([1, 0, -1]), tpose))
#print(parser.calcBotPose(tpose, [100.0,0.0,0.0]))
#tpose = ToolPose(1, 1, 1, -1, 0, 1)
#print(parser.calcABC(np.array([1, 0, 1]), tpose))
#print(parser.calcBotPose(tpose, [1.0,0.0,0.0]))
#tpose = ToolPose(1, 1, 1, 0, 1, 1)
#print(parser.calcABC(np.array([1, 0, 0]), tpose))
#print(parser.calcBotPose(tpose, [100.0,0.0,0.0]))
#tpose = ToolPose(1, 1, 1, 0, -1, 1)
#print(parser.calcABC(np.array([1, 0, 0]), tpose))
#print(parser.calcBotPose(tpose, [100.0,0.0,0.0]))

    
