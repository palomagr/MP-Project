
#!/usr/bin/python
#
# Copyright 2018 BIG VISION LLC ALL RIGHTS RESERVED
#
# /// = code by Kimmy
from __future__ import print_function
import sys
import cv2
from random import randint
import math
from scipy import special
import time as tm #///

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
bboxes = []
colors = {0:(0,0,255), 1:(0,128,255), 2:(0,255,255), 3:(0,255,0), 4:(255,0,0), 5:(255,0,128)} #/// makes dict of colors - first person red, second orange, ...

def createTrackerByName(trackerType):
  # Create a tracker based on tracker name
    if trackerType == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]:
        tracker = cv2.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif trackerType == trackerTypes[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)

    return tracker

def create_boxes(): #/// helper method - select boxes
    global bboxes
    bboxes = []
    while True:
        # draw bounding boxes over objects
        # selectROI's default behaviour is to draw box starting from the center
        # when fromCenter is set to false, you can draw box starting from top left corner
        bbox = cv2.selectROI('Select Boxes', frame)
        bboxes.append(bbox)
        print("Press q to quit selecting boxes and start tracking")
        print("Press any other key to select next object")
        if cv2.waitKey(0) & 0xFF == ord('q'):  # q is pressed (quit)
            print("q pressed")
            break
    i = 0 #/// this section updates rectangle sizes when you reselect
    for bbox in bboxes:
        rwid[i] = bbox[2]
        rlen[i] = bbox[3]
        i += 1


if __name__ == '__main__':

    print("Default tracking algoritm is CSRT\nAvailable tracking algorithms are:\n")
    for t in trackerTypes:
      print(t)

    trackerType = "CSRT"

    # Set video to load
    videoPath = '/Users/kmcpherson/Documents/UROP/Videos/dj08/dj08_2.mp4'
    text_string = 'dj08_2.txt' # full file - records every frame
    sim_text_string = 'dj08_2_sim.txt' #/// simplified file - records every second

    # Create a video capture object to read videos
    cap = cv2.VideoCapture(videoPath)
    fps = cap.get(cv2.CAP_PROP_FPS)
    time = cap.get(cv2.CAP_PROP_POS_MSEC)/1000

    # Read first frame
    cx, cy, user = 0,0,0
    success, frame = cap.read() # read the first frame
    width, height, channels = frame.shape #/// get width and height

    if not success: # quit if unable to read the video file
        print('Failed to read video')
        sys.exit(1)

    rwid = {} #/// width of the rect. drawn for each person
    rlen = {} #/// length of the rect. drawn for each person

    create_boxes() #/// helper method
    #print('Selected bounding boxes {}'.format(bboxes)) # check the boxes you selected

    multiTracker = cv2.MultiTracker_create() # Create MultiTracker object
    i = 0
    for bbox in bboxes: #/// make the rectangles for each person
        rwid[i] = bbox[2]
        rlen[i] = bbox[3]
        i += 1
        multiTracker.add(createTrackerByName(trackerType), frame, bbox)

    f = open(text_string, "w") # open full file
    fsim = open(sim_text_string, "w") #/// open simplified file

    print('Press X to reselect boxes')

    while cap.isOpened(): # Process video and track objectspremie
        success, frame = cap.read()
        font = cv2.FONT_HERSHEY_SIMPLEX #///
        time_mins_secs = tm.strftime('%M:%S', tm.gmtime((time))) #/// time (min:sec)
        cv2.putText(frame,time_mins_secs,(int(.85*width),int(.05*height)),font,1,(255,255,255),2,cv2.LINE_AA) #/// timestamp, upper right
        if not success: # if video ends or can't be read
            print("Failed")
            break

        # get updated location of objects in subsequent frames
        success, boxes = multiTracker.update(frame)

        for user, newbox in enumerate(boxes):
            x, y = int(newbox[0]), int(newbox[1]) #/// starting point
            wid, len = rwid[user], rlen[user] #/// width and length of the selected rectangle
            cv2.rectangle(frame, (x,y), (x+wid, y+len), colors[user], 2, 1) #/// draws a rectangle around the object
            cx = ((newbox[0]) + (wid/2)) * (900/width) #/// midpoint of the selected region in x (image is 900 pixels)
            cy = ((newbox[1]) + (len/2)) * (900/height) #/// midpoint of the selecteed region in y
            time = cap.get(cv2.CAP_PROP_POS_MSEC)/1000

            f.write(str(user) +'\t'+ # unsimplified file
                    str("{:.{}f}".format(cx, 3)) +'\t'+
                    str("{:.{}f}".format(cy, 3)) +'\t'+
                    str("{:.{}f}".format(time, 3)) +'\n')

            if time%1 <= (1/fps): #/// simplified file (every second)
                fsim.write(str(user) +'\t'+
                           str("{:.{}f}".format(cx, 3))+'\t'+
                           str("{:.{}f}".format(cy, 3))+'\t'+
                           str(float(int(time))) +'\n') #write data

        # track trajectories / write data
        cv2.imshow('Tracking Trajectories', frame)

        if cv2.waitKey(1) & 0xFF == ord('x'): #/// X pressed - reselect boxes
            create_boxes()
            multiTracker = cv2.MultiTracker_create()
            for bbox in bboxes:
                multiTracker.add(createTrackerByName(trackerType), frame, bbox)

        # quit on ESC button
        elif cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break

    f.close() # close the files at the end
    fsim.close()
