import cv2 as cv
import numpy as np
import glob

def detect_circles(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    circles = cv.HoughCircles(
        gray, cv.HOUGH_GRADIENT, dp=1.2, minDist=20,
        param1=50, param2=30, minRadius=20, maxRadius=200
    )
    return circles[0] if circles is not None else []

def detect_red_regions(image):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 100, 100])   # Lower range for red
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100]) # Upper range for red
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    return cv.add(mask1, mask2)

def is_circle_overlap(circle1, circle2):
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2
    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance < (r1 + r2)

def process_images(image_folder):
    selected_images = []
    for img_path in glob.glob(f"{image_folder}/*.png"):
        image = cv.imread(img_path)
        if image is None:
            continue  # Skip if image not loaded

        red_mask = detect_red_regions(image)
        circles = detect_circles(image)

        if len(circles) >= 2:
            for i, circle1 in enumerate(circles):
                if any(
                    is_circle_overlap(circle1, circle2)
                    for j, circle2 in enumerate(circles) if i != j
                ):
                    mask_circle = np.zeros_like(red_mask)
                    cv.circle(
                        mask_circle,
                        (int(circle1[0]), int(circle1[1])),
                        int(circle1[2]),
                        255,
                        -1
                    )
                    if cv.countNonZero(cv.bitwise_and(red_mask, mask_circle)) > 100:
                        selected_images.append(img_path)
                        break
        if len(selected_images) == 10:
            break

    print("Identified Images:", selected_images)


process_images('./Images')
