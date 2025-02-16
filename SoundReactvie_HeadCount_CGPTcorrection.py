import cv2
import pygame
import datetime

# Initialize pygame mixer
pygame.mixer.init()

# Function to adjust the volume smoothly
def set_volume(target_count, current_volume):
    target_volume = min(3.0, target_count / 5)  # Normalize count to a max of 5
    step = 0.05  # Smaller step for smoother changes
    if current_volume < target_volume:
        current_volume = min(current_volume + step, target_volume)
    elif current_volume > target_volume:
        current_volume = max(current_volume - step, target_volume)
    print(f"Setting volume to: {current_volume:.2f}")  # Debug statement
    pygame.mixer.music.set_volume(current_volume)
    return current_volume

# Function to stop sound
def stop_sound():
    pygame.mixer.music.stop()

# Function to play sound
def play_sound(audio_file):
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

# Initialize variables
cap = cv2.VideoCapture(0)
head_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
audio_files = {1: "leah4_final.wav", 2: "CLS_all Snyths 1.wav", 3: "CLS_Beats&Bass 1.wav", 4: "CLS_Voices 1.wav", 5: "CLS_Wind.wav"}
current_volume = 0.0
previous_head_count = 0
last_sound_change = datetime.datetime.now()
current_audio_file = ""

while True:
    # Read the frame
    ret, img = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect heads
    heads = head_cascade.detectMultiScale(gray, 1.1, 4)
    current_head_count = len(heads)

    # Check if the number of detected heads has changed
    if current_head_count != previous_head_count and (datetime.datetime.now() - last_sound_change > datetime.timedelta(milliseconds=500)):
        # Smoothly adjust volume based on the number of heads
        current_volume = set_volume(current_head_count, current_volume)

        # Determine which sound to play based on the number of heads
        if current_head_count == 0:
            current_audio_file = ""
            stop_sound()
        elif current_head_count in audio_files:
            current_audio_file = audio_files[current_head_count]
            play_sound(current_audio_file)
        elif current_head_count > 5:
            current_audio_file = audio_files[5]  # Play the "Wind" sound for more than 5 heads
            play_sound(current_audio_file)

        # Update the previous head count
        previous_head_count = current_head_count
        last_sound_change = datetime.datetime.now()

    # Display the output
    for (x, y, w, h) in heads:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the currently playing audio file and the number of detected heads
    if current_audio_file:
        text = f"Heads: {current_head_count} | Playing: {current_audio_file.split('/')[-1]}"
    else:
        text = f"Heads: {current_head_count} | No sound"
    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('Video Feed', img)

    # Stop if escape key is pressed
    if cv2.waitKey(30) & 0xFF == 27:
        break

# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
