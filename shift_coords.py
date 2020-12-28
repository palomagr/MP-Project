
filepath = '/Users/kmcpherson/Documents/UROP/'
datafile = filepath + 'Videos/Video Text Files/dj08/g08_2.txt'
copyfile1 = datafile.replace('ad', 'add1')
copyfile2 = datafile.replace('ad', 'add2')
copyfile3 = datafile.replace('ad', 'add3')

def shiftcoords(xshift, yshift):
    """
    Shifts the coordinate by the specified x and y amounts.
    """
    file = open(datafile, 'r')
    newfile = open(copyfile1, 'w')
    lines = file.readlines()
    for line in lines:
        index = line.split()[0]
        xcoord = float(line.split()[1])
        ycoord = float(line.split()[2])
        time = line.split()[3]
        newx = xcoord + xshift
        newy = ycoord + yshift
        # keep the new coordinates within the 0-900 bounds
        if newx > 899:
            newx = 899
        if newy > 899:
            newy = 899
        if newx < 0:
            newx = 0
        if newy < 0:
            newy = 0
        newfile.write(index +'\t'+ str("{:.{}f}".format(newx, 3)) +'\t'+ str("{:.{}f}".format(newy, 3)) +'\t'+ time +'\n')

def make_diff():
    """
    Used the change the indices of a file.
    This can be useful if you got the coordinates of a large group using several smaller groups.
        For example: A group of 9 people was recorded using 3 groups of 3 people.
        You now have three files with indices 0-2, but you can change the last
        two files to indices 3-5 and 6-8.
    """
    file = open(datafile, 'r')
    newfile = open(copyfile1, 'w')
    lines = file.readlines()
    for line in lines:
        if line.split()[0] == '0':
            newfile.write('3' +'\t'+ line.split()[1] +'\t'+ line.split()[2] +'\t'+ line.split()[3] +'\n')
        elif line.split()[0] == '1':
            newfile.write('4' +'\t'+ line.split()[1] +'\t'+ line.split()[2] +'\t'+ line.split()[3] +'\n')
        elif line.split()[0] == '2':
            newfile.write('5' +'\t'+ line.split()[1] +'\t'+ line.split()[2] +'\t'+ line.split()[3] +'\n')

def combine():
    """
    Combines several smaller files into one big file, based on index.
    Whenever it reaches a line with index 0, it writes the rest of the indices in the file.
    """
    file1 = open(filepath + 'Videos/Video Text Files/dj08/g08_2.txt', 'r')
    file2 = open(filepath + 'Videos/Video Text Files/dj08/g08_2_add1.txt', 'r')
    file3 = open(filepath + 'Videos/Video Text Files/dj08/g08_2_add2.txt', 'r')
    file4 = open(filepath + 'Videos/Video Text Files/dj08/g08_2_add3.txt', 'r')
    newfile = open(filepath + 'Videos/Video Text Files/dj08/g08_2_com.txt', 'w')
    lines1 = file1.readlines()
    lines2 = file2.readlines()
    lines3 = file3.readlines()
    lines4 = file4.readlines()
    for i in range(len(lines1)):
        if lines1[i].split()[0] == '0':
            for j in range(3):
                newfile.write(lines1[i+j])
            for j in range(3):
                newfile.write(lines2[i+j])
            for j in range(3):
                newfile.write(lines3[i+j])
            for j in range(3):
                newfile.write(lines4[i+j])
    newfile.close()


if __name__ == '__main__':

    #shiftcoords(4, -8)
    #make_diff()
    #combine()
