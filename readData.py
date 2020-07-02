
import numpy as np
import math
import pandas as pd
import os
import cv2

filepath = '/Users/kmcpherson/Documents/UROP/' #filepath to the main folder - can be changed depending on the user
testfile = filepath + 'testfile.txt' #tester file with more indices than just 0 & 1
datafile = filepath + 'dj02_3_a_good_1200x1200.txt'
col_coord = ['Visitor Index', 'X coordinate', 'Y coordinate', 'Time'] #names of the columns for the coordinate file
col_dir = ['Visitor Index', 'Action', 'Distance', 'Timestamp', 'Time Static'] #names of the columns for the directions file
file_list = []
heatmap_list = []

def separate_file(filename): #separates one .txt file into .txt files for each index
    file = open(filename, 'r') #whole .txt file with indices
    lines = file.readlines()
    index_dict = {} #dictionary that maps index to filepath
    for line in lines: #finds the indices, fills the dictionary
        index = line.split()[0] + 'file' #0file, 1file, ...
        if index not in index_dict: #if it's a new index
            file_list.append(filepath + index + '.txt') #adds the file to the global list
            index_dict[index] = filepath + index + '.txt' #make a key in the dict for it
            globals()[index] = open(index_dict[index], 'w') #opens each of the files and assigns them to a variable (0file = __, 1file = __)
        globals()[index].write(line)

def txt_to_csv(filename, cols): #converts a .txt to .csv
    f = open(filename, 'r') #open the file
    if 'dir' in cols: #create the columns
        columns = col_dir
    else:
        columns = col_coord

    read_file = pd.read_csv(filename, delimiter='\t', header=None, names=columns) #take in the .txt file
    read_file.to_csv(filename.replace('txt', 'csv'), index=None) #convert to .csv

def separate_and_convert(filename): #takes in the big .txt file, converts it into .csv files for each index
    separate_file(filename)
    for file in file_list:
        txt_to_csv(file, 'coord')

#simplify should be done after separating the big file
def simplify(filename): #takes in a .txt, simplifies to a .txt with fewer points (every second)
    f = open(filename, 'r')
    lines = f.readlines()
    desired_lines = []
    seconds_list = []
    for line in lines:
        split = line.split() #[index, x coord, y coord, time]
        if (int(float(split[3]))) not in seconds_list: #simplifies it to every second
            seconds_list.append(int(float(split[3])))
            desired_lines.append(line)
    file = open(filename.replace('.txt', '_sim.txt'), 'w') #create simplified file
    for line in desired_lines: #print every 24th line (every second)
        file.write(line[:len(line)-4:] + '0\n') #simplifies the seconds (0.0, 1.0, 2.0 ...)

def get_directions(filename, numDirections): #gets list (.txt) of directions from .txt file
    file = open(filename, 'r') #.txt file
    dir_file = open(filename.replace('.txt', '_dir.txt'), 'w') #file with directions

    interval = 360.0/numDirections #the range of each direction

    directions_dict = {} #dictionary of directions: [0-45:D1], [45-90:D2], [90-135:D3] ...
    for x in range(numDirections):
        directions_dict[(interval*x, interval*(x+1))] = ('D' + str(x+1)) #maps 'D1' to a range of degrees, 'D2' to the next range, etc.

    dir_list = [] #list of directions to see if it matches the previous line (in that case, just go forward)
    lines = file.readlines()
    for x in range(len(lines)-1): #for every line (except last)
        thisLine = lines[x].split()
        newLine = thisLine[0]
        nextLine = lines[x+1].split() #looks at next coords to get vector direction
        Ydiff = float(nextLine[2]) - float(thisLine[2]) #Y component
        Xdiff = float(nextLine[1]) - float(thisLine[1]) #X component
        distance = math.sqrt(Ydiff**2 + Xdiff**2)/29 # ** distance to use in the future for the unity simulation (meters)
        degrees = round((math.atan2(Xdiff, Ydiff)/math.pi*180), 1) #direction in degrees the person is moving at that second
        if degrees < 0: #accounts for negative degrees - makes the range 0 to 360 instead of -180 to 180
            degrees += 360

        for key in directions_dict:
            if degrees == 0 or distance <= 0.01: #if the person doesn't move
                dir_list.append('None')
                break
            elif key[0] < degrees <= key[1]: #if the person's direction falls within a D#'s range
                dir_list.append(directions_dict[key])
                break

    timeDiff, timePrint = 0,0
    for x in range(len(lines)-1): #for every line (except last)
        thisLine = lines[x].split()
        newLine = thisLine[0]
        nextLine = lines[x+1].split() #looks at next coords to get vector direction
        Ydiff = float(nextLine[2]) - float(thisLine[2]) #Y component
        Xdiff = float(nextLine[1]) - float(thisLine[1]) #X component
        distance = math.sqrt(Ydiff**2 + Xdiff**2)/29 # ** distance to use in the future for the unity simulation (meters)
        degrees = round((math.atan2(Xdiff, Ydiff)/math.pi*180), 1) #direction in degrees the person is moving at that second
        time_interval = float(nextLine[3]) - float(thisLine[3])

        if dir_list[x] == 'None': #if this line has no direction (doesn't move)
            newLine += '\tNone\t' #give it no direction
            distance = 0
            #time static column
            if dir_list[x-1] != 'None': #if this is the first 'None' (the previous one is not None)
                timeDiff = time_interval #start keeping track of time
                timePrint = 0.0
                if dir_list[x+1] != 'None': #if it's the first and last None (only 1 second)
                    timePrint = timeDiff
                    heatmap_list.append((int(float(thisLine[1])), int(float(thisLine[2]))))
                    timeDiff = 0.0
            else: #if there was a 'None' before this
                timeDiff += time_interval #add the line's time
                if dir_list[x+1] != 'None': #if this is the last 'None'
                    timePrint = timeDiff #record this time to print
                    heatmap_list.append((int(float(thisLine[1])), int(float(thisLine[2]))))
                    timeDiff = 0.0 #reset the time
        else: #if it has a direction
            timePrint = 0.0
            if dir_list[x] == dir_list[x-1]: #if this direction is the same as the previous line
                newLine += '\t' + 'F\t' #just go forward
            else:
                newLine += '\t' + dir_list[x] + ', F\t' #turn and go forward

        if timePrint == 0:
            timePrint = ''
        #newLine += str(round(distance,3)) + '\t' +(thisLine[3] + '\n') #distance and time columns (no time static)
        newLine += str(round(distance,3)) + '\t' +(thisLine[3] + '\t' + str(timePrint) + '\n') #distance, time, time static columns
        dir_file.write(newLine) #writes the line in the .txt file

# def old_get_directions(filename): #old directions function - U, D, L, R
#     file = open(filename, 'r') #.txt file
#     dir_file = open(filename.replace('.txt', '_dir.txt'), 'w') #file with directions
#     dir_dict = {} #dictionary of directions: D1, D2, D3 ...
#     UDLR_list = ['R', 'UR', 'U', 'UL', 'L', 'DL', 'D', 'DR']
#     UDLR_dict = {} #dictionary of U, D, L, R ...
#     for x in range(numDirections):
#         dir_dict[(interval*x - 22.5, interval*(x+1) - 22.5)] = ('D' + str(x+1))
#         UDLR_dict['D' + str(x+1)] = UDLR_list[x] #maps D1 to R, D2 to UR, etc
#     lines = file.readlines()
#     for x in range(len(lines)-1): #for every line (except last)
#         thisLine = lines[x].split()
#         newLine = thisLine[0]
#         nextLine = lines[x+1].split() #looks at next coords to get vector direction
#         Ydiff = float(nextLine[2]) - float(thisLine[2]) #Y component
#         Xdiff = float(nextLine[1]) - float(thisLine[1]) #X component
#         distance = math.sqrt(Ydiff**2 + Xdiff**2)/29 # ** distance to use in the future for the unity simulation (meters)
#         degrees = round((math.atan2(Xdiff, Ydiff)/math.pi*180), 1) #direction in degrees the person is moving at that second
#         if degrees < 0: #accounts for negative degrees - makes the range 0 to 360 instead of -180 to 180
#             degrees += 360
#         for key in dir_dict:
#             if degrees == 0: #if the person doesn't move
#                 newLine += '\tNone\t' #give it no direction
#                 break
#             elif key[0] < degrees <= key[1]: #if the person's direction falls within a D#'s range
#                 newLine += '\t' + UDLR_dict[dir_dict[key]] + '\t' #assign it to that direction in the file
#                 break
#         newLine += (thisLine[3] + '\n') #just time column
#         newLine += (str(degrees) + '\t' + thisLine[3] + '\n') #degrees and time columns
#         dir_file.write(newLine) #writes the line in the .txt file

def create_heatmap():
    img = cv2.imread(filepath + 'machu.jpg')
    height = img.shape[0]
    for coord in heatmap_list:
        cv2.circle(img,(coord[0],height-coord[1]), 5, (0,0,255), -1)
    cv2.imshow('image', img)
    cv2.waitKey(0)

separate_file(datafile) #separate the main file into files of each index
for file in file_list: #for the file of each index
    simplify(file) #simplify it to every second
    get_directions(file.replace('.txt', '_sim.txt'), 9) #get the directions of the simplified file
    txt_to_csv(file.replace('.txt', '_sim_dir.txt'), 'dir') #put that into a csv
create_heatmap() #has to be done after get_directions
