import datetime
import os
import cv2
import pygame
import mediapipe as mp

# Initialize the pygame mixer
pygame.mixer.init(buffer=2048)

# Correct paths for the audio files
audio_files = {
    1: "/Users/jeainpyo/Desktop/AnnaSound/Loslassen.wav",
}

# Function to play a sound with volume control
def play_sound(file_path, volume):
    print(f"Playing sound: {file_path} at volume: {volume}")  # Debug statement
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.set_volume(volume)  # Adjust volume dynamically
    else:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops=1, fade_ms=2000)

# Function to stop sound with fading effect
def stop_sound():
    if pygame.mixer.music.get_busy():
        print("Stopping current sound")  # Debug statement
        pygame.mixer.music.fadeout(1000)

# Initialize the mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Load the cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
fullbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# Open the webcam
cap = cv2.VideoCapture(0)

# Variables to keep track of detected people
current_people_count = 0
previous_people_count = 0
last_sound_change = datetime.datetime.now()
current_audio_file = ""

while True:
    # Read the frame
    _, img = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Detect full bodies
    fullbodies = fullbody_cascade.detectMultiScale(gray, 1.1, 4)

    # Detect hands
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    hand_landmarks = result.multi_hand_landmarks

    # Count the number of hands detected
    hand_count = len(hand_landmarks) if hand_landmarks else 0

    # Update the current people count
    current_people_count = len(faces) + len(fullbodies) + hand_count

    # Check if the number of detected people has changed
    if current_people_count != previous_people_count and (datetime.datetime.now() - last_sound_change > datetime.timedelta(milliseconds=500)):

        # Set volume based on the number of people detected
        max_people = 10  # Adjusting max count for finer control
        volume = min(1.0, max(0.1, current_people_count / max_people))  # Normalize volume from 0.1 to 1.0

        # Determine which sound to play based on the number of people
        if current_people_count == 0:
            current_audio_file = ""
            stop_sound()
        elif current_people_count in audio_files:
            current_audio_file = audio_files[current_people_count]
            play_sound(current_audio_file, volume)
        else:
            current_audio_file = audio_files[1]  # Default to one file
            play_sound(current_audio_file, volume)

        # Update previous count
        previous_people_count = current_people_count
        last_sound_change = datetime.datetime.now()

    # Display the output
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    for (x, y, w, h) in fullbodies:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    if hand_landmarks:
        for hand_landmark in hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)

    # Display the currently playing audio file and volume level
    if current_audio_file:
        text = f"People: {current_people_count} | Volume: {volume:.2f} | Playing: {os.path.basename(current_audio_file)}"
    else:
        text = f"People: {current_people_count} | No sound"
    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('img', img)

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
