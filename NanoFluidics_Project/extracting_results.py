import numpy as np 
import os

def extract_results(path):
    x_array = []
    y_array = []
    z_array = []
    xx_array = []
    yy_array = []
    zz_array = []
    number_of_simulations = 0
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "Final position in nm is" in line:
                number_of_simulations += 1
                line = line.strip().split()
                x_array.append(np.longdouble(line[5][1:-1]))
                y_array.append(np.longdouble(line[6][:-1]))
                z_array.append(np.longdouble(line[7][:-1]))
            elif "Square of the final position in nm is" in line:
                line = line.strip().split()
                xx_array.append(np.longdouble(line[8][1:-1]))
                yy_array.append(np.longdouble(line[9][:-1]))
                zz_array.append(np.longdouble(line[10][:-1]))
    x_average = np.average(x_array)
    y_average = np.average(y_array)
    z_average = np.average(z_array)
    xx_average = np.average(xx_array)
    yy_average = np.average(yy_array)
    zz_average = np.average(zz_array)
    t = 1e-9
    dt = 1e-15
    D = 2*1e-9
    with open("results.txt", "w") as file:
        file.write("--------------------------------------------------\n")
        file.write(f"Values in meters:\n")
        file.write(f"Number of simulations is {number_of_simulations}\n")
        file.write(f"Total time is {t}\n")
        file.write(f"dt is {dt}\n")
        file.write(f"n_steps = t/dt = {t/dt}\n")
        file.write(f"Average values of position:\n{x_average*1e-9, y_average*1e-9, z_average*1e-9}\n")
        file.write(f"Average square values of position:\n{xx_average*(1e-9)**2, yy_average*(1e-9)**2, zz_average*(1e-9)**2}\n")
        file.write(f"4*sqrt(2Dt/n_simulations) is {np.sqrt(2*D*t/number_of_simulations)*4}\n")
        file.write(f"2Dt is {2*D*t}\n\n\n")
        file.write("--------------------------------------------------\n")
        file.write(f"Values in nanometers:\n")
        file.write(f"Number of simulations is {number_of_simulations}\n")
        file.write(f"Total time is {t} s\n")
        file.write(f"dt is {dt} s\n")
        file.write(f"n_steps = t/dt = {t/dt}\n")
        file.write(f"Average values of position:\n{x_average:.4f}, {y_average:.4f}, {z_average:.4f} nm\n")
        file.write(f"Average square values of position:\n{xx_average:.4f}, {yy_average:.4f}, {zz_average:.4f} nm^2\n")
        a = np.sqrt(2*D*((1e+9)**2)*t/number_of_simulations)*4
        b = 2*D*((1e+9)**2)*t
        file.write(f"4*sqrt(2Dt/n_simulations) is {a:.4f} nm\n")
        file.write(f"2Dt is {b:.4f} nm^2 \n\n")
        file.write(f"Difference between expected values and the ones we got (in nm):\n")
        a = x_average - np.sqrt(2*D*((1e+9)**2)*t/number_of_simulations)*4
        b = y_average - np.sqrt(2*D*((1e+9)**2)*t/number_of_simulations)*4
        c = z_average - np.sqrt(2*D*((1e+9)**2)*t/number_of_simulations)*4
        file.write(f"x_avg - 4*sqrt(2Dt/n_simulations) is {a:.4f} nm\n")
        file.write(f"y_avg - 4*sqrt(2Dt/n_simulations) is {b:.4f} nm\n")
        file.write(f"z_avg - 4*sqrt(2Dt/n_simulations) is {c:.4f} nm\n")
        a = xx_average - 2*D*((1e+9)**2)*t
        b = yy_average - 2*D*((1e+9)**2)*t
        c = zz_average - 2*D*((1e+9)**2)*t
        file.write(f"x_avg**2 - 2Dt is {a:.4f} nm^2\n")
        file.write(f"y_avg**2 - 2Dt is {b:.4f} nm^2\n")
        file.write(f"z_avg**2 - 2Dt is {c:.4f} nm^2\n")
        file.write(f"--------------------------------------------------\n")
    print(f"Number of simulations is {number_of_simulations}\n")
    print(f"Total time is {t}\n")
    print(f"dt is {dt}\n")
    print(f"n_steps = t/dt = {t/dt}\n")
    print(f"Average values of position:\n{x_average*1e-9, y_average*1e-9, z_average*1e-9}\n")
    print(f"Average square values of position:\n{xx_average*(1e-9)**2, yy_average*(1e-9)**2, zz_average*(1e-9)**2}\n")
    print(f"4*sqrt(2Dt/n_simulations) is {np.sqrt(2*D*t/number_of_simulations)*4}\n")
    print(f"2Dt is {2*D*t}\n\n\n")
    print("--------------------------------------------------\n")
    print(f"Values in nanometers:\n")
    print(f"Number of simulations is {number_of_simulations}\n")
    print(f"Total time is {t*1e+9}\n")
    print(f"dt is {dt*1e+9}\n")
    print(f"n_steps = t/dt = {t/dt}\n")
    print(f"Average values of position:\n{x_average, y_average, z_average}\n")
    print(f"Average square values of position:\n{xx_average, yy_average, zz_average}\n")
    print(f"4*sqrt(2Dt/n_simulations) is {np.sqrt(2*D*((1e-9)**2)*t/number_of_simulations)*4}\n")
    print(f"2Dt is {2*D*((1e-9)**2)*t}\n\n")
    print(f"Difference between expected values and the ones we got (in nm):\n")
    print(f"x_avg - 4*sqrt(2Dt/n_simulations) is {x_average - np.sqrt(2*D*((1e-9)**2)*t/number_of_simulations)*4}\n")
    print(f"y_avg - 4*sqrt(2Dt/n_simulations) is {y_average - np.sqrt(2*D*((1e-9)**2)*t/number_of_simulations)*4}\n")
    print(f"z_avg - 4*sqrt(2Dt/n_simulations) is {z_average - np.sqrt(2*D*((1e-9)**2)*t/number_of_simulations)*4}\n")
    print(f"x_avg**2 - 2Dt is {xx_average - 2*D*((1e-9)**2)*t}\n")
    print(f"y_avg**2 - 2Dt is {yy_average - 2*D*((1e-9)**2)*t}\n")
    print(f"z_avg**2 - 2Dt is {zz_average - 2*D*((1e-9)**2)*t}\n")
    print(f"--------------------------------------------------\n")




    return 

path = "/Users/petrumilev/Documents/projects_python/Smaller_Projects/NanoFluidics_Project/System_one_e-9.txt"

extract_results(path)
