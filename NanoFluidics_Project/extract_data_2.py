import numpy as np 
import matplotlib.pyplot as plt

path_2_0 = "/Users/petrumilev/Documents/projects_python/Smaller_Projects/NanoFluidics_Project/Results/Simulation/System_2_0_nm_dist.txt"
path_2_5 = "/Users/petrumilev/Documents/projects_python/Smaller_Projects/NanoFluidics_Project/Results/Simulation/System_2_5_nm_dist.txt"
path_3_0 = "/Users/petrumilev/Documents/projects_python/Smaller_Projects/NanoFluidics_Project/Results/Simulation/System_3_0_nm_dist.txt"
path_3_5 = "/Users/petrumilev/Documents/projects_python/Smaller_Projects/NanoFluidics_Project/Results/Simulation/System_3_5_nm_dist.txt"
path_4_0 = "/Users/petrumilev/Documents/projects_python/Smaller_Projects/NanoFluidics_Project/Results/Simulation/System_4_0_nm_dist.txt"
path_4_5 = "/Users/petrumilev/Documents/projects_python/Smaller_Projects/NanoFluidics_Project/Results/Simulation/System_4_5_nm_dist.txt"

data_2_0 = []

def extract_data(path):
    to_return = []
    with open(path, "r") as file:
        lines = file.readlines()
        time = 0
        pos = 0
        for index, line in enumerate(lines):
            if "Final time in seconds" in line.strip():
                time = float(line.strip().split()[-1])
                a = lines[index + 1].strip().split()
                pos = np.linalg.norm(np.array([float(a[5][1:-1]), float(a[6][:-1]), float(a[7][:-1])]))
                to_return.append(("{:.2e}".format(time), np.round(pos,4)))
    return to_return

data_2_0 = extract_data(path_2_0)
data_2_5 = extract_data(path_2_5)
data_3_0 = extract_data(path_3_0)
data_3_5 = extract_data(path_3_5)
data_4_0 = extract_data(path_4_0)
data_4_5 = extract_data(path_4_5)

dictionary = {"2.0": data_2_0, "2.5": data_2_5, "3.0": data_3_0, "3.5": data_3_5, "4.0": data_4_0, "4.5": data_4_5}

all = [data_2_0, data_2_5, data_3_0, data_3_5, data_4_0, data_4_5]

def nr_captured(data):
    count = 0 
    for i in data:
        if i[1] <= 3.0:
            count += 1
    return count

def average_capture_time(data):
    time = []
    for i in data:
        if i[1] <= 3.0:
            time.append(np.float(i[0]))
    return time

print(f"Length of sets is: data_2_0: {len(data_2_0)}, data_2_5: {len(data_2_5)}, data_3_0: {len(data_3_0)}, data_3_5: {len(data_3_5)}, data_4_0: {len(data_4_0)}, data_4_5: {len(data_4_5)}")
print(f"Number of captured particles is: data_2_0: {nr_captured(data_2_0)}, data_2_5: {nr_captured(data_2_5)}, data_3_0: {nr_captured(data_3_0)}, data_3_5: {nr_captured(data_3_5)}, data_4_0: {nr_captured(data_4_0)}, data_4_5: {nr_captured(data_4_5)}")
#print(f"Average capture time is (in seconds): data_2_0: {average_capture_time(data_2_0)}, data_2_5: {average_capture_time(data_2_5)}, data_3_0: {average_capture_time(data_3_0)}, data_3_5: {average_capture_time(data_3_5)}, data_4_0: {average_capture_time(data_4_0)}, data_4_5: {average_capture_time(data_4_5)}")
print("--------------------------------------------------")
#print(f"Average capture time in nanoseconds is: data_2_0: {average_capture_time(data_2_0)*1e9}, data_2_5: {average_capture_time(data_2_5)*1e9}, data_3_0: {average_capture_time(data_3_0)*1e9}, data_3_5: {average_capture_time(data_3_5)*1e9}, data_4_0: {average_capture_time(data_4_0)*1e9}, data_4_5: {average_capture_time(data_4_5)*1e9}")


capt_times = [average_capture_time(i) for i in all]
capt_times_std = ["{:.4f}".format(np.std(np.array(i))*1e+9) for i in capt_times]
print(capt_times_std)

plt.title("Distribution of capture times")
plt.hist(capt_times[0], bins = 100, alpha = 0.5, label = "2.0 nm")
plt.hist(capt_times[1], bins = 100, alpha = 0.5, label = "2.5 nm")
plt.hist(capt_times[2], bins = 100, alpha = 0.5, label = "3.0 nm")
plt.hist(capt_times[3], bins = 100, alpha = 0.5, label = "3.5 nm")
plt.hist(capt_times[4], bins = 100, alpha = 0.5, label = "4.0 nm")
plt.hist(capt_times[5], bins = 100, alpha = 0.5, label = "4.5 nm")
plt.xlabel("Capture time (s)")
plt.ylabel("Number of captures")
plt.legend(loc = "upper right")
plt.show()
