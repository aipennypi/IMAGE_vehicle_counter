<h2>Vehicle Counting System using OpenCV and Dlib</h2>
This project is designed to count vehicles entering and exiting a predefined region in a video. The system utilizes computer vision techniques such as background subtraction, contour detection, and object tracking to detect and track vehicles. This is particularly useful for traffic monitoring and analysis.

<h2>Step-by-Step Process</h2>
Background Subtraction:

A background subtractor is used to separate moving objects (vehicles) from the background.
Contour Detection:

Detects the contours of moving objects in the frame.
Object Tracking:

Vehicles are tracked using dlib.correlation_tracker to ensure consistent counting even if the vehicle is partially occluded.
Counting Logic:

Vehicles are counted as "IN" or "OUT" based on their position in the frame relative to a threshold line.
Frame Updates:

Updates the positions of tracked objects and removes trackers for objects that leave the region of interest or have poor tracking quality.

<h2>Outputs</h2>
Visual Feedback:

Bounding boxes around detected vehicles.
Vehicle counts displayed on the video (IN and OUT).
Logs:

Real-time vehicle counts are displayed in the console for debugging.
