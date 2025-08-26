import opencv as cv
import numpy as np
import glob

def detect_circles(image):
    gray = cv.cvtColor(image, cv.Color_BGR2GRAY)
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, dp=1.2, minDist=20,
                               param1=50, param2=30, minRadius=20, maxRadius=200)
    return circles[0] if circles is not None else []

def detect_red_regions(image):
    hsv = cv.cvtColor(image, cv.Color_BGR2HSV)
    lower_red1 = np.array([0, 100, 100]) # Lower range for red
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100]) # Upper range for red
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv.add(mask1, mask2)
    return red_mask

def process_images(image_folder):
    selected_images = []
    for img_path in glob.glob(f"{image_folder}/*.jpg"):
        image = cv.imread(img_path)
        red_mask = detect_red_regions(image)
        circles = detect_circles(image)



process_images('path/to/images')