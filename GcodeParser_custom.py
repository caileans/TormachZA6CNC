import re

class GcodeParser_custom:
    def __init__(self, gcode):
        self.gcode = gcode
        self.block = 0
        self.d = 0

    def parseAllLines(self):
        
        self.parsedLines = []
        for line in self.gcode.splitlines():
            self.parsedLine, self.errors = self.parseLine(line)
            if self.parsedLine:
                self.parsedLines.append(self.parsedLine)
            if self.errors:
                print("did not regonize "+str(self.errors)+" in '"+line+"'")

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


#interp = GcodeParser_custom("G01 XX1.1 Y1. Z1.;\n\n(asdfasd_)\n(asdf\nX1Y1.").parseAllLines()
# print(GcodeParser_custom.parseLine("G01"))

