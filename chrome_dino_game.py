import numpy as np
import cv2
from mss import mss

from pynput.keyboard import Key, Controller
from time import sleep
keyboard = Controller()

bounding_box = {'top': 140, 'left': 790, 'width': 300, 'height': 210} #specifying area to capture
#specifying area to watch from the captured stream
x1,y1=75,120
x2,y2=120,175
sct = mss()
sum_perv=0
while True:
    sct_img = sct.grab(bounding_box)  #capture the area specified
    screen_array=np.array(sct_img) #convert the captured stream to numpy array
    gray_sc=cv2.cvtColor(screen_array,cv2.COLOR_RGB2GRAY)   # converting the array to grayscale(two dimensional)
    
    box_array=gray_sc[y1:y2,x1:x2] #slicing and creating a matrix within the box drawn
    box_array=cv2.bitwise_not(box_array) #inverting the color
    cv2.imshow('box',box_array) # display the box area only
    sum= np.sum(box_array) #obtain sum of all the elements in the box array
    if sum >38000:     #setting the threshold; obstacle inside the box returns higher value
        #sleep(0.08)
        print('activation = '+str(sum)) 
        #simulate the key press                                                                                                                                                                                                                                                                                
        keyboard.press(Key.space)                                                                                                                                        
        keyboard.release(Key.space)

    img=cv2.rectangle(gray_sc, (x1,y1), (x2,y2), (0,255,0),1) #drawing rectangle for obstacle detection
    cv2.imshow('screen', img) #displaying the captured stream with a rectangle overlay
    
    if (cv2.waitKey(1) & 0xFF) == 27: #waiting to press ESC
        cv2.destroyAllWindows()
        break