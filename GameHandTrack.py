import cv2
import time
import handtrackingmodule as htm
import threading
import speech_recognition as sr
import SAHVI

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

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
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        print(lmList[4])

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

if exit_program:
    cap.release()
    cv2.destroyAllWindows()
    SAHVI.main()