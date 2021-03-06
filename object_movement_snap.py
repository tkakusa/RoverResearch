# USAGE
# python object_movement.py --video object_tracking_example.mp4
# python object_movement.py

# import the necessary packages
from collections import deque
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import argparse
import imutils
import cv2
from functions import *

def capture():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
            help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=32,
            help="max buffer size")
    args = vars(ap.parse_args())

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)

    # initialize the list of tracked points, the frame counter,
    # and the coordinate deltas
    pts = deque(maxlen=args["buffer"])
    counter = 0
    (dX, dY) = (0, 0)
    (X, Y) = (0,0)
    direction = ""
    radius = 0

    # grab the reference to the webcam
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 80
    rawCapture = PiRGBArray(camera)

    camera.capture(rawCapture, format="bgr")
        
    # grab the current frame
    frame = rawCapture.array

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None


    # only proceed if at least one contour was found
    if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # cleanup the camera and close any open windows
    camera.close()

    if radius > 0:
        return True
    else:
        return False

def getLocation():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
            help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=32,
            help="max buffer size")
    args = vars(ap.parse_args())

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)

    # initialize the list of tracked points, the frame counter,
    # and the coordinate deltas
    pts = deque(maxlen=args["buffer"])
    counter = 0
    (dX, dY) = (0, 0)
    (x, y) = (0,0)
    direction = ""
    radius = 0

    # grab the reference to the webcam
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 80
    rawCapture = PiRGBArray(camera)

    camera.capture(rawCapture, format="bgr")
        
    # grab the current frame
    frame = rawCapture.array

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None


    # only proceed if at least one contour was found
    if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                            (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    pts.appendleft(center)
    
    # cleanup the camera and close any open windows
    camera.close()
    
    if radius > 0:
        return (x, y)
    else:
        return (-1,-1)

def continuousFollow():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
            help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=32,
            help="max buffer size")
    args = vars(ap.parse_args())

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)

    # initialize the list of tracked points, the frame counter,
    # and the coordinate deltas
    pts = deque(maxlen=args["buffer"])
    print (len(pts))
    counter = 0
    (dX, dY) = (0, 0)
    (x, y) = (0, 0)
    radius = 0
    direction = ""

    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
            camera = PiCamera()
            camera.resolution = (640, 480)
            camera.framerate = 32
            rawCapture = PiRGBArray(camera, size=(640, 480))
    # otherwise, grab a reference to the video file
    else:
            camera = cv2.VideoCapture(args["video"])

    # allow the camera to warmup
    time.sleep(0.1)


    # keep looping
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the current frame
            frame = image.array

            # if we are viewing a video and we did not grab a frame,
            # then we have reached the end of the video
            if args.get("video") and not grabbed:
                    break

            # resize the frame, blur it, and convert it to the HSV
            # color space
            frame = imutils.resize(frame, width=600)
            # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            # only proceed if at least one contour was found
            if len(cnts) > 0:
                    # find the largest contour in the mask, then use
                    # it to compute the minimum enclosing circle and
                    # centroid
                    c = max(cnts, key=cv2.contourArea)
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                    print (radius)

            # show the frame to our screen and increment the frame counter
            key = cv2.waitKey(1) & 0xFF
            counter += 1

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                    break

            
            if x < 70 and x > 0:
                print("left")
                Stop()
                time.sleep(.5)
                SlightTurn("Left")
                time.sleep(.5)
                Stop()
                time.sleep(.5)
            elif x > 520:
                print("right")
                Stop()
                time.sleep(.5)
                SlightTurn("Right")
                time.sleep(.3)
                Stop()
                time.sleep(.5)
            elif radius > 70:
                print("Too close")
                Stop()
                break
            elif len(cnts) > 0:
                print("forward")
                MoveForward()
            else:
                print("Nothing")
                Stop()

            

    # cleanup the camera and close any open windows
    camera.close()
    cv2.destroyAllWindows()
    Cleanup()
