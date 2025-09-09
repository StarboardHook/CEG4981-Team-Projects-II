import cv2 as cv
import numpy as np
import glob

def detect_circles(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 9)
    rows = gray.shape[0]
    circles = cv.HoughCircles(
        gray, cv.HOUGH_GRADIENT, dp=1.2, minDist=rows/8,
        param1=200, param2=50, minRadius=0, maxRadius=0
    )

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        output = image.copy()
        for (x, y, r) in circles:
            cv.circle(output, (x, y), r, (0, 255, 0), 2)   # circle outline
            cv.circle(output, (x, y), 2, (0, 0, 255), 3)   # center point
        cv.imshow("Detected Circles", output)
        cv.waitKey(0)
        cv.destroyAllWindows()
        return circles
    else:
        return []
    #cv.imshow("Detected Circles", circles)
    #return circles[0] if circles is not None else []

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

def show_detected_circles(image, circles, winname="Detected Circles"):
    output = image.copy()

    if len(circles) > 0:
        for (x, y, r) in circles:
            # draw the outer circle
            cv.circle(output, (int(x), int(y)), int(r), (0, 255, 0), 2)
            # draw the circle center
            cv.circle(output, (int(x), int(y)), 2, (0, 0, 255), 3)

    cv.imshow(winname, output)
    cv.waitKey(0)
    cv.destroyAllWindows()

def process_images(image_folder):
    selected_images = []
    for img_path in glob.glob(f"{image_folder}/*.png"):
        image = cv.imread(img_path)
        if image is None:
            continue  # Skip if image not loaded

        red_mask = detect_red_regions(image)
        circles = detect_circles(image)
        #show_detected_circles(image,circles)

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
