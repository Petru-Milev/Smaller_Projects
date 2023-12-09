import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
from matplotlib.patches import Circle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d
import os

#All values are in SI units

class Physical_System: 
    def __init__(self, name, dt, t, gamma, particle_radius, pore_radius, z,  pore_position, D, electric_field = None, applied_potential = None):
        self.name = name
        self.dt = dt
        self.t = t
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
        
def solve_langevin(x, z, E, gamma, D, dt, e = 1.6021766e-19):
    #x_new = x + e*z*E*dt/gamma + np.sqrt(2*D*dt)*np.random.normal(0, np.sqrt(2*D*dt))
    x_new = x + np.sqrt(2*D*dt)*np.random.normal(0, 1)
    return x_new

def run_simulation(object, pos):
    current_directory = os.getcwd()
    path_log = os.path.join(current_directory, object.name + ".txt")
    with open(path_log, "w") as file:
        pass
    x_sum = 0
    y_sum = 0
    z_sum = 0
    xx_sum = 0
    yy_sum = 0
    zz_sum = 0
    t = 0 
    t += object.dt
    print(pos)
    x, y, z = pos[0], pos[1], pos[2]
    print(x, y, z)
    E_x, E_y, E_z = object.electric_field[0], object.electric_field[1], object.electric_field[2]
    x_array = []
    y_array = []
    z_array = []

    #while (z > object.particle_radius) or (np.sqrt(x**2 + y**2) > object.pore_radius - 2*object.particle_radius):
    while True:
        x_sum += x*1e+9
        y_sum += y*1e+9
        z_sum += z*1e+9
        xx_sum += (x*1e+9)**2
        yy_sum += (y*1e+9)**2
        zz_sum += (z*1e+9)**2
        
        t += object.dt
        #def solve_langevin(x, z, E, gamma, D, dt, e = 1.6021766e-19)
        x = solve_langevin(x, object.z, E_x, object.gamma, object.D, object.dt, object.e)
        y = solve_langevin(y, object.z, E_y, object.gamma, object.D, object.dt, object.e)
        z = solve_langevin(z, object.z, E_z, object.gamma, object.D, object.dt, object.e)
        
        """        if z < object.particle_radius and np.sqrt(x**2 + y**2) < object.pore_radius - 2*object.particle_radius:
            break
        elif z < 0:
            z = -z"""
        print(f"x={x*1e+9}nm, y={y*1e+9}nm, z={z*1e+9}nm")
        #x_array.append(x)
        #y_array.append(y)
        #z_array.append(z)
        if t >= object.t:
            n = int(np.round(t/object.dt, 0))
            print("--------------------------------")
            print(n)
            x_sum = + x*1e+9
            y_sum = + y*1e+9
            z_sum = + z*1e+9
            xx_sum = + (x*1e+9)**2
            yy_sum = + (y*1e+9)**2
            zz_sum = + (z*1e+9)**2
            x_average = x_sum/n
            y_average = y_sum/n
            z_average = z_sum/n
            xx_average = xx_sum/n
            yy_average = yy_sum/n
            zz_average = zz_sum/n
            with open(path_log, "a") as file:
                file.write(f"Average values of possition:\n{x_average*1e-9, y_average*1e-9, z_average*1e-9}\n")
                file.write(f"Average square values of possition:\n{xx_average*(1e-9)**2, yy_average*(1e-9)**2, zz_average*(1e-9)**2}\n")
                file.write(f"sqrt(2Dt)*3.4 is {np.sqrt(2*object.D*t)*3.4}\n")
                file.write(f"2Dt is {2*object.D*t}\n\n")
                #print all the characteristis of the object
                file.write(f"Properties of the object:\n")
                file.write(f"Name is {object.name}\n")
                file.write(f"dt is {object.dt}\n")
                file.write(f"t is {t}\n")
                file.write(f"gamma is {object.gamma}\n")
                file.write(f"particle_radius is {object.particle_radius}\n")
                file.write(f"pore_radius is {object.pore_radius}\n")
                file.write(f"z is {object.z}\n")
                file.write(f"D is {object.D}\n")
            print(f"Average position is (in nm) {x_average*1e-9, y_average*1e-9, z_average*1e-9}")
            print(f"Average square position is {xx_average*(1e-9)**2, yy_average*(1e-9)**2, zz_average*(1e-9)**2}")
            print(f"sqrt(2Dt)*3.4 is {np.sqrt(2*object.D*t)*3.4}")
            print(f"2Dt is {2*object.D*t}")
            print("--------------------------------")
            break
    
    print(f"t is {t}")
    print(f"Final position is {x*1e+9, y*1e+9, z*1e+9}")
    #print(f"Pore Radius is {object.pore_radius*1e+9}nm")
    #print(f"Particle Radius is {object.particle_radius*1e+9}nm")
    #print(f"Effective Radius of Pore is {(object.pore_radius - 2*object.particle_radius)*1e+9}nm")

    """fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_array, y_array, z_array, c = 'r', marker = 'o', markersize = 1)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    p = Circle((0, 0), object.pore_radius, color='b', alpha=0.2)
    p1 = Circle((0, 0), object.pore_radius - 2*object.particle_radius, color='r', alpha=0.2)
    ax.add_patch(p)
    ax.add_patch(p1)
    art3d.pathpatch_2d_to_3d(p, z=0, zdir="z")
    art3d.pathpatch_2d_to_3d(p1, z=0, zdir="z")

    plt.show()"""
    return  
 
#def __init__(self, dt, gamma, particle_radius, pore_radius, z,  pore_position, D, electric_field = None, applied_potential = None)

"""
Diffusion coefficient of proton in water is 
9.31e-9 m^2/s
gamma = 6*pi*eta*a
gamma = 6*pi*1*10^(-3)Pa*s * 1*10^(-9)m = 1.88*10^(-11) kg/s
D = 2kB*T/gamma
D = 2*1.38*10^(-23)*300/1.88*10^(-11) = 2.06*10^(-9) m^2/s
"""
system_one = Physical_System(name = "System_one_e-9", dt = 1e-15, t = 1e-11, gamma = 1.88e-11, particle_radius = 1*1e-9, pore_radius = 5*1e-9, z = 1.0, pore_position = 0.0, D = 4.40*1e-9, electric_field = np.array([0.0, 0.0, 0.0])) #-1.4 * 1e-10
system_two = Physical_System(name = "System_two_e-8", dt = 1e-15, t = 1e-8, gamma = 1.88e-11, particle_radius = 1*1e-9, pore_radius = 5*1e-9, z = 1.0, pore_position = 0.0, D = 4.40*1e-9, electric_field = np.array([0.0, 0.0, 0.0])) #-1.4 * 1e-10
system_three = Physical_System(name = "System_one_e-7", dt = 1e-15, t = 1e-7, gamma = 1.88e-11, particle_radius = 1*1e-9, pore_radius = 5*1e-9, z = 1.0, pore_position = 0.0, D = 4.40*1e-9, electric_field = np.array([0.0, 0.0, 0.0])) #-1.4 * 1e-10
pos = np.array([0.0, 0, 0]) #Initial coordinates of the particle
run_simulation(system_one, pos)
run_simulation(system_two, pos)
run_simulation(system_three, pos)
