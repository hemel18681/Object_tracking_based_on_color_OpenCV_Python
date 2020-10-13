
#BGR to HSV , HSV - hue saturation value / can easily compare
#minimum enclosing circle - minimum possible circle for the object area
#moments to find center of the area - objects center
#drawing circle - draw the minimum enclosing circle
#block diagram: reading from camera -> pre-processing image -> finding counters -> drawing minimum enclosing circle
# -> finding center of counter area -> drawing circle and center -> direction based on radius and position
#179,253,81

import imutils #resizing
import cv2 #camera

#(hue,saturation,value)
lower = (0,0,0)      #hsv value
upper = (179,255,91) #hsv value

camera = cv2.VideoCapture(0)

while True:
    (grabbed,frame) = camera.read()
    frame = imutils.resize(frame , width=600)
    blurred = cv2.GaussianBlur(frame,(11,11),0)
    hsv = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

    #mask only the object color thar I want to track
    mask = cv2.inRange(hsv, lower, upper) #assign color
    mask = cv2.erode(mask,None,iterations=2) #erotion , to remove the noise
    mask = cv2.dilate(mask, None, iterations=2) #dilation , to remove the noise

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] #how much presence of the color
    center = None
    if len(cnts)>0:
        #max contour area/ max object area
        c = max(cnts,key=cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(c) #obtain the center and radius
        M = cv2.moments(c)
        #center co-ordinate
        center = (int (M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        if radius >10:
            #make the circle and draw
            cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
            #draw centroid
            cv2.circle(frame,center,5,(0,0,255),-1)
            print(center[0],radius)
            if radius > 250:
                print("stop")
            else:
                if center[0]<150:
                    print("Left")
                elif center[0]>450:
                    print("Right")
                elif radius < 250:
                    print("Front")
                else:
                    print("Stop")
        #show original frame
        cv2.imshow("Frame",frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
camera.release()
cv2.destroyAllWindows()