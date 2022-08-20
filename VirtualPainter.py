import cv2
import numpy as np
import time
import os
import HandTrackerModule as htm

folderPath = "NewHeader"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

folderPath2 = "Size"
myList2 = os.listdir(folderPath2)
print(myList2)
overlayList2 = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

for imPath2 in myList2:
    image2 = cv2.imread(f'{folderPath2}/{imPath2}')
    overlayList2.append(image2)

print(len(overlayList))
print(len(overlayList2))

header = overlayList[0]
drawColor = (255, 255, 255)
size = overlayList2[0]
thickness = 15

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.9)
xp, yp = 0, 0

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

shapesList = []
cntList = []

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList)

        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]


        fingers = detector.fingersUp()
        # print(fingers)


        if fingers[1] and fingers[2] and fingers[0] == False and fingers[3] == False and fingers[4] == False:
            xp, yp = 0, 0
            # print("Selection Mode")

            if y1 < 125:
                if 25 < x1 < 225:
                    header = overlayList[1]
                    drawColor = (0, 0, 0)
                elif 225 < x1 < 425:
                    header = overlayList[5]
                    drawColor = (255, 0, 0)
                elif 425 < x1 < 625:
                    header = overlayList[4]
                    drawColor = (0, 255, 0)
                elif 625 < x1 < 825:
                    header = overlayList[3]
                    drawColor = (200, 50, 255)
                elif 825 < x1 < 1025:
                    header = overlayList[2]
                    drawColor = (0, 0, 255)
                elif 1025 < x1 < 1225:
                    header = overlayList[0]
                    drawColor = (255, 255, 255)

            elif (150 < y1 < 650) and (0 < x1 < 125):
                if 200 < y1 < 300:
                    size = overlayList2[0]
                    thickness = 15
                elif 300 < y1 < 400:
                    size = overlayList2[2]
                    thickness = 25
                elif 400 < y1 < 500:
                    size = overlayList2[3]
                    thickness = 50
                elif 500 < y1 < 600:
                    size = overlayList2[1]
                    thickness = 100

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        if fingers[1] and fingers[2] == False and fingers[0] == False and fingers[3] == False and fingers[4] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            # print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, thickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, thickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, thickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, thickness)

            xp, yp = x1, y1






        if fingers[1] and fingers[2] == False and fingers[0] == False and fingers[3] == False and fingers[4]:
            gray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            ROI_number = 0
            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            for cnt in cnts:
                approx = cv2.approxPolyDP(cnt, 0.1 * cv2.arcLength(cnt, True), True)
                approxSafety = cv2.approxPolyDP(cnt, 0.005 * cv2.arcLength(cnt, True), True)
                # print(len(approx))

                newApprox = []
                newApprox.append(approx)
                cntList.append(cnt)
                # print(cntList)


                length = len(shapesList)
                control = 0
                # print(length)
                if length == 0:
                    shapesList.append(newApprox)
                    shapesList.append(drawColor)
                    cnt2 = cnt
                else:
                    for i in range(int(length/2)):
                        # print("Hi")
                        point = shapesList[-(2*i)]
                        p = point[0]
                        # print(p[0][0][0])
                        if p[0][0][0] == approx[0][0][0]:
                            control += 1
                            break
                    if control == 0:
                        shapesList.append(newApprox)
                        shapesList.append(drawColor)
                        cnt2 = cnt



        if fingers[1] and fingers[2] and fingers[0] == False and fingers[3] == False and fingers[4]:

            if len(shapesList) != 0:

                color = shapesList[-1]
                points = shapesList[-2]
                # print(points)
                # print(points[0])
                newPoints = points[0]

                match len(newPoints):
                    case 2:
                        cv2.drawContours(imgCanvas, [cnt2], 0, (0, 0, 0), -1)
                        cv2.line(img, (newPoints[0][0][0], newPoints[0][0][1]), (newPoints[1][0][0], newPoints[1][0][1]), color,
                                 thickness)
                        cv2.line(imgCanvas, (newPoints[0][0][0], newPoints[0][0][1]), (newPoints[1][0][0], newPoints[1][0][1]),
                                 color, thickness)
                    case 3:
                        cv2.drawContours(imgCanvas, [cnt2], 0, (0, 0, 0), -1)
                        for i in range(2):
                            cv2.line(img, (newPoints[i][0][0], newPoints[i][0][1]),
                                     (newPoints[i + 1][0][0], newPoints[i + 1][0][1]),
                                     color,
                                     thickness)
                            cv2.line(imgCanvas, (newPoints[i][0][0], newPoints[i][0][1]),
                                     (newPoints[i + 1][0][0], newPoints[i + 1][0][1]),
                                     color, thickness)
                        cv2.line(img, (newPoints[2][0][0], newPoints[2][0][1]), (newPoints[0][0][0], newPoints[0][0][1]), color,
                                 thickness)
                        cv2.line(imgCanvas, (newPoints[2][0][0], newPoints[2][0][1]), (newPoints[0][0][0], newPoints[0][0][1]),
                                 color, thickness)
                    case 4:
                        cv2.drawContours(imgCanvas, [cnt2], 0, (0, 0, 0), -1)
                        for i in range(3):
                            cv2.line(img, (newPoints[i][0][0], newPoints[i][0][1]),
                                     (newPoints[i + 1][0][0], newPoints[i + 1][0][1]),
                                     color,
                                     thickness)
                            cv2.line(imgCanvas, (newPoints[i][0][0], newPoints[i][0][1]),
                                     (newPoints[i + 1][0][0], newPoints[i + 1][0][1]),
                                     color, thickness)
                        cv2.line(img, (newPoints[3][0][0], newPoints[3][0][1]), (newPoints[0][0][0], newPoints[0][0][1]), color,
                                 thickness)
                        cv2.line(imgCanvas, (newPoints[3][0][0], newPoints[3][0][1]), (newPoints[0][0][0], newPoints[0][0][1]),
                                 color, thickness)

        if fingers[1] and fingers[2] and fingers[0] == False and fingers[3] and fingers[4]:

            if len(shapesList) != 0:
                listLength = len(shapesList)
                for k in range(len(cntList)):
                    cv2.drawContours(imgCanvas, [cntList[k]], 0, (0, 0, 0), -1)
                for x in range(int(listLength / 2)):
                    color = shapesList[2 * x - 1]
                    points = shapesList[2 * x - 2]
                    newPoints = points[0]
                    match len(newPoints):
                        case 2:
                            cv2.line(img, (newPoints[0][0][0], newPoints[0][0][1]),
                                     (newPoints[1][0][0], newPoints[1][0][1]), color,
                                     thickness)
                            cv2.line(imgCanvas, (newPoints[0][0][0], newPoints[0][0][1]),
                                     (newPoints[1][0][0], newPoints[1][0][1]),
                                     color, thickness)
                        case 3:
                            for i in range(2):
                                cv2.line(img, (newPoints[i][0][0], newPoints[i][0][1]),
                                         (newPoints[i + 1][0][0], newPoints[i + 1][0][1]),
                                         color,
                                         thickness)
                                cv2.line(imgCanvas, (newPoints[i][0][0], newPoints[i][0][1]),
                                         (newPoints[i + 1][0][0], newPoints[i + 1][0][1]),
                                         color, thickness)
                            cv2.line(img, (newPoints[2][0][0], newPoints[2][0][1]),
                                     (newPoints[0][0][0], newPoints[0][0][1]), color,
                                     thickness)
                            cv2.line(imgCanvas, (newPoints[2][0][0], newPoints[2][0][1]),
                                     (newPoints[0][0][0], newPoints[0][0][1]),
                                     color, thickness)
                        case 4:
                            for i in range(3):
                                cv2.line(img, (newPoints[i][0][0], newPoints[i][0][1]),
                                         (newPoints[i + 1][0][0], newPoints[i + 1][0][1]),
                                         color,
                                         thickness)
                                cv2.line(imgCanvas, (newPoints[i][0][0], newPoints[i][0][1]),
                                         (newPoints[i + 1][0][0], newPoints[i + 1][0][1]),
                                         color, thickness)
                            cv2.line(img, (newPoints[3][0][0], newPoints[3][0][1]),
                                     (newPoints[0][0][0], newPoints[0][0][1]), color,
                                     thickness)
                            cv2.line(imgCanvas, (newPoints[3][0][0], newPoints[3][0][1]),
                                     (newPoints[0][0][0], newPoints[0][0][1]),
                                     color, thickness)



    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)


    img[0:125, 0:1280] = header
    img[150:650, 0:125] = size
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)
