import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
from matplotlib.patches import Circle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import Axes3D
import os

#All values are in SI units

class Physical_System: 
    def __init__(self, name, dt, t, gamma, particle_radius, pore_radius, pore_charge, z,  pore_position, D, applied_potential = None):
        self.name = name
        self.dt = dt
        self.t = t
        self.gamma = gamma
        self.particle_radius = particle_radius
        self.pore_radius = pore_radius
        self.pore_position = pore_position
        self.pore_charge = pore_charge * 1.6021766e-19
        self.D = D
        self.e = 1.6021766e-19
        self.z = z 
        #to not forget to add the case when we have electric field

def calculate_electric_field(pos_particle, pos_pore, charge_pore, relative_permittivity = 78.4):
    #return a np.array([E_x, E_y, E_z])
    #We have a charged pore which is generating an electric field
    #We have a charged particle which is moving in this electric field
    #https://en.wikipedia.org/wiki/Electric_field
    epsilon_0 = 8.8541878128e-12 #F/m
    epsilon = relative_permittivity*epsilon_0
    pos_particle = np.array(pos_particle)
    pos_pore = np.array(pos_pore)
    magnitude = np.linalg.norm(pos_particle - pos_pore)
    E = charge_pore * (pos_particle - pos_pore) / (4*np.pi*epsilon*magnitude**3) #in V/m
    return E

def solve_langevin(x, z, E, gamma, D, dt, e = 1.6021766e-19):
    x_new = x + e*z*E*dt/gamma + np.sqrt(2*D*dt)*np.random.normal(0, 1)
    #x_new = x + np.sqrt(2*D*dt)*np.random.normal(0, 1)
    return x_new

def make_plot(x_array, y_array, z_array, pore_radius, particle_radius):
    """    fig = plt.figure()
    ax = plt.axes(projection="3d")

    # Plot the wireframe
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 5 * np.outer(np.cos(u), np.sin(v))
    y = 5 * np.outer(np.sin(u), np.sin(v))
    z = 5 * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(x, y, z, color='b')
    # Plot the data set
    ax.plot(x_array[::10000], y_array[::10000], z_array[::10000])

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()
    """
    fig = plt.figure(figsize = (8, 8))
    ax = plt.axes(projection="3d")
    # Plot the wireframe
    u = np.linspace(0, 2*np.pi, 100)
    v = np.linspace(0, np.pi/2, 100)
    x = pore_radius *1e+9 * np.outer(np.cos(u), np.sin(v))
    y = pore_radius *1e+9 * np.outer(np.sin(u), np.sin(v))
    z = pore_radius *1e+9 * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(x, y, z, color='b')
    # Plot the data set
    ax.plot(x_array[::10000], y_array[::10000], z_array[::10000])
    ax.set_xlabel('X axis (nm)')
    ax.set_ylabel('Y axis (nm)')
    ax.set_zlabel('Z axis (nm)')
    ax.set_zlim(bottom = 0)

    plt.tight_layout()
    plt.show()
    return


def run_simulation(object, pos):
    current_directory = os.getcwd()
    path_log = os.path.join(current_directory, object.name + ".txt")
    with open(path_log, "a") as file:
        pass
    x_sum, y_sum, z_sum, xx_sum, yy_sum, zz_sum, t = 0, 0, 0, 0, 0, 0, 0
    t += object.dt
    x, y, z = pos[0], pos[1], pos[2]
    count = 0
    count_positions_registered = 1
    simulation_running = True
    x_array, y_array, z_array = [], [], []
    E_array = []
    #while (z > object.particle_radius) or (np.sqrt(x**2 + y**2) > object.pore_radius - 2*object.particle_radius):
    while simulation_running:
    #while True:
        n = int(np.round(object.t/object.dt, 0))
        record_possition = n//10
        if count % record_possition == 0:
            #This is recording the stats over time
            with open(path_log, "a") as file:
                file.write(f"Position number {count_positions_registered}, time {t}\n")
                file.write(f"Position is {x*1e+9:.4f}, {y*1e+9:.4f}, {z*1e+9:.4f} nm\n")
                file.write(f"Square of the position is {(x*1e+9)**2:.4f}, {(y*1e+9)**2:.4f}, {(z*1e+9)**2:.4f} nm^2\n")
                count_positions_registered += 1
        count += 1
        x_sum += x*1e+9
        y_sum += y*1e+9
        z_sum += z*1e+9
        xx_sum += (x*1e+9)**2
        yy_sum += (y*1e+9)**2
        zz_sum += (z*1e+9)**2
        t += object.dt
        #def calculate_electric_field(pos_particle, pos_pore, charge_pore, epsiolon_0, relative_permittivity = 78.4):
        E = calculate_electric_field(pos_particle = [x, y, z], pos_pore = object.pore_position, charge_pore = object.pore_charge)
        E_x, E_y, E_z = E[0], E[1], E[2]
        E_array.append(E_z)
        #def solve_langevin(x, z, E, gamma, D, dt, e = 1.6021766e-19)
        x = solve_langevin(x, object.z, E_x, object.gamma, object.D, object.dt, object.e)
        y = solve_langevin(y, object.z, E_y, object.gamma, object.D, object.dt, object.e)
        z = solve_langevin(z, object.z, E_z, object.gamma, object.D, object.dt, object.e)
        x_array.append(np.round(x*1e+9, 2))
        y_array.append(np.round(y*1e+9, 2))
        z_array.append(np.round(z*1e+9, 2))
        #Check if object is inside of the semisphere created by the radius of the pore
        if np.sqrt(x**2 + y**2 + z**2) < object.pore_radius:
            simulation_running = False
        if z < 0:
            z = -z
        if (t >= object.t):
            simulation_running = False
    n = int(np.round(t/object.dt, 0))
    print("--------------------------------")
    print(n)
    x_sum =+ x*1e+9
    y_sum =+ y*1e+9
    z_sum =+ z*1e+9
    xx_sum =+ (x*1e+9)**2
    yy_sum =+ (y*1e+9)**2
    zz_sum =+ (z*1e+9)**2
    x_average = x_sum/n
    y_average = y_sum/n
    z_average = z_sum/n
    xx_average = xx_sum/n
    yy_average = yy_sum/n
    zz_average = zz_sum/n
    with open(path_log, "a") as file:
        file.write(f"Average values of possition:\n{x_average*1e-9, y_average*1e-9, z_average*1e-9}\n")
        file.write(f"Average square values of possition:\n{xx_average*(1e-9)**2, yy_average*(1e-9)**2, zz_average*(1e-9)**2}\n")
        file.write(f"sqrt(2Dh)*3.4 is {np.sqrt(2*object.D*object.dt)*3.4}\n")
        file.write(f"2Dh is {2*object.D*object.dt}\n\n")
        file.write(f"Final time in seconds is {t}\n")
        file.write(f"Final position in nm is {x*1e+9, y*1e+9, z*1e+9}\n")
        file.write(f"Square of the final position in nm is {(x*1e+9)**2, (y*1e+9)**2, (z*1e+9)**2}\n")
        file.write("--------------------------------\n")
        #print all the characteristis of the object
        """file.write(f"Properties of the object:\n")
        file.write(f"Name is {object.name}\n")
        file.write(f"dt is {object.dt}\n")
        file.write(f"t is {t}\n")
        file.write(f"gamma is {object.gamma}\n")
        file.write(f"particle_radius is {object.particle_radius}\n")
        file.write(f"pore_radius is {object.pore_radius}\n")
        file.write(f"z is {object.z}\n")
        file.write(f"D is {object.D}\n")"""
    #print(f"Average position is (in nm) {x_average*1e-9, y_average*1e-9, z_average*1e-9}")
    #print(f"Average square position is {xx_average*(1e-9)**2, yy_average*(1e-9)**2, zz_average*(1e-9)**2}")
    #print(f"sqrt(2Dh)*3.4 is {np.sqrt(2*object.D*object.dt)*3.4}")
    #print(f"2Dh is {2*object.D*object.dt}")
    #print("--------------------------------")
    
    print(f"t is {t}")
    print()
    print(f"position -1 is {x_array[-1], y_array[-1], z_array[-1]}")
    print(f"Final position is {x*1e+9, y*1e+9, z*1e+9}")
    print(f"Pore charge is {object.pore_charge}")
    print(f"Particle charge is {object.z*object.e}")
    #print(f"Pore Radius is {object.pore_radius*1e+9}nm")
    #print(f"Particle Radius is {object.particle_radius*1e+9}nm")
    #print(f"Effective Radius of Pore is {(object.pore_radius - 2*object.particle_radius)*1e+9}nm")
    #print(x_array[::100000], y_array[::100000], z_array[::100000])
    #def make_plot(x_array, y_array, z_array, pore_radius, particle_radius):
    make_plot(x_array, y_array, z_array, object.pore_radius, object.particle_radius)

    return

"""    fig = plt.figure()
    ax = plt.axes(projection="3d")

    # Plot the wireframe
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 5 * np.outer(np.cos(u), np.sin(v))
    y = 5 * np.outer(np.sin(u), np.sin(v))
    z = 5 * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_wireframe(x, y, z, color='b')
    # Plot the data set
    ax.plot(x_array[::10000], y_array[::10000], z_array[::10000])

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()
"""
    #return  
 
#def __init__(self, dt, gamma, particle_radius, pore_radius, z,  pore_position, D, electric_field = None, applied_potential = None)

"""
Diffusion coefficient of proton in water is 
9.31e-9 m^2/s
gamma = 6*pi*eta*a
gamma = 6*pi*1*10^(-3)Pa*s * 1*10^(-9)m = 1.88*10^(-11) kg/s
D = 2kB*T/gamma
D = 2*1.38*10^(-23)*300/1.88*10^(-11) = 2.06*10^(-9) m^2/s
Gamma = 2kB*T/D
Gamma = 2*1.38*10^(-23)*300/2.06*10^(-9) = 4.02*10^(-12) kg/s
"""

#test = Physical_System(name = "Test_e-11", dt = 1e-15, t = 1e-8, gamma = 4.02e-12, particle_radius = 1*1e-9, pore_radius = 3*1e-9, z = 1.0, pore_position = [0, 0, 0], D = 2*1e-9, pore_charge = -1000) #-1.4 * 1e-10
#system_two = Physical_System(name = "System_two_e-8", dt = 1e-15, t = 1e-8, gamma = 4.02e-12, particle_radius = 1*1e-9, pore_radius = 5*1e-9, z = 1.0, pore_position = [0, 0, 0], D = 2*1e-9, pore_charge = 1) #-1.4 * 1e-10
#system_three = Physical_System(name = "System_three_e-7", dt = 1e-15, t = 1e-7, gamma = 4.02e-12, particle_radius = 1*1e-9, pore_radius = 5*1e-9, z = 1.0, pore_position = [0, 0, 0], D = 2*1e-9, pore_charge = 1) #-1.4 * 1e-10
#system_four = Physical_System(name = "System_four_e-6", dt = 1e-15, t = 1e-6, gamma = 4.02e-12, particle_radius = 1*1e-9, pore_radius = 5*1e-9, z = 1.0, pore_position = [0, 0, 0], D = 2*1e-9, pore_charge = 1) #-1.4 * 1e-10
#pos = np.array([0, 0, 6*1e-9]) #Initial coordinates of the particle

#run_simulation(system_one, pos)
#run_simulation(system_two, pos)
#run_simulation(system_three, pos)
#run_simulation(system_four, pos)
test = Physical_System(name = "Test_e-11", dt = 1e-15, t = 1e-8, gamma = 4.02e-12, particle_radius = 1*1e-9, pore_radius = 3*1e-9, z = 1.0, pore_position = [0, 0, 0], D = 2*1e-9, pore_charge = -10) #-1.4 * 1e-10
pos = np.array([0, 0, 5.5*1e-9]) #Initial coordinates of the particle
run_simulation(test, pos)
#for i in range(1,20000):
    #run_simulation(system_one, pos)
