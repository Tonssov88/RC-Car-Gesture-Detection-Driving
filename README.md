# RC-Car-Gesture-Detection-Driving

Code for a RC Car that uses a Camera to detect gestures and drive around.
- Uses OpenCV and Mediapipe to detect the hand of a user.
- The number of fingers being held up corresponds to one of five different gestures
1. Forward
2. Backwards
3. Turn Wheels Left
4. Straighten Wheels Out
5. Turn Wheels Right

The RC Car was made by me using:
- A Raspberry PI 4B
- a L298N Motor Driver
- A 12V battery
- A generic USB Camera
- A 9 gram Servo for steering
- A small DC motor
- The chasis and drivetrain of a normal RC Car

An issue I have faced is that the servo jitters a lot and I believe this is due to how the Raspberry Pi software creates PWM signals. There are resources that explain this more in-depth online.
I have attached a video of me using the gesture detection minus the actual movement and a photo of the RC car.
