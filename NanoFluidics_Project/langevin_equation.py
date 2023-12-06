import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
from matplotlib.patches import Circle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d

#Initial conditions
#All units will be in atomic units

class Physical_System: 
    def __init__(self, dt, gamma, particle_radius, pore_radius, z,  pore_position, D, electric_field = None, applied_potential = None):
        self.dt = dt
        self.gamma = gamma
        self.electric_field = electric_field
        self.particle_radius = particle_radius
        self.pore_radius = pore_radius
        self.D = D
        self.e = 1 
        self.z = z 
        if electric_field.any():
            self.electric_field = electric_field
        #to not forget to add the case when we have electric field

pos = np.array([10.0, 0, 0]) #Initial coordinates of the particle 
R = np.linalg.norm(pos) #Distance to the center of coordinates
#applied_potential = np.array([1.4, 0, 0]) #Applied electric potential 
#electric_field = applied_potential/R #Electric field 
#particle_radius = 1 #Radius of the particle
#D = 1 #Diffusion coefficient

def solve_langevin(x, z, E, gamma, D, dt, e = 1.0):
    x_new = x + e*z*E*dt/gamma + np.sqrt(2*D*dt)*np.random.normal(0,1)
    return x_new

def run_simulation(object, pos):
    t = 0 
    t += object.dt
    print(pos)
    x, y, z = pos[0], pos[1], pos[2]
    print(x, y, z)
    E_x, E_y, E_z = object.electric_field[0], object.electric_field[1], object.electric_field[2]
    x_array = []
    y_array = []
    z_array = []
    while (z > object.particle_radius) or (np.sqrt(x**2 + y**2) > object.pore_radius - 2*object.particle_radius):
        t += object.dt
        print(x, y, z)
        x = solve_langevin(x, object.z, E_x, object.gamma, object.D, object.dt, object.e)
        y = solve_langevin(y, object.z, E_y, object.gamma, object.D, object.dt, object.e)
        z = solve_langevin(z, object.z, E_z, object.gamma, object.D, object.dt, object.e)
        if z < object.particle_radius and np.sqrt(x**2 + y**2) < object.pore_radius - 2*object.particle_radius:
            break
        elif z < 0:
            z = -z
        print(x, y, z)
        x_array.append(x)
        y_array.append(y)
        z_array.append(z)
        if t > 10000:
            break
    
    print(f"t is {t}")
    print(f"Final position is {x, y, z}")

    circe_radius = object.pore_radius
    circle_center = (0, 0, 0)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_array, y_array, z_array, c = 'r', marker = 'o', markersize = 1)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    p = Circle((0, 0), 10)
    ax.add_patch(p)
    art3d.pathpatch_2d_to_3d(p, z=0, zdir="z")

    plt.show()
    return 
 
#def __init__(self, dt, gamma, particle_radius, pore_radius, z,  pore_position, D, electric_field = None, applied_potential = None)

system_one = Physical_System(0.01, 1, 1, 100, 1, 0, 1, np.array([0, 0, -1.4]))
pos = np.array([0.0, 0, 10000.0]) #Initial coordinates of the particle
run_simulation(system_one, pos)
