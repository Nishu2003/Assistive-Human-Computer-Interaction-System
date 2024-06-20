import cv2
import numpy as np
import handtrackingmodule as html
import time
import pyautogui
import keyinput
import speech_recognition as sr
import threading 
import SAHVI

############################
wCam, hCam = 640, 488
frameR = 100  # Frame Reduction
smoothening = 6
############################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = html.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()
# print(wScr, hScr)

# Variable to indicate if the program should exit
exit_program = False

# Function to recognize voice command
def recognize_command():
    global exit_program
    recognizer = sr.Recognizer()
    while not exit_program:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print(f"Command: {command}")
            if "exit" in command or "close" in command:
                exit_program = True
        except sr.UnknownValueError:
            print("Could not understand the command.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

# Start voice recognition in a separate thread
voice_thread = threading.Thread(target=recognize_command)
voice_thread.start()

while not exit_program:

    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # 4. Only Index finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:

            # 5. Convert Coordinates

            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
            pyautogui.moveTo(wScr-clocX, clocY)
            cv2.circle(img, (x1, y1), 6, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both Index and Middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:

            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)

            # 10. Click mouse if distance short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 6, (255, 0, 0), cv2.FILLED)
                pyautogui.click()

    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)

if exit_program:
    cap.release()
    cv2.destroyAllWindows()
    SAHVI.main()