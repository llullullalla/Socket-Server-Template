import datetime
import os
import cv2
import pygame
import mediapipe as mp

# Initialize pygame mixer with pre-init to avoid potential waitpid issues
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Correct paths for the audio files
audio_files = {
    1: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Wind.wav",
    2: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Voices_Cut.wav",
    3: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Beats&Bass_Cut.wav",
    4: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_allSynths_Cut.wav",
    7: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Overcrowded.wav"  # Added fallback for >6 people
}

# Function to play a sound with fading effect
def play_sound(file_path):
    print(f"Playing sound: {file_path}")  # Debug statement
    if pygame.mixer.music.get_busy():
        queue_sound(file_path)
    else:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(loops=1, fade_ms=2000)

def queue_sound(file_path):
    pygame.mixer.music.queue(file_path)  # Removed `loops=1` (not supported)

# Function to stop sound with fading effect
def stop_sound():
    if pygame.mixer.music.get_busy():
        print("Stopping current sound")  # Debug statement
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()  # Ensures the sound actually stops

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Load OpenCV cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
fullbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# Open the webcam
cap = cv2.VideoCapture(0)

# Variables to keep track of the current and previous number of detected people
current_people_count = 0
previous_people_count = 0
last_sound_change = datetime.datetime.now()
current_audio_file = ""

while True:
    # Read the frame
    ret, img = cap.read()
    if not ret:
        break  # Exit if the camera fails

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces and full bodies
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    fullbodies = fullbody_cascade.detectMultiScale(gray, 1.1, 4)

    # Detect hands
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    hand_landmarks = result.multi_hand_landmarks
    hand_count = len(hand_landmarks) if hand_landmarks else 0

    # Update the current people count
    current_people_count = len(faces) + len(fullbodies) + hand_count

    # Ensure minimum time interval between sound changes (500ms)
    if (current_people_count != previous_people_count and 
        (datetime.datetime.now() - last_sound_change > datetime.timedelta(milliseconds=500))):

        # Determine which sound to play based on the number of people
        if current_people_count == 0:
            stop_sound()
            current_audio_file = ""
        else:
            sound_key = min(current_people_count, max(audio_files.keys()))  # Ensure valid key
            current_audio_file = audio_files.get(sound_key, "")
            if current_audio_file:
                play_sound(current_audio_file)

        # Update tracking variables
        previous_people_count = current_people_count
        last_sound_change = datetime.datetime.now()

    # Display detection results
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    for (x, y, w, h) in fullbodies:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    if hand_landmarks:
        for hand_landmark in hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)

    # Display the currently playing audio file and the number of detected people
    text = f"People: {current_people_count} | Playing: {os.path.basename(current_audio_file) if current_audio_file else 'No sound'}"
    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('img', img)

    # Stop if escape key is pressed
    if cv2.waitKey(30) & 0xff == 27:
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
