import os
import cv2 as cv
import time
import uuid


# Configurations
IMAGE_PATH = "CollectedImages"
labels = ["One", "Two", "Three", "Four", "Five"]
num_of_images = 5
capture_delay = 2 # seconds btw captures
startup_delay = 3


# create the main folder if it doesn't exist
os.makedirs(IMAGE_PATH, exist_ok=True)

for label in labels:
    label_path = os.path.join(IMAGE_PATH, label)
    os.makedirs(label_path, exist_ok=True)

    # open webcam
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Error can't open the webcam")
        break

    print(f"\nCollecting images for {label} in {startup_delay} secs")
    time.sleep(startup_delay)

    for img_num in range(num_of_images):
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture img. Skipping....")
            continue


        # save image with unique name
        image_name = os.path.join(label_path, f"{label}.{uuid.uuid1()}.jpg")
        cv.imwrite(image_name, frame)

        # display the captured frame
        cv.imshow("Capturing", frame)
        print(f"Captured image {img_num+1} for {label}")

        # wait before next capture or break if 'q' is pressed
        if cv.waitKey(capture_delay * 1000) & 0xFF == ord('q'):
            print("Capture interruped by user")
            break

    # release webcam & close windows
    cap.release()
    cv.destroyAllWindows()

print("\nImage Collection Completed")