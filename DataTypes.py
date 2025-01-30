from dataclasses import dataclass, field
from enum import Enum
import numpy as np

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
    x: float = 0
    y: float = 0
    z: float = 0
    i: float = 0
    j: float = 0
    k: float = 0

# class MotionType(Enum):
#     line = 1
#     ccw = 2
#     cw = 3

@dataclass
class WayPoint:
    # pos: Position = field(default_factory=Position)
    # toolVec: IJKVector = field(default_factory=IJKVector)
    # circ: IJKVector = field(default_factory=IJKVector)
    pos: np.ndarray = field(default_factory=lambda: np.array([0,0,0]))
    toolVec: np.ndarray = field(default_factory=lambda: np.array([0,0,0]))
    circijk: np.ndarray = field(default_factory=lambda: np.array([0,0,0]))
    vel: float = 0
    rotAxis: np.ndarray = field(default_factory=lambda: np.array([0,0,0]))

@dataclass
class TrajPoint:
    # pos: Position = field(default_factory=Position)
    # toolVec: IJKVector = field(default_factory=IJKVector)
    # rot: EulerAngles = field(default_factory=EulerAngles)
    # vel: float = 0
    pos: np.ndarray = field(default_factory=lambda: np.array([0,0,0]))
    toolVec: np.ndarray = field(default_factory=lambda: np.array([0,0,0]))
    rot: np.ndarray = field(default_factory=lambda: np.array([0,0,0]))