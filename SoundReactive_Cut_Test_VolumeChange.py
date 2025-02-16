import datetime
import os
import cv2
import pygame
import mediapipe as mp

# Initialize pygame mixer
pygame.mixer.init(buffer=2048)

# Audio file paths
audio_files = {
    1: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_allSynths_Cut.wav",
    2: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Beats&Bass_Cut.wav",
    3: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Voices_Cut.wav",
    4: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Wind.wav",
    5: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Default.wav",
}

# Play sound function
def play_sound(file_path):
    try:
        print(f"Playing sound: {file_path}")  # Debugging
        if not pygame.mixer.music.get_busy():  # Check if music is not already playing
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(loops=1, fade_ms=2000)
    except Exception as e:
        print(f"Error while playing sound: {e}")

# Stop sound with fade effect
def stop_sound():
    try:
        if pygame.mixer.music.get_busy():
            print("Stopping current sound")
            pygame.mixer.music.fadeout(1000)  # Fade out sound
    except Exception as e:
        print(f"Error while stopping sound: {e}")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Load cascades for face and full-body detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
fullbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Tracking variables
current_people_count = 0
previous_people_count = 0
last_sound_change = datetime.datetime.now()
current_audio_file = ""

# Start playing the default sound initially
current_audio_file = audio_files[5]
play_sound(current_audio_file)

while True:
    ret, img = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert to grayscale for detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
    fullbodies = fullbody_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(40, 80))

    # Detect hands
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    hand_landmarks = result.multi_hand_landmarks
    hand_count = len(hand_landmarks) if hand_landmarks else 0

    # Count total people
    current_people_count = len(faces) + len(fullbodies) + hand_count

    # Change sound based on count
    if current_people_count != previous_people_count and (datetime.datetime.now() - last_sound_change > datetime.timedelta(milliseconds=500)):
        if current_people_count > 0:
            current_audio_file = audio_files.get(min(current_people_count, 5), audio_files[5])
            play_sound(current_audio_file)

        previous_people_count = current_people_count
        last_sound_change = datetime.datetime.now()

    # Draw detections
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    for (x, y, w, h) in fullbodies:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if hand_landmarks:
        for hand_landmark in hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)

    # Display info
    text = f"People: {current_people_count} | Playing: {os.path.basename(current_audio_file) if current_audio_file else 'No sound'}"
    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('img', img)

    # Exit on 'Esc' key
    if cv2.waitKey(30) & 0xFF == 27:
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
pygame.mixer.quit()
