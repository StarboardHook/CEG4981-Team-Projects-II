import cv2 as cv
import numpy as np
import glob

def detect_circles(image, output_path):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 9)
    rows = gray.shape[0]
    circles = cv.HoughCircles(
        gray, cv.HOUGH_GRADIENT, dp=1.2, minDist=rows/8,
        param1=200, param2=50, minRadius=5, maxRadius=0
    )

    if circles is not None:
        circles = np.round(circles[0, :2]).astype("int")  # Limit to 2 circles
        output = image.copy()
        for (x, y, r) in circles:
            cv.circle(output, (x, y), r, (0, 255, 0), 2)   # circle outline
            cv.circle(output, (x, y), 2, (0, 0, 255), 3)   # center point
        cv.imwrite(output_path, output)  # Save the output image
        return circles
    else:
        return []

def detect_red_regions(image):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    lower1 = np.array([0, 50, 50])   # Lower range for red (0-10)
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 50, 50]) # Upper range for red (170-180)
    upper2 = np.array([180, 255, 255])
    mask1 = cv.inRange(hsv, lower1, upper1)
    mask2 = cv.inRange(hsv, lower2, upper2)
    mask = cv.bitwise_or(mask1, mask2)
    cv.imshow("Red Mask", mask)
    cv.waitKey(0)
    return cv.bitwise_and(image, image, mask=mask)

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
        output_path = img_path.replace(".png", "_output.png")
        circles = detect_circles(image, output_path)

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
                    if cv.countNonZero(cv.bitwise_and(red_mask, mask_circle)) > 0:
                        selected_images.append(img_path)
                        break
        if len(selected_images) == 10:
            break

    print("Identified Images:", selected_images)


process_images('./Images')