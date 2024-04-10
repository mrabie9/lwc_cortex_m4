import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
data_dir = "../Data/Power/python_plots/idd_current/"
# Read the CSV file into a DataFrame
# df = pd.read_csv('Data/2024_03_29_08_57_01_32_rawfile_13.csv', delimiter=';', names=['x', 'y'])  # Replace 'data.csv' with the path to your CSV file

filenames = ['2024_03_29_14_54_33_1_rawfile_5.csv', '2024_03_29_14_54_33_1_rawfile_6.csv', '2024_03_29_14_54_33_1_rawfile_7.csv',
            '2024_03_29_14_54_33_1_rawfile_8.csv', '2024_03_29_14_54_33_1_rawfile_9.csv', '2024_03_29_14_54_33_1_rawfile_10.csv',
            '2024_03_29_14_54_33_1_rawfile_11.csv', '2024_03_29_14_54_33_1_rawfile_12.csv']
dfs_idd = []

for filename in filenames:
    df = pd.read_csv(data_dir + filename, delimiter=';', names=["x", "y"])
    dfs_idd.append(df)

data_dir = "../Data/Power/python_plots/3v3_current/"
filenames = ['2024_03_29_14_49_58_2_rawfile_21.csv', '2024_03_29_14_49_58_2_rawfile_22.csv', '2024_03_29_14_49_58_2_rawfile_23.csv',
            '2024_03_29_14_49_58_2_rawfile_24.csv', '2024_03_29_14_49_58_2_rawfile_25.csv', '2024_03_29_14_49_58_2_rawfile_26.csv',
            '2024_03_29_14_49_58_2_rawfile_27.csv', '2024_03_29_14_49_58_2_rawfile_28.csv']
dfs_3v3 = []

for filename in filenames:
    df = pd.read_csv(data_dir + filename, delimiter=';', names=["x", "y"])
    dfs_3v3.append(df)

# Concatenate all DataFrames into a single DataFrame
df_idd = pd.concat(dfs_idd, ignore_index=True)
df_3v3 = pd.concat(dfs_3v3, ignore_index=True)


# print(combined_df)
df = df_idd

# Assuming your CSV file has columns named 'x' and 'y', change them accordingly if they are different
x_values = df['x']/1e3
y_values = df['y']/1e6
x_values = x_values[:656000]
y_values = y_values[:656000]

x_3v3 = df_3v3['x']/1e3
x_3v3 = x_3v3 - 17.5 + 0.06 #+ (5.7-2.8)
y_3v3 = df_3v3['y']/1e6

x_3v3=x_3v3[143999:]
y_3v3 = y_3v3[143999:]
print(x_3v3)
# start_idx = x_3v3[x_3v3 == "4.00000"].index[0]
# print(start_idx)

# calculate energy
t = x_values[len(x_values)-1] - x_values[0]
average_IDD = round(y_values.mean(), 2)
print("t = ", t)
average_energy_idd = round(average_IDD * 3.3 * t, 2)
print("Average IDD energy = " + str(average_energy_idd) + " J")
average_3v3 = round(y_3v3.mean(), 2)
average_energy_3v3 = round(average_3v3 * 3.3 *t, 2)
print("Average 3V3 energy = " + str(average_energy_3v3) + " J")


# Plotting the graph
plt.plot(x_values, y_values,linestyle='-', label="IDD current")  # You can customize the marker and linestyle as needed
plt.plot(x_3v3, y_3v3,linestyle='-', label="3V3 current")  # You can customize the marker and linestyle as needed
plt.xlabel('Time (s)')  # Replace 'X Axis Label' with your desired label
plt.ylabel('Current (A)')  # Replace 'Y Axis Label' with your desired label
plt.title('Current flowing through 3V3 vs IDD pins')  # Replace 'Title of the Graph' with your desired title
plt.legend(loc='upper right')
plt.text(7.0, 0.055, "Average IDD energy = " + str(average_energy_idd) + " J", fontsize=12, ha='center', va='center', color='black')
plt.text(7.0, 0.19, "Average 3V3 energy = " + str(average_energy_3v3) + " J", fontsize=12, ha='center', va='center', color='black')
plt.grid(True)  # Add gridlines if needed
plt.show()


