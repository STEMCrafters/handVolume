import cv2
import mediapipe as mp
import time, math, os

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

volumeP = -1
sent_value = True

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # print(results.multi_hand_landmarks)#####

    if results.multi_hand_landmarks:
        sent_value = False   ######################################
        lmList = []         # holder for landmark data
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):  #print landmarks
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                lmList.append([id,cx,cy])

            thumbx = lmList[4][1]
            thumby = lmList[4][2]
            indx = lmList[8][1]
            indy = lmList[8][2]

            raw_distance = math.hypot(thumbx - indx, thumby - indy)

            #NEW.....................
            mid_base_x = lmList[9][1]
            mid_base_y = lmList[9][2]
            mid_med_x = lmList[10][1]
            mid_med_y = lmList[10][2]
            calibrate_dist = math.hypot(mid_base_x - mid_med_x, mid_base_y - mid_med_y)
            reference_distance = 72

            if calibrate_dist > reference_distance:
                scale = abs((calibrate_dist-reference_distance)/reference_distance)
                factor = 1-scale
            elif calibrate_dist < reference_distance:
                scale = abs((calibrate_dist-reference_distance)/reference_distance)
                factor = 1+scale
            else:
                factor = 1
            print(factor)

            #------------------------

            distance = raw_distance * (factor**2)


            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            cv2.circle(img,(thumbx,thumby),15,(200,0,0), cv2.FILLED)
            cv2.circle(img, (indx, indy), 15, (200, 0, 0), cv2.FILLED)
            cv2.line(img,(thumbx,thumby),(indx, indy),(200,0,0),3)

            distance = round(distance)
            distance =  max(min(distance, 160), 30)
            volumeP =  round(100*(distance-30)/130)
            cv2.putText(img,f"Distance: {distance}", (50,50),cv2.FONT_HERSHEY_PLAIN,3,(200,0,0),3)
            cv2.putText(img, f"Volume: {volumeP}", (50, 90), cv2.FONT_HERSHEY_PLAIN, 3, (200, 0, 0), 3)

            top = 430 - round(310 * volumeP / 100)
            bottom = 460 - round(310 * volumeP / 100)

            cv2.rectangle(img,(50,120),(85,460),(50,200,50),3)
            cv2.rectangle(img, (50, bottom), (85, top), (50, 200, 50), cv2.FILLED)
    else:
        if sent_value == False:
            print(volumeP)
            os.system('cmd /c "cd C:/Users/Allen/OneDrive - Tech EdVentures/Content/2022/Advanced Coders/Computer Vision/vol/nircmd-x64 & nircmd.exe setsysvolume {}"'.format(round(65535 *volumeP/100)))

            sent_value = not sent_value


    cv2.imshow("Image", img)
    cv2.waitKey(50)

    #media pipe google github mediapipe iris-  callibrate
'''    hands - ---
    checked_hands = true

    no
    hands - --
    if checked_hands == true:
        set
        volume
        checked_hands = false
        
1. threading in Python for key cap
2. look for second hand....       
'''
