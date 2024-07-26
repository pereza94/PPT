from random import random
from sre_constants import SUCCESS
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

# for index in range(0, 10):
#     cap = cv2.VideoCapture(index)
#     if cap.isOpened():
#         print(f"Camera index available: {index}")
#         cap.release()
#     else:
#         print(f"Camera index not available: {index}")


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0]
jugando = False

while True:
    print("paso 1")
    imgBG = cv2.imread('Resources/pantalla_juego.jpg')
    SUCCESS, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]
    imgBG[234:654, 795:1195] = imgScaled

    # find hands
    hands, img = detector.findHands(imgScaled)

    try:
        print("paso 3")
        if startGame:
            print("paso 4")
            if stateResult is False:
                print("paso 5")
                timer = time.time() - initialTime
                time_cd = 3 - int(timer)

                cv2.putText(imgBG, str(int(time_cd)), (605,435),cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

                if timer > 4:
                    stateResult = True
                    timer = 0

                    if hands:
                        playerMove = None
                        hand = hands[0]
                        jugada = ""
                        fingers = detector.fingersUp(hand)
                        print(fingers)
                        if fingers == [0, 0, 0, 0, 0] or sum(fingers) <= 1:
                            playerMove = 1
                            jugada = "piedra"
                        elif fingers == [1, 1, 1, 1, 1] or sum(fingers) > 4:
                            playerMove = 2
                            jugada = "papel"
                        elif fingers == [0, 1, 1, 0, 0] or (fingers[3] == 0 and fingers[4] == 0):
                            playerMove = 3
                            jugada = "tijera"

                        randomNumber = random.randint(1, 3)

                        imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 240))

                        # Player wins
                        if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                            scores[1] += 1

                        # AI wins
                        if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                            scores[0] += 1

            if stateResult:
                start_time = time.time()
                while time.time() - start_time < 2:
                    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 225, 255), 6)
                    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 225, 255), 6)
                    cv2.putText(imgBG, jugada, (920, 710), cv2.FONT_HERSHEY_PLAIN, 4, (53, 67, 203), 6)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 240))
                    cv2.imshow('FCyT Piedra/Papel/Tijera', imgBG)
                    cv2.putText(imgBG, jugada, (920, 710), cv2.FONT_HERSHEY_PLAIN, 4, (53, 67, 203), 6)
                    cv2.waitKey(1000)

                if time.time() - start_time > 2:
                    initialTime = time.time()
                    stateResult = False
                    jugando = True

            cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 225, 255), 6)
            cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 225, 255), 6)

            if scores[0] == 3:
                start_time = time.time()
                while time.time() - start_time < 2:
                    cv2.putText(imgBG, "Gano", (180, 570), cv2.FONT_HERSHEY_PLAIN, 4, (53, 67, 203), 6)
                    cv2.putText(imgBG, "PC", (180, 620), cv2.FONT_HERSHEY_PLAIN, 4, (53, 67, 203), 6)
                    cv2.imshow('FCyT Piedra/Papel/Tijera', imgBG)
                    cv2.waitKey(2000)
            elif scores[1] == 3:
                start_time = time.time()
                while time.time() - start_time < 2:
                    cv2.putText(imgBG, "Gano", (180, 570), cv2.FONT_HERSHEY_PLAIN, 4, (53, 67, 203), 6)
                    cv2.putText(imgBG, "Humano", (180, 620), cv2.FONT_HERSHEY_PLAIN, 4, (53, 67, 203), 6)
                    cv2.imshow('FCyT Piedra/Papel/Tijera', imgBG)
                    cv2.waitKey(2000)
                cv2.waitKey(2000)

            if scores[0] == 3 or scores[1] == 3:
                scores = [0, 0]
                startGame = False

        imgBG[234:654, 795:1195] = imgScaled

    except:
        pass


    cv2.imshow('FCyT Piedra/Papel/Tijera', imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
        jugando = True
        print("paso 2")
        if scores[0] == 3 or scores[1] == 3:
            scores = [0, 0]
            jugando = False
    if key == ord('q'):
        cv2.destroyAllWindows()
        break
