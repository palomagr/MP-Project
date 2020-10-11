
import math
import cv2

filepath = '/Users/Isbla/Directions/Assets/Scripts/MP-Project-master/' #filepath to the main folder - can be changed depending on the user
datafile = 'dj01_1.txt'
col_coord = ['Visitor Index', 'X coordinate', 'Y coordinate', 'Time'] #names of the columns for the coordinate file
col_dir = ['Visitor Index', 'Action', 'Distance', 'Timestamp', 'Time Static'] #names of the columns for the directions file

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

def get_directions(filename): #gets list (.txt) of directions from .txt file
    file = open(filename, 'r') #.txt file
    dir_file = open(filename.replace('.txt', '_dir.txt'), 'w') #file with directions

    dir_list = [] #list of directions to see if it matches the previous line (in that case, just go forward)
    lines = file.readlines()
    
    for x in range(len(lines)-1): #for every line (except last)
        thisLine = lines[x].split()
        nextLine = lines[x+1].split() #looks at next coords to get vector direction
        Ydiff = float(nextLine[2]) - float(thisLine[2]) #Y component
        Xdiff = float(nextLine[1]) - float(thisLine[1]) #X component
        distance = math.sqrt(Ydiff**2 + Xdiff**2)/29*(4/3) #distance the person moves (4/3 b/c it's out of 900 & it should be 1200)
        degrees = round((math.atan2(Xdiff, Ydiff)/math.pi*180), 1) #direction in degrees the person is moving at that second
        
        if degrees < 0: #accounts for negative degrees - makes the range 0 to 360 instead of -180 to 180
            degrees += 360

        if degrees == 0 or distance <= 0.0042:
            dir_list.append('None')
        else: 
            dir_list.append(str(degrees))
    
    timeDiff, timePrint = 0,0
    for x in range(len(lines)-1): #for every line (except last)
        thisLine = lines[x].split()
        newLine = thisLine[0]
        nextLine = lines[x+1].split() #looks at next coords to get vector direction
        Ydiff = float(nextLine[2]) - float(thisLine[2]) #Y component
        Xdiff = float(nextLine[1]) - float(thisLine[1]) #X component
        distance = math.sqrt(Ydiff**2 + Xdiff**2) # ** distance to use in the future for the unity simulation (meters)
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
                    timeDiff = 0.0
            else: #if there was a 'None' before this
                timeDiff += time_interval #add the line's time
                if dir_list[x+1] != 'None': #if this is the last 'None'
                    timePrint = timeDiff #record this time to print
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

get_directions(datafile) #get the directions of the file
    #txt_to_csv(file, 'dir') #put that into a csv
#create_heatmap() #has to be done after get_directions
