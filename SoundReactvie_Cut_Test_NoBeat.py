# headcount in volume

import datetime
import os

import cv2
import pygame
import mediapipe as mp

# Initialize the pygame mixer
pygame.mixer.init(buffer=2048)

# Correct paths for the audio files
audio_files = {
    1: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_allSynths_Cut.wav",
    3: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Voices_Cut.wav",
    4: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Wind.wav",
}

# Verify that all audio files exist
for key, path in audio_files.items():
    if not os.path.exists(path):
        print(f"Audio file not found for key {key}: {path}")

# Function to play a sound with fading effect
def play_sound(file_path):
    print(f"Playing sound: {file_path}")  # Debug statement
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.queue(file_path)
    else:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(loops=1, fade_ms=2000)

# Function to adjust volume based on head count
def adjust_volume(head_count):
    volume = min(1.0, head_count / 4.0)  # Scale volume between 0 and 1.0
    pygame.mixer.music.set_volume(volume)
    print(f"Adjusted volume to: {volume}")

# Initialize the mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Load the cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the webcam
cap = cv2.VideoCapture(0)

# Variables to keep track of the current and previous number of detected heads
current_head_count = 0
previous_head_count = 0
last_sound_change = datetime.datetime.now()
current_audio_file = ""

def process_frame():
    global current_head_count, previous_head_count, last_sound_change, current_audio_file

    ret, img = cap.read()
    if not ret:
        print("Failed to read from camera. Exiting...")
        return False

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Update the current head count
    current_head_count = len(faces)

    # Check if the number of detected heads has changed
    if current_head_count != previous_head_count and (
        datetime.datetime.now() - last_sound_change > datetime.timedelta(milliseconds=500)
    ):

        # Determine which sound to play based on the number of heads
        if current_head_count in audio_files:
            current_audio_file = audio_files[current_head_count]
            play_sound(current_audio_file)
        elif current_head_count > 4:
            current_audio_file = audio_files[4]
            play_sound(current_audio_file)

        # Adjust the volume based on the head count
        adjust_volume(current_head_count)

        # Update the previous head count
        previous_head_count = current_head_count
        last_sound_change = datetime.datetime.now()

    # Display the output
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the currently playing audio file and the number of detected heads
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (400, 50), (0, 0, 0), -1)
    img = cv2.addWeighted(overlay, 0.5, img, 0.5, 0)

    if current_audio_file:
        text = f"Heads: {current_head_count} | Playing: {os.path.basename(current_audio_file)}"
    else:
        text = f"Heads: {current_head_count} | No sound"
    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('img', img)
    return True

try:
    while True:
        # Always continue processing the frame
        process_frame()

        # Stop if escape key is pressed
        if cv2.waitKey(30) & 0xFF == 27:
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()
