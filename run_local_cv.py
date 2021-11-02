# Run this file on CV2 in local machine to construct a Concentration Index (CI).
# Video image will show emotion on first line, and engagement on second. Engagement/concentration classification displays either 'Pay attention', 'You are engaged' and 'you are highly engaged' based on CI. Webcam is required.
# Analysis is in 'Util' folder.


from util.analysis_realtime import analysis
from  opencv_plot import Plotter
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Initializing
global ci
cap = cv2.VideoCapture(0)
ana = analysis()
#concentration over time
cot = []
# x looking direction over time
xot = []
# emotion over time
eot = []
# summation of concentration over time
sot = []
# eye looking direction over time
eyeot = []
p = Plotter(640,100 )
q = Plotter(640,100)
i = 0
font = cv2.FONT_HERSHEY_SIMPLEX

# Capture every frame and send to detector
while True:
    _, frame = cap.read()
    bm = ana.detect_face(frame)
    sloped = sum(cot[-25:])
    p.plot(sloped*4)
    x = p.plot_canvas
    cv2.imshow("x", x)
    cv2.imshow("Frame2", frame)
    cot.append(bm)
    eyeot.append(ana.size)
    eot.append(ana.emotion)
    xot.append(ana.x)
    sot.append(sloped)
    if i > 25 and len(cot) > 50: 
        # Pausing condition
        if int(sum(cot[-25:])) < 12.5 and sot[len(sot)-1] <= sot[len(sot)-2]:
            left = 0
            right = 0 
            eye = 0
            emotion = np.zeros(6)
            counter = 0
            plot_canvas = np.ones((200, 1200, 3))*255
            #determining why the video paused
            for val in eot[-25:]: 
                emotion[val] = emotion[val] + 1
            for val in xot[-25:]:
                if val < 0.6: 
                    right= right + 1
                elif val > 2:
                    left = left + 1  
            for val in eyeot[-25:]:
                if val < 0.20:
                    eye = eye+ 1
                    
                    
            message = "You seem distracted! continue y/n" 
            pemotions = {0: 'Angry', 1: 'Fear', 2: 'Happy',
                        3: 'Sad', 4: 'Surprised', 5: 'Neutral'}
            s = 0
            while s < 5:
                if emotion[s] > 15:
                    message = "you seem {}".format(pemotions[s])
                    counter = 1
                s+=1
            if left > 15: 
                message = "you looked to the left"  
            elif right > 15: 
                message = "you looked to the right"
            elif eye > 15:
                message ="youre eyes where closed"
            elif counter == 1:
                key = cv2.waitKey(1)
     
            cv2.putText(plot_canvas, message,
                        (50, 150), font, 2, (0, 0, 255), 3)
            cv2.imshow("ds", plot_canvas)
            key2 = cv2.waitKey(1000000)
            if key2 == ord('n'):
        
                break
            if key2 == ord('y'):
        
                i = 0
                cv2.destroyWindow("ds")
    else:
        i=i+1
    
    key = cv2.waitKey(1)
# Exit if 'q' is pressed
    if key == ord('q'):
        
        break

# Release the memoryq
cap.release()
cv2.destroyAllWindows()
#end report
report_canvas = np.ones((1000, 1000, 3))*255
emotion2 = np.zeros(6)
rleft = 0
rright = 0
rmiddle = 0 
cv2.putText(report_canvas, "Your average Ci was {:.2f}".format(sum(cot)/len(cot)),
                        (50, 50), font, 2, (0, 0, 255), 3)
cv2.putText(report_canvas, "This is based on: ",
                        (50, 150), font, 2, (0, 0, 255), 3)
for val in eot: 
                emotion2[val] = emotion2[val] + 1
cv2.putText(report_canvas, "neutral = {:.2f}%".format(emotion2[5]/len(eot)* 100),
                        (50, 250), font, 2, (0, 0, 255), 3)
cv2.putText(report_canvas, "sad = {:.2f}%".format(emotion2[3]/len(eot)* 100),
                        (50, 300), font, 2, (0, 0, 255), 3)
cv2.putText(report_canvas, "angry = {:.2f}%".format(emotion2[0]/len(eot)* 100),
                        (50, 350), font, 2, (0, 0, 255), 3)
cv2.putText(report_canvas, "fear = {:.2f}%".format(emotion2[1]/len(eot)* 100),
                        (50, 400), font, 2, (0, 0, 255), 3)
cv2.putText(report_canvas, "happy = {:.2f}%".format(emotion2[2]/len(eot)* 100),
                        (50, 450), font, 2, (0, 0, 255), 3)
cv2.putText(report_canvas, "suprised = {:.2f}%".format(emotion2[4]/len(eot)* 100),
                        (50, 500), font, 2, (0, 0, 255), 3)
for val in xot: 
    if val < 0.6: 
        rleft= rleft + 1
    elif val > 1.5:
        rright = rright + 1 
    else:
        rmiddle = rmiddle + 1
cv2.putText(report_canvas, "left = {:.2f}%".format(rleft/len(xot)* 100),
                        (50, 600), font, 2, (0, 0, 255), 3)
cv2.putText(report_canvas, "middle = {:.2f}%".format(rmiddle/len(xot)* 100),
                        (50, 650), font, 2, (0, 0, 255), 3)
cv2.putText(report_canvas, "rright = {:.2f}%".format(rright/len(xot)* 100),
                        (50, 700), font, 2, (0, 0, 255), 3)
    
cv2.imshow("report", report_canvas)

while True:
    key = cv2.waitKey(1)
# Exit if 'q' is pressed
    if key == ord('q'):
    
        break
cv2.destroyAllWindows()

	
