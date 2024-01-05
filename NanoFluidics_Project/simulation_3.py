import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
from matplotlib.patches import Circle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import Axes3D
import os

from langevin_equation import *

system_3_0 = Physical_System(name = "System_3_0_nm_dist", dt = 1e-15, t = 1*1e-8, gamma = 4.02e-12, particle_radius = 1*1e-9, pore_radius = 3*1e-9, z = 1.0, pore_position = [0, 0, 0], D = 2*1e-9, pore_charge = -5) #-1.4 * 1e-10
pos = np.array([0, 0, 6*1e-9]) #Initial coordinates of the particle
for i in range(2000):
    run_simulation(system_3_0, pos)
