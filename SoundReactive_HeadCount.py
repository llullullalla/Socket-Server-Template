import datetime
import cv2
import pygame

# Initialize the pygame mixer
pygame.mixer.init(buffer=2048)

# Correct paths for the audio files
audio_files = {
    1: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_allSynths_Cut.wav",
    2: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Beats&Bass_Cut.wav",
    3: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Voices_Cut.wav",
    4: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Wind.wav",
    7: "/Users/jeainpyo/Desktop/AnnaSoundCutShort/CLS_Overcrowded.wav"  # Added fallback for >6 people
}

# Function to play a sound with fading effect
def play_sound(file_path):
    print(f"Playing sound: {file_path}")  # Debug statement
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(loops=1, fade_ms=2000)

# Function to stop sound with fading effect
def stop_sound():
    if pygame.mixer.music.get_busy():
        print("Stopping current sound")  # Debug statement
        pygame.mixer.music.fadeout(1000)

# Function to adjust the volume
def set_volume(count):
    volume = min(3.0, count / 5)  # Normalize count to a max of 5
    print(f"Setting volume to: {volume}")  # Debug statement
    pygame.mixer.music.set_volume(volume)

# Load the head (upper body) cascade
head_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')

# Open the webcam (default camera)
cap = cv2.VideoCapture(0)

# Verify if the video capture is successful
if not cap.isOpened():
    print("Error: Could not access the camera")
    exit()

# Variables to keep track of the current and previous number of detected heads
current_head_count = 0
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
        # Adjust volume based on the number of heads
        set_volume(current_head_count)

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
