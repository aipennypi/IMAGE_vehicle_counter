import cv2
import dlib
import os


# Function to find the center of a rectangle
def findCenter(x, y, w, h):
    cx = int((x + w) / 2)
    cy = int((y + h) / 2)
    return cx, cy


# Function to check if a point is inside a rectangle
def pointInRect(x, y, w, h, cx, cy):
    x1, y1 = cx, cy
    if (x < x1 and x1 < x + w):
        if (y < y1 and y1 < y + h):
            return True
    else:
        return False


# Main function
def main():
    # Open the video file
    # add file path
    cap = cv2.VideoCapture('car.mp4')

    # Create background subtractor
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    # Initialize counters and constants
    count = 0
    SKIP_FRAMES = 10  # Number of frames to skip for detection
    trackers = []  # List to store trackers
    cars_in = 0  # Counter for cars entering
    cars_out = 0  # Counter for cars exiting
    Font = cv2.FONT_HERSHEY_COMPLEX_SMALL  # Font for text overlay

    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Failed to capture frame. Exiting...")
            break

        # Resize frame to a fixed size
        frame_r = cv2.resize(frame, (640, 480))

        # Crop a region of interest
        frame_cropped = frame_r[200:640, 0:640]
        cv2.imshow('cropped', frame_cropped)

        # Apply background subtraction
        fgmask_r = fgbg.apply(frame_cropped)

        # Dilate the mask to fill holes
        fgmask_r = cv2.dilate(fgmask_r, (9, 9), 2)
        cv2.imshow('fgmask', fgmask_r)

        # Find contours of the objects in the mask
        contours, h = cv2.findContours(fgmask_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Remove trackers with poor quality
        trackers_to_del = []
        for tid, trackersid in enumerate(trackers):
            trackingQuality = trackersid[0].update(frame_cropped)
            if trackingQuality < 5:
                trackers_to_del.append(trackersid[0])
        try:
            for trackersid in trackers_to_del:
                trackers.pop(tid)
        except IndexError:
            pass

        # Perform object detection every SKIP_FRAMES frames
        if (count % SKIP_FRAMES) == 0:
            for num, cnt in enumerate(contours):
                area = cv2.contourArea(cnt)
                if area in range(400, 8000):  # Filter by area size
                    x, y, w, h = cv2.boundingRect(cnt)
                    rect = dlib.rectangle(x, y, x + w, y + h)
                    tracking = False

                    # Check if the object is already being tracked
                    for trackersid in trackers:
                        pos = trackersid[0].get_position()
                        startX = int(pos.left())
                        startY = int(pos.top())
                        endX = int(pos.right())
                        endY = int(pos.bottom())
                        tx, ty = findCenter(startX, startY, endX, endY)
                        t_location_chk = pointInRect(x, y, w, h, tx, ty)
                        if t_location_chk:
                            tracking = True

                    # If not being tracked, start a new tracker
                    if not tracking:
                        tracker = dlib.correlation_tracker()
                        tracker.start_track(frame_cropped, rect)
                        trackers.append([tracker, frame_cropped])

        # Update positions of trackers and count cars
        for num, trackersid in enumerate(trackers):
            pos = trackersid[0].get_position()
            startX = int(pos.left())
            startY = int(pos.top())
            endX = int(pos.right())
            endY = int(pos.bottom())
            offset = 0
            cv2.rectangle(frame_cropped, (startX - offset, startY - offset),
                          (endX + offset, endY + offset), (0, 255, 250), 1)

            # Count cars entering
            if endX < 320 and endY >= 280:
                cars_in += 1
                trackers.pop(num)

            # Count cars exiting
            if endX > 320 and startY < 0:
                cars_out += 1
                trackers.pop(num)

        # Increment frame count
        count += 1

        # Display car counts on the frame
        cv2.putText(frame_r, f"IN:{cars_in}",
                    (20, 40), Font, 1, (255, 0, 0), 1)
        cv2.putText(frame_r, f"OUT:{cars_out}",
                    (550, 40), Font, 1, (255, 0, 0), 1)

        # Display the frame
        cv2.namedWindow("frame")
        cv2.moveWindow("frame", 0, 0)
        cv2.imshow('frame', frame_r)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


# Run the main function
if __name__ == "__main__":
    main()
