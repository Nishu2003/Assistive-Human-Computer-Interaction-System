import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import threading
import SAHVI

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

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

    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
    
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
    
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)
    
        left = [landmarks[145], landmarks[159]]
    
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
    
        if (left[0].y - left[1].y) < 0.004:
            pyautogui.click()
            pyautogui.sleep(1)
            
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)

if exit_program:
    cam.release()
    cv2.destroyAllWindows()
    SAHVI.main()