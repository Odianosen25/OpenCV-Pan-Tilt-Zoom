import numpy as np
import cv2
import imutils


cap = cv2.VideoCapture(0)
ret, frame = cap.read() # Initializing the video frame
# setting width & height of the video frame
width = frame.shape[1] 
height = frame.shape[0]
zoom = 1

def nothing(x):
    pass

def zoom_changed_state(z):
    global zoom
    z = 1 if z <= 0 else z

    # first get present state
    x = cv2.getTrackbarPos('X','frame')
    y = cv2.getTrackbarPos('Y','frame')

    scale = z/zoom
    x = int(x * scale)
    y = int(y * scale)
    cv2.setTrackbarPos('X','frame', x)
    cv2.setTrackbarPos('Y','frame', y)
    zoom = z

def Zoom(cv2Object, point, zoomSize):
    # Resizes the image/video frame to the specified amount of "zoomSize".
    # A zoomSize of "2", for example, will double the canvas size
    cv2Object = imutils.resize(cv2Object, width=(zoomSize * cv2Object.shape[1]))
    # center is simply half of the height & width (y/2,x/2)
    center = (int(cv2Object.shape[0]/2),int(cv2Object.shape[1]/2))
    # cropScale represents the top left corner of the cropped frame (y/x)
    cropScale = (int(center[0]/zoomSize), int(center[1]/zoomSize))

    dx = point[0] - center[1]
    dy = point[1] - center[0]

    cv2Object = imutils.translate(cv2Object, dx, dy)
    # The image/video frame is cropped to the center with a size of the original picture
    # image[y1:y2,x1:x2] is used to iterate and grab a portion of an image
    # (y1,x1) is the top left corner and (y2,x1) is the bottom right corner of new cropped frame.
    cv2Object = cv2Object[0:(center[0] + cropScale[0]), 0:(center[1] + cropScale[1])]
    cv2Object = imutils.resize(cv2Object, width=width)

    (h, w) = cv2Object.shape[:2]
    #print(h, w)
    return cv2Object

cv2.namedWindow("frame")
cv2.createTrackbar('Zoom','frame', 1, 10, zoom_changed_state)
cv2.createTrackbar('X','frame', 1, width*2, nothing)
cv2.createTrackbar('Y','frame', 1, height*2, nothing)
cv2.setTrackbarPos('X','frame', int(width/2))
cv2.setTrackbarPos('Y','frame', int(height/2))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    (h, w) = frame.shape[:2]
    #print(f"orignal {h} {w}")

    x = cv2.getTrackbarPos('X','frame')
    y = cv2.getTrackbarPos('Y','frame')

    frame = Zoom(frame, (x, y), zoom)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releasing the capture
cv2.imwrite("CanvasTest12.png", frame)
cap.release()
cv2.destroyAllWindows()
