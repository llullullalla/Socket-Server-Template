from gpiozero import MotionSensor

pir = MotionSensor(4) # out plugged into GPIO12
while True:
    if pir.motion_detected:
        print("Human deactivated...")
