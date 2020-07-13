
#!/usr/bin/python
#
# Copyright 2018 BIG VISION LLC ALL RIGHTS RESERVED
#
from __future__ import print_function
import sys
import cv2
from random import randint
import math
from scipy import special

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
bboxes = []
colors = []

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

def create_boxes(): # helper method - select boxes
    ## Select boxes
    global bboxes
    bboxes = []
    global colors
    colors = []
    while True:
        # draw bounding boxes over objects
        # selectROI's default behaviour is to draw box starting from the center
        # when fromCenter is set to false, you can draw box starting from top left corner
        bbox = cv2.selectROI('Select Boxes', frame)
        bboxes.append(bbox)
        colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
        print("Press q to quit selecting boxes and start tracking")
        print("Press any other key to select next object")
        if cv2.waitKey(0) & 0xFF == ord('q'):  # q is pressed
            print("q pressed")
            break

    #print('Selected bounding boxes {}'.format(bboxes))


if __name__ == '__main__':

    print("Default tracking algoritm is CSRT\nAvailable tracking algorithms are:\n")
    for t in trackerTypes:
      print(t)

    trackerType = "CSRT"

    # Set video to load
    videoPath = '/Users/kmcpherson/Documents/UROP/Videos/dj08_0.mp4'
    text_string = 'dj08_0.txt'

    # Create a video capture object to read videos
    cap = cv2.VideoCapture(videoPath)
    fps = cap.get(cv2.CAP_PROP_FPS)
    timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
    calc_timestamps = [0.0]
    ts,cur_ts, prev_ts = 0,0,0
    rrr = '0'
    time = '0'

    # Read first frame
    cx, cy, cx0, cy0, user = 0,0,0,0,0
    success, frame = cap.read()
    width, height, channels = frame.shape

    if not success: # quit if unable to read the video file
        print('Failed to read video')
        sys.exit(1)

    create_boxes()
    print('Selected bounding boxes {}'.format(bboxes))

    multiTracker = cv2.MultiTracker_create() # Create MultiTracker object
    for bbox in bboxes: # Initialize MultiTracker
        multiTracker.add(createTrackerByName(trackerType), frame, bbox)

    f = open(text_string, "w") #open the file to write to

    while cap.isOpened(): # Process video and track objectspremie
        success, frame = cap.read()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,time,(1070,60), font, 1,(255,255,255),2,cv2.LINE_AA) #timestamp
        if not success:
            print("Failed")
            break

        # get updated location of objects in subsequent frames
        success, boxes = multiTracker.update(frame)
        users = {}

        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
            cx = ((int(newbox[0])+ int(newbox[0] + newbox[2]))/2) * (900/width) #mid point of the selected region of interest in x
            cy = ((int(newbox[1]) + int(newbox[1] + newbox[3])) / 2) * (900/height) #mid point of the selecteed region of interest in y
            user = i
            cur_ts = str((cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))
            num = cap.get(cv2.CAP_PROP_POS_MSEC)/1000
            time = str("{:.{}f}".format(num, 3))
            r, rr = cur_ts.split('.')
            if r != rrr:
             rrr = r

            # if float(time)%1 < 0.042: #every second
            #     f.write(str(user) + '\t' +
            #     str("{:.{}f}".format(cx, 3)) + '\t' + str("{:.{}f}".format(cy, 3))
            #     + '\t' + str("{:.{}f}".format(num, 1)) +  '\n') #write data

        # show frame / write data
        cv2.imshow('Tracking Trajectories', frame)

        #spacebar = 32
        if cv2.waitKey(1) & 0xFF == ord('x'): # X pressed
            create_boxes()
            print('Selected bounding boxes {}'.format(bboxes))
            multiTracker = cv2.MultiTracker_create() # Create MultiTracker object
            for bbox in bboxes: # Initialize MultiTracker
                multiTracker.add(createTrackerByName(trackerType), frame, bbox)

        # quit on ESC button
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break


    #for i, (ts, cts) in enumerate(zip(timestamps, calc_timestamps)):
        #print('Frame %d difference:' % i, abs(ts - cts))
    f.close()
