from imutils.video import VideoStream
#from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from imutils.video import FPS
import os
import numpy as np
import argparse
import imutils
import time
import cv2


p="C:\\Users\\peace\\Desktop\\video editing tool\\real-time-object-detection\\MobileNetSSD_deploy.prototxt.txt"
m="C:\\Users\\peace\\Desktop\\video editing tool\\real-time-object-detection\\MobileNetSSD_deploy.caffemodel"
c=0.2

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(p, m)

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()
video = cv2.VideoCapture(0)
frame_width = int(video.get(3)) 
frame_height = int(video.get(4)) 
size = (frame_width, frame_height)
result = cv2.VideoWriter('filename.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 

while (True):
        ret, frame = video.read()
        #if ret == True:
                #result.write(frame)
        frame = imutils.resize(frame, width=400)
        
        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()
        
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with
                # the prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > c:
                        # extract the index of the class label from the
                        # `detections`, then compute the (x, y)-coordinates of
                        # the bounding box for the object
                        idx = int(detections[0, 0, i, 1])
                        if(idx==15):
                                ret, frame = video.read()
                                if ret == True:
                                        result.write(frame)
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")
                        
                        # draw the prediction on the frame
                        label = "{}: {:.2f}%".format(CLASSES[idx],
                                confidence * 100)
                        cv2.rectangle(frame, (startX, startY), (endX, endY),
                                COLORS[idx], 2)
                        y = startY - 15 if startY - 15 > 15 else startY + 15
                        cv2.putText(frame, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

        # update the FPS counter
        fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cv2.destroyAllWindows()
vs.stop()
video.release() 
result.release() 



