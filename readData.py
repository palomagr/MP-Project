
import numpy as np
import math
import pandas as pd
import os
import cv2
from PIL import Image

filepath = '/Users/kmcpherson/Documents/UROP/' #filepath to the main folder - can be changed depending on the user
testfile = filepath + 'testfile.txt' #tester file with more indices than just 0 & 1
datafile = filepath + 'Videos/Video Text Files/dj01/g01_2.txt'
col_coord = ['Visitor Index', 'X coordinate', 'Y coordinate', 'Time'] #names of the columns for the coordinate file
col_dir = ['Visitor Index', 'Action', 'Distance', 'Timestamp', 'Time Static'] #names of the columns for the directions file
file_list = []
BLUE = (3, 155, 229)
GREEN = (30, 187, 120)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

heatmap_dict = {}
for x in range(900):
    for y in range(900):
        heatmap_dict[(x,y)] = -1

heat_color = {BLUE: [],
              GREEN: [],
              YELLOW: [],
              ORANGE: [],
              RED: []}


def separate_file(filename):
    """
    Separates one .txt file into individual .txt files for each index
    """
    file = open(filename, 'r') #whole .txt file with indices
    lines = file.readlines()
    index_dict = {} #dictionary that maps index to filepath
    for line in lines: #finds the indices, fills the dictionary
        index = line.split()[0] + 'file' #0file, 1file, ...
        if index not in index_dict: #if it's a new index
            file_list.append(filename.replace('.txt', '__'+index+'.txt')) #adds the file to the global list
            index_dict[index] = filename.replace('.txt', '__'+index+'.txt') #make a key in the dict for it
            globals()[index] = open(index_dict[index], 'w') #opens each of the files and assigns them to a variable (0file = __, 1file = __)
        globals()[index].write(line)



def txt_to_csv(filename, cols):
    """
    Converts a .txt file to .csv
    """
    f = open(filename, 'r') #open the file
    if 'dir' in cols: #create the columns
        columns = col_dir
    else:
        columns = col_coord

    read_file = pd.read_csv(filename, delimiter='\t', header=None, names=columns) #take in the .txt file
    read_file.to_csv(filename.replace('txt', 'csv'), index=None) #convert to .csv


def separate_and_convert(filename):
    """
    Takes in the big .txt file, converts it into .csv files for each index
    """
    separate_file(filename)
    for file in file_list:
        txt_to_csv(file, 'coord')


def simplify(filename):
    """
    Takes in a .txt, simplifies to a .txt with fewer points (every second)
    *** SHOULD BE DONE AFTER SEPARATE ***
    """
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


def get_directions(filename, numDirections):
    """
    Gets list (.txt) of directions from .txt file
    """
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
        distance = math.sqrt(Ydiff**2 + Xdiff**2)*(4/3) #distance the person moves (4/3 b/c it's out of 900 & it should be 1200)
        degrees = round((math.atan2(Xdiff, Ydiff)/math.pi*180), 1) #direction in degrees the person is moving at that second
        if degrees < 0: #accounts for negative degrees - makes the range 0 to 360 instead of -180 to 180
            degrees += 360

        for key in directions_dict:
            if degrees == 0 or distance < .25: #if the person doesn't move
                dir_list.append('None')
                break
            elif key[0] < degrees <= key[1]: #if the person's direction falls within a D#'s range
                dir_list.append(directions_dict[key])
                break

    timeDiff, timePrint = 0,0
    for x in range(len(lines)-2): #for every line (except last)
        thisLine = lines[x].split()
        newLine = thisLine[0]
        nextLine = lines[x+1].split() #looks at next coords to get vector direction
        Ydiff = float(nextLine[2]) - float(thisLine[2]) #Y component
        Xdiff = float(nextLine[1]) - float(thisLine[1]) #X component
        distance = math.sqrt(Ydiff**2 + Xdiff**2)*(4/3) # ** distance to use in the future for the unity simulation (meters)
        degrees = round((math.atan2(Xdiff, Ydiff)/math.pi*180), 1) #direction in degrees the person is moving at that second
        time_interval = float(nextLine[3]) - float(thisLine[3])

        this_point = (int(float(thisLine[1])), int(float(thisLine[2])))
        if this_point[0] < 0:
            this_point = (0, this_point[1])
        elif this_point[0] > 899:
            this_point = (899, this_point[1])
        if this_point[1] < 0:
            this_point = (this_point[0], 0)
        elif this_point[1] > 899:
            this_point = (this_point[0], 899)

        if dir_list[x] == 'None': #if this line has no direction (doesn't move)
            newLine += '\tNone\t' #give it no direction
            distance = 0
            #time static column
            if dir_list[x-1] != 'None': #if this is the first 'None' (the previous one is not None)
                timeDiff = time_interval #start keeping track of time
                timePrint = 0.0
                if dir_list[x+1] != 'None': #if it's the first and last None (only 1 second)
                    timePrint = timeDiff #record this time to print

                    if heatmap_dict[this_point] == -1:
                        heatmap_dict[this_point] = 0
                    else:
                        heatmap_dict[this_point] += timePrint

                    timeDiff = 0.0
            else: #if there was a 'None' before this
                timeDiff += time_interval #add the line's time
                if dir_list[x+1] != 'None': #if this is the last 'None'
                    timePrint = timeDiff

                    if heatmap_dict[this_point] == -1:
                        heatmap_dict[this_point] = 0
                    else:
                        heatmap_dict[this_point] += timePrint

                    timeDiff = 0.0 #reset the time
        else: #if it has a direction
            timePrint = 0.0

            if heatmap_dict[this_point] == -1:
                heatmap_dict[this_point] = 0
            else:
                heatmap_dict[this_point] += time_interval

            if dir_list[x] == dir_list[x-1]: #if this direction is the same as the previous line
                newLine += '\t' + 'F\t' #just go forward
            else:
                newLine += '\t' + dir_list[x] + ', F\t' #turn and go forward

        if timePrint == 0:
            newLine += str(round(distance,3)) + '\t' +(thisLine[3] + '\t' + '' + '\n')
        else:
            newLine += str(round(distance,3)) + '\t' +(thisLine[3] + '\t' + str("{:.{}f}".format(timePrint, 2)) + '\n') #distance, time, time static columns

        dir_file.write(newLine) #writes the line in the .txt file
    old_filename = filename.replace('.txt', '_dir.txt')
    new_filename = filepath + 'Videos/Video Text Files/Directions/' + os.path.basename(old_filename)
    os.rename(old_filename, new_filename)
    dir_file.close()


def create_heatmap():
    """
    Makes a cumulative heatmap from all the files that have been made so far.
    """
    assign_colors(heat_color)
    draw_heatmap(heat_color)

# HELPER FUNCTIONS

def assign_colors(heat_color):
    """
    Helper function: given a dictionary to fill,
    assigns coordinates to one of 5 color groups
    """
    for y in range(900):
        for x in range(900):
            heat_value = heatmap_dict[(x,y)] # do it on result instead of image
            if heat_value == -1: # no one's ever walked there - make it blue
                heat_color[BLUE].append((x,y))
            elif 0 <= heat_value <= 0.05:
                heat_color[GREEN].append((x,y))
            elif 0.05 < heat_value <= 1:
                heat_color[YELLOW].append((x,y))
            elif 1 < heat_value <= 4:
                heat_color[ORANGE].append((x,y))
            else: # > 4
                heat_color[RED].append((x,y))


def draw_heatmap(heat_color):
    """
    Helper function. Given a dictionary of color values,
    creates an image with the heatmap and returns it.
    """
    image = load_image('/Users/kmcpherson/Documents/UROP/machu.jpg')
    result = {'height': image['height'],
              'width': image['width'],
              'pixels': image['pixels'].copy()}

    for coord in heat_color[BLUE]:
        x, y = coord[0], coord[1]
        set_pixel(result, x, y, BLUE)

    for coord in heat_color[GREEN]:
        x, y = coord[0], coord[1]
        draw_circle(result, x, y, 12, GREEN)

    for coord in heat_color[YELLOW]:
        x, y = coord[0], coord[1]
        draw_circle(result, x, y, 12, YELLOW)

    for coord in heat_color[ORANGE]:
        x, y = coord[0], coord[1]
        draw_circle(result, x, y, 12, ORANGE)

    for coord in heat_color[RED]:
        x, y = coord[0], coord[1]
        draw_circle(result, x, y, 12, RED)

    save_image(result, '/Users/kmcpherson/Documents/UROP/heatmap.png')


def draw_circle(image, x, y, radius, color):
    """
    Helper function.
    Given: an image to draw on, a coordinate (x,y), a radius, and a color.
    Draws a circle of that radius (outline of 2 pixels)
    and of the selected color on the image, at the specified point.
    """
    PI = 3.1415926535
    for angle in range(360):
        x1 = int((radius-1) * math.cos(angle * PI / 180))
        y1 = int((radius-1) * math.sin(angle * PI / 180))
        set_pixel(image, x+x1, y+y1, color)
        x1 = int(radius * math.cos(angle * PI / 180))
        y1 = int(radius * math.sin(angle * PI / 180))
        set_pixel(image, x+x1, y+y1, color)



def load_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def get_pixel(image, x, y):
    width = image['width']
    height = image['height']
    if x in range(width) and y in range(height): # if it's in the original image
        return image['pixels'][width*y + x] # new calculation for index
    else: # if it's outside of the image
        if x < 0: # to the left of the image
            return get_pixel(image, 0, y) # return the pixel at the beginning of the row
        elif x > (width-1): # to the right of the image
            return get_pixel(image, width-1, y) # return the pixel at the end of the row
        if y < 0: # above the image
            return get_pixel(image, x, 0) # return the pixel at the top of the column
        elif y > (height-1): # below the image
            return get_pixel(image, x, height-1) # return the pixel at the bottom of the column


def set_pixel(image, x, y, c):
    image['pixels'][image['width']*y + x] = c


if __name__ == '__main__':
    folder = '/Users/kmcpherson/Documents/UROP/Videos/Video Text Files/'

    # add the free walker files
    for video in ['dj01/dj01_', 'dj02/dj02_', 'dj08/dj08_']:
        for i in range(1,100):
            name = folder + video + str(i) + '_sim.txt'
            if os.path.exists(name):
                separate_file(name)
            else:
                break

    # add the group files
    for video in ['dj01/g01_', 'dj02/g02_', 'dj08/g08_']:
        for i in range(1,100):
            name = folder + video + str(i) + '_sim.txt'
            if os.path.exists(name):
                separate_file(name)
            else:
                break

    for file in file_list: # for every file we've looked throug
        get_directions(file, 9) #get the directions of the file
        # txt_to_csv(file.replace('.txt', '_dir.txt'), 'dir') #put that into a csv
    create_heatmap() #has to be done after get_directions
    for file in file_list:
        os.remove(file)



    #
