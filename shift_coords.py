
filepath = '/Users/kmcpherson/Documents/UROP/'
datafile = filepath + 'Videos/Video Text Files/dj08/g08_2_ad.txt'
copyfile = datafile.replace('ad', 'add')

def shiftcoords(xshift, yshift):
    file = open(datafile, 'r')
    newfile = open(copyfile, 'w')
    lines = file.readlines()
    for line in lines:
        index = line.split()[0]
        xcoord = float(line.split()[1])
        ycoord = float(line.split()[2])
        time = line.split()[3]
        newx = xcoord + xshift
        newy = ycoord + yshift
        if newx > 900:
            newx = 900
        if newy > 900:
            newy = 900
        if newx < 0:
            newx = 0
        if newy < 0:
            newy = 0
        newfile.write(index +'\t'+ str("{:.{}f}".format(newx, 3)) +'\t'+ str("{:.{}f}".format(newy, 3)) +'\t'+ time +'\n')

def make_diff():
    file = open(datafile, 'r')
    newfile = open(copyfile, 'w')
    lines = file.readlines()
    for line in lines:
        if line.split()[0] == '0':
            newfile.write('3' +'\t'+ line.split()[1] +'\t'+ line.split()[2] +'\t'+ line.split()[3] +'\n')
        elif line.split()[0] == '1':
            newfile.write('4' +'\t'+ line.split()[1] +'\t'+ line.split()[2] +'\t'+ line.split()[3] +'\n')
        elif line.split()[0] == '2':
            newfile.write('5' +'\t'+ line.split()[1] +'\t'+ line.split()[2] +'\t'+ line.split()[3] +'\n')

def combine():
    file1 = open(filepath + 'Videos/Video Text Files/dj08/g08_2.txt', 'r')
    file2 = open(filepath + 'Videos/Video Text Files/dj08/g08_2_add.txt', 'r')
    file3 = open(filepath + 'Videos/Video Text Files/dj08/g08_2_add2.txt', 'r')
    file4 = open(filepath + 'Videos/Video Text Files/dj08/g08_1_sim_add3.txt', 'r')
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

#shiftcoords(-2, 5)
#shiftcoords(2, -5) # change
#shiftcoords(4, -8) # change
#make_diff()
#combine()
