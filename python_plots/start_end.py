import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
data_dir = "../Data/Power/python_plots/start_end_loop/"
# Read the CSV file into a DataFrame
# df = pd.read_csv('Data/2024_03_29_08_57_01_32_rawfile_13.csv', delimiter=';', names=['x', 'y'])  # Replace 'data.csv' with the path to your CSV file

filenames = ['2024_04_09_19_54_29_15_rawfile_4.csv', '2024_04_09_19_54_29_15_rawfile_5.csv', '2024_04_09_19_54_29_15_rawfile_6.csv',
            '2024_04_09_19_54_29_15_rawfile_7.csv', '2024_04_09_19_54_29_15_rawfile_8.csv', '2024_04_09_19_54_29_15_rawfile_9.csv',
            '2024_04_09_19_54_29_15_rawfile_10.csv', '2024_04_09_19_54_29_15_rawfile_11.csv']
dfs_idd = []

for filename in filenames:
    df = pd.read_csv(data_dir + filename, delimiter=';', names=["x", "y"])
    dfs_idd.append(df)

# Concatenate all DataFrames into a single DataFrame
df_idd = pd.concat(dfs_idd, ignore_index=True)


# print(combined_df)
df = df_idd

# Assuming your CSV file has columns named 'x' and 'y', change them accordingly if they are different
x_values = df['x']/1e3
y_values = df['y']/1e6

specific_x_val = 3.99519
index_of_x = x_values[x_values== specific_x_val].index[0]

annotate_x = x_values[index_of_x]
annotate_y = round(y_values[index_of_x], 4)

# Annotate the point with its coordinates
plt.annotate(f'({annotate_x}, {annotate_y})', xy=(annotate_x, annotate_y), xytext=(annotate_x-2e-5, annotate_y+1e-4))
plt.xlim(x_values[index_of_x]-9e-5,x_values[index_of_x]+5e-5 )
plt.gca().yaxis.set_ticks_position('right')
plt.gca().yaxis.set_label_position('right')
# Plotting the graph
plt.plot(x_values, y_values,linestyle='-')  # You can customize the marker and linestyle as needed
plt.xlabel('Time (s)')  # Replace 'X Axis Label' with your desired label
plt.ylabel('Current (A)')  # Replace 'Y Axis Label' with your desired label
plt.title('Example of program start and end')  # Replace 'Title of the Graph' with your desired title


# plt.text(4.28073, 0.047, "Start of program", fontsize=12, ha='center', va='center', color='black')
plt.grid(True)  # Add gridlines if needed
plt.show()


