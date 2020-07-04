import numpy as np
import cv2


#cap = cv2.VideoCapture("http://208.72.70.171:80/mjpg/video.mjpg")
cap = cv2.VideoCapture(0)
ret, frame = cap.read() # Initializing the video frame
# setting width & height of the video frame
width = frame.shape[1] 
height = frame.shape[0]
zoom = 1
frame_center = (int(height/2), int(width/2))

def nothing(x):
    pass

def translate(image, x, y, w, h):
    # define the translation matrix and perform the translation
    M = np.float32([[1, 0, x], [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (w, h))

    # return the translated image
    return shifted

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

def Zoom(cv2Object, point, zoomSize, res):
    # Resizes the image/video frame to the specified amount of "zoomSize".
    # A zoomSize of "2", for example, will double the canvas size
    newh = zoomSize * res[0]
    neww = zoomSize * res[1]
    cv2Object = cv2.resize(cv2Object, (neww, newh), interpolation=cv2.INTER_AREA)
    # center is simply half of the height & width (y/2,x/2)
    center = (int(newh/2),int(neww/2))
    # cropScale represents the top left corner of the cropped frame (y/x)
    cropScale = (int(center[0]/zoomSize), int(center[1]/zoomSize))

    dx = point[0] - center[1]
    dy = point[1] - center[0]

    if dx > 0:
        dx = 0

    if dy > 0:
        dy = 0

    scale = zoomSize - 1
    scale = scale * -1

    if dx < 0:
        if zoomSize > 1:
            if (frame_center[1] * scale) > dx:
                dx = frame_center[1] * scale
        
        elif dx != 0:
            dx = 0

    if dy < 0:
        if zoomSize > 1:
            if (frame_center[0] * scale) > dy:
                dy = frame_center[0] * scale
        
        elif dy != 0:
            dy = 0

    cv2Object = translate(cv2Object, dx, dy, neww, newh)
    # The image/video frame is cropped to the center with a size of the original picture
    # image[y1:y2,x1:x2] is used to iterate and grab a portion of an image
    # (y1,x1) is the top left corner and (y2,x1) is the bottom right corner of new cropped frame.
    cv2Object = cv2.UMat.get(cv2Object)
    cv2Object = cv2Object[0:(center[0] + cropScale[0]), 0:(center[1] + cropScale[1])]
    cv2Object = cv2.resize(cv2Object, (width, height), interpolation=cv2.INTER_AREA)

    #print(h, w)
    return cv2Object

cv2.namedWindow("frame")
cv2.createTrackbar('Zoom','frame', 1, 4, zoom_changed_state)
cv2.createTrackbar('X','frame', 1, width*2, nothing)
cv2.createTrackbar('Y','frame', 1, height*2, nothing)
cv2.setTrackbarPos('X','frame', int(width/2))
cv2.setTrackbarPos('Y','frame', int(height/2))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    res = frame.shape[:2]
    #print(f"orignal {h} {w}")

    x = cv2.getTrackbarPos('X','frame')
    y = cv2.getTrackbarPos('Y','frame')

    uframe = cv2.UMat(frame) # move to gpu
    frame = Zoom(uframe, (x, y), zoom, res)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releasing the capture
cap.release()
cv2.destroyAllWindows()
