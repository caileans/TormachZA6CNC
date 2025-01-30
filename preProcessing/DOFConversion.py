import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import DataTypes


def AddFixed6DOF(trajectory):
    for point in trajectory:
        point.rot=np.array([0.0, np.pi, 0.0])

    return trajectory
