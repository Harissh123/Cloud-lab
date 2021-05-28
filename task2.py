import numpy as np
import csv
import argparse

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "csv file name")
args = parser.parse_args()


# Checking if the argument is valid
if args.file[-4:] != ".csv":
    print("Enter Valid file name ending with .csv")
    exit()


# Reading the CSV File
with open(args.file, newline='') as csvfile:
    data = list(csv.reader(csvfile))

# Separating all the headers
header = data[0]
marks = {}

# Creating an empty dictionary with Headers as Keys and the rest as Values
for h in header:
    marks[h] = []

# Populate the Dictionary 
for i in range(1, len(data)):
    for j in range(len(data[i])):
        if header[j] != "Name":
            data[i][j] = int(data[i][j])

        marks[header[j]].append(data[i][j])    
        


print("============ 1. Topper in each subject============")
subjects = ['Maths', 'Biology', 'English', 'Physics', 'Chemistry', 'Hindi']
for s in subjects:
    topper_index = np.argmax(marks[s])

    print(f"Topper in {s}: {marks['Name'][topper_index]}")

print("============ 2. Top 3 students============")
marks['aggr'] = []
arr = np.array([marks['Maths'], marks['Biology'], marks['English'], marks['Physics'], marks['Chemistry'], marks['Hindi']])
marks['aggr'] = np.add(0, arr.sum(axis=0))

toppers = sorted(zip(marks['aggr'], marks['Name']), reverse=True)[:3]
print(f"Best students in the class are ({toppers[0][1]}, {toppers[1][1]}, {toppers[2][1]})")