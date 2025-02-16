import cv2
import pygame
import numpy as np

# Initialize Pygame for audio playback (if needed for other purposes)
pygame.init()

# Initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Room dimensions and object size in centimeters
room_width = 500  # cm
room_height = 350  # cm
room_depth = 440  # cm
object_diameter = 100  # cm
object_radius = object_diameter / 2  # cm

# Initialize the camera feed
cap = cv2.VideoCapture(0)

def estimate_distance(box_height):
    # Estimate the distance to the person based on the bounding box height
    # This is a simplified approximation assuming the person's height is about 170 cm
    # and the camera is at the same height as the person's head.
    person_height_cm = 170  # Average person height in cm
    focal_length = 615  # Focal length of the camera (this is an approximate value)
    distance_cm = (person_height_cm * focal_length) / box_height
    return distance_cm

def calculate_vibration_intensity(distance):
    if distance < 500:  # Only apply vibration for distances less than 500 cm
        intensity = max(0, 1000 - (distance * 2))  # Simple inverse relationship
        return intensity
    return 0

def main():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to improve processing speed
        frame = cv2.resize(frame, (640, 480))

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect people in the frame
        boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8), padding=(16, 16), scale=1.05)

        # Process detected people
        for (x, y, w, h) in boxes:
            distance_cm = estimate_distance(h)
            
            # Calculate vibration intensity
            vibration_intensity = calculate_vibration_intensity(distance_cm)
            
            # Here you would send the `vibration_intensity` value to your real speaker hardware.
            # This part depends on the specific hardware and interface you're using.
            # For example, you might use GPIO, serial communication, or a specific API.
            print(f'Vibration Intensity: {vibration_intensity} (Distance: {distance_cm:.2f} cm)')

            # Draw rectangles around detected people and display the distance
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f'{distance_cm:.2f} cm', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with annotations
        cv2.imshow('People Detection and Distance Measurement', frame)

        # Exit the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == '__main__':
    main()
