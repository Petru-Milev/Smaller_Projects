import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, least_squares

def linear(x, a, b):
    return a*x + b

path_1 = "/Users/petrumilev/Documents/projects_python/Smaller_Projects/NanoFluidics_Project/Results/Simulation/System_one_e-9.txt"

with open(path_1, "r") as file:
    lines = file.readlines()
    p1, p2, p3, p4, p5, p6, p7, p8, p9, p10 = [], [], [], [], [], [], [], [], [], []
    final_position, square_final_position = [], []
    for index, line in enumerate(lines):
        count = 0
        if "Position number 1," in line.strip():
            a = lines[index + 2].strip().split()
            p1.append((float(a[5][:-1]), float(a[6][:-1]), float(a[7])))
            count += 1
        elif "Position number 2" in line.strip():
            a = lines[index + 2].strip().split()
            p2.append((float(a[5][:-1]), float(a[6][:-1]), float(a[7])))
            count += 1
        elif "Position number 3" in line.strip():
            a = lines[index + 2].strip().split()
            p3.append((float(a[5][:-1]), float(a[6][:-1]), float(a[7])))
            count += 1
        elif "Position number 4" in line.strip():
            a = lines[index + 2].strip().split()
            p4.append((float(a[5][:-1]), float(a[6][:-1]), float(a[7])))
            count += 1
        elif "Position number 5" in line.strip():
            a = lines[index + 2].strip().split()
            p5.append((float(a[5][:-1]), float(a[6][:-1]), float(a[7])))
            count += 1
        elif "Position number 6" in line.strip():
            a = lines[index + 2].strip().split()
            p6.append((float(a[5][:-1]), float(a[6][:-1]), float(a[7])))
            count += 1
        elif "Position number 7" in line.strip():
            a = lines[index + 2].strip().split()
            p7.append((float(a[5][:-1]), float(a[6][:-1]), float(a[7])))
            count += 1
        elif "Position number 8" in line.strip():
            a = lines[index + 2].strip().split()
            p8.append((float(a[5][:-1]), float(a[6][:-1]), float(a[7])))
            count += 1
        elif "Position number 9" in line.strip():
            a = lines[index + 2].strip().split()
            p9.append((float(a[5][:-1]), float(a[6][:-1]), float(a[7])))
            count += 1
        elif "Position number 10" in line.strip():
            a = lines[index + 2].strip().split()
            p10.append((float(a[5][:-1]), float(a[6][:-1]), float(a[7])))
            count += 1
        elif "Final position in nm is" in line.strip():
            a = line.strip().split()
            final_position.append((float(a[5][1:-1]), float(a[6][:-1]), float(a[7][:-1])))
            count += 1  
        elif "Square of the final position in nm is" in line.strip():
            a = line.strip().split()
            square_final_position.append((float(a[8][1:-1]), float(a[9][:-1]), float(a[10][:-1])))
            count += 1

p1 = [np.linalg.norm(i) for i in p1]
p1 = [i*(1e-9)**2 for i in p1]
p2 = [np.linalg.norm(i) for i in p2]
p2 = [i*(1e-9)**2 for i in p2]
p3 = [np.linalg.norm(i) for i in p3]
p3 = [i*(1e-9)**2 for i in p3]
p4 = [np.linalg.norm(i) for i in p4]
p4 = [i*(1e-9)**2 for i in p4]
p5 = [np.linalg.norm(i) for i in p5]
p5 = [i*(1e-9)**2 for i in p5]
p6 = [np.linalg.norm(i) for i in p6]
p6 = [i*(1e-9)**2 for i in p6]
p7 = [np.linalg.norm(i) for i in p7]
p7 = [i*(1e-9)**2 for i in p7]
p8 = [np.linalg.norm(i) for i in p8]
p8 = [i*(1e-9)**2 for i in p8]
p9 = [np.linalg.norm(i) for i in p9]
p9 = [i*(1e-9)**2 for i in p9]
p10 = [np.linalg.norm(i) for i in p10]
p10 = [i*(1e-9)**2 for i in p10]
p_x = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
p1_avg, p2_avg, p3_avg, p4_avg, p5_avg, p6_avg, p7_avg, p8_avg, p9_avg, p10_avg = np.average(p1), np.average(p2), np.average(p3), np.average(p4), np.average(p5), np.average(p6), np.average(p7), np.average(p8), np.average(p9), np.average(p10)
p = [p1_avg, p2_avg, p3_avg, p4_avg, p5_avg, p6_avg, p7_avg, p8_avg, p9_avg, p10_avg]
#p_std = [np.std(p1), np.std(p2), np.std(p3), np.std(p4), np.std(p5), np.std(p6), np.std(p7), np.std(p8), np.std(p9), np.std(p10)]
p_std = [np.std(i)/np.sqrt(len(i)) for i in p_x]
print(len(p1), np.sqrt(len(p1)))
print(p_std)

t = [0, 1*1e-10, 2*1e-10, 3*1e-10, 4*1e-10, 5*1e-10, 6*1e-10, 7*1e-10, 8*1e-10, 9*1e-10]
#print(p1[:10])
#print(p1_avg, p2_avg, p3_avg, p4_avg, p5_avg, p6_avg, p7_avg, p8_avg, p9_avg, p10_avg)
m, b = np.polyfit(t, p, 1)
#ax + b
popt, pcov = curve_fit(linear, t, p)
print(f"popt is {popt}")
print(f"pcov is {pcov}")
print(f"6D is {6*2.06*10**(-9)}")
fitted_data = popt[0]*np.array(t) + popt[1]

fig = plt.figure(figsize = (8, 6))
plt.title("Verification of the Einstein relation")
plt.plot(t, p, marker = 'o')
plt.plot(t, fitted_data, linestyle = '--')
plt.xlabel("Time (s)")
plt.ylabel("Position^2 (nm^2)")
plt.errorbar(t, p, yerr = p_std, linestyle = 'None')
plt.legend(["Position^2 (nm^2)", "Linear fit", "Standard deviation"])
plt.text(0.0*1e-10, 6.5*1e-18, f"Number of Samples is 20000")
plt.text(0.0*1e-10, 6.0*1e-18, f"Theoretical 6D is {6*2.06*10**(-9)}")
plt.text(0.0*1e-10, 5.5*1e-18, f"From the slope 6D is {popt[0]:.2e}")
plt.text(0.0*1e-10, 5.0*1e-18, f"Difference is {abs(6*2.06*10**(-9) - popt[0]):.2e}")
plt.text(0.0*1e-10, 4.5*1e-18, f"Relative Error is {abs(6*2.06*10**(-9) - popt[0])*100/(6*2.06*10**(-9)):.2f}"+"%")
plt.tight_layout()
plt.show()




