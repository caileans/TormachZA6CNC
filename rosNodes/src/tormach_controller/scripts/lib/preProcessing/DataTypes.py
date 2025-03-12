import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

'''define data classes to pass tool path information between components'''


# @dataclass
# class IJKVector:
#     i: float = 0
#     j: float = 0
#     k: float = 0

#     def ijk(self):
#         return np.array([self.i, self.j, self.k])

# @dataclass
# class EulerAngles:
#     a: float = 0
#     b: float = 0
#     c: float = 0

#     def abc(self):
#         return np.array([self.a, self.b, self.c])


# @dataclass
# class Position:
#     x: float = 0
#     y: float = 0
#     z: float = 0

#     def xyz(self):
#         return np.array([self.x, self.y, self.z])
    

# @dataclass
# class DOF5Pose:
#     pos: Position = field(default_factory=Position)
#     toolVec: IJKVector = field(default_factory=IJKVector)

# @dataclass
# class DOF6Pose:
#     pos: Position = field(default_factory=Position)
#     rot: EulerAngles = field(default_factory=EulerAngles)

@dataclass
class ToolPose:
    '''stores the x, y, z position of a tool as well as the toolvector i, j, k components. ijk represent a vector (not necessarily a unit vector) from the tool tip pointing to the tool shank'''
    x: float = 0
    y: float = 0
    z: float = 0
    i: float = 0
    j: float = 0
    k: float = 1

# class MotionType(Enum):
#     line = 1
#     ccw = 2
#     cw = 3

@dataclass
class WayPoint:
    '''stores a Gcode waypoint. Used to store Gcode movements'''
    # pos: Position = field(default_factory=Position)
    # toolVec: IJKVector = field(default_factory=IJKVector)
    # circ: IJKVector = field(default_factory=IJKVector)
    pos: np.ndarray = field(default_factory=lambda: np.array([0.0,0.0,0.0]))
    toolVec: np.ndarray = field(default_factory=lambda: np.array([0.0,0.0,0.0]))
    circijk: np.ndarray = field(default_factory=lambda: np.array([0.0,0.0,0.0]))
    vel: float = 0
    rotAxis: np.ndarray = field(default_factory=lambda: np.array([0.0,0.0,0.0]))

@dataclass
class TrajPoint:
    '''stores a trajectory point. this assumes constant timing information, so no velocity information is stored. also assumes discretized linear motion, so circular motion can not be represented.'''
    # pos: Position = field(default_factory=Position)
    # toolVec: IJKVector = field(default_factory=IJKVector)
    # rot: EulerAngles = field(default_factory=EulerAngles)
    # vel: float = 0
    pos: np.ndarray = field(default_factory=lambda: np.array([0.0,0.0,0.0]))
    toolVec: np.ndarray = field(default_factory=lambda: np.array([0.0,0.0,0.0]))
    rot: np.ndarray = field(default_factory=lambda: np.array([0.0,0.0,0.0]))