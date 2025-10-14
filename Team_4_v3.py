import cv2 as cv
import numpy as np
import glob, os
import transceiver
import aes
port = "/dev/ttyUSB0"

def detect_red_regions(image, imageName, debug=False):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # two red ranges
    lower_red1 = np.array([0, 200,  200], np.uint8)
    upper_red1 = np.array([12, 255, 255], np.uint8)
    lower_red2 = np.array([168, 200,  200], np.uint8)
    upper_red2 = np.array([180, 255, 255], np.uint8)

    mask1 = cv.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv.bitwise_or(mask1, mask2)

    # clean up small specks / fill gaps
    kernel = np.ones((3, 3), np.uint8)
    red_mask = cv.morphologyEx(red_mask, cv.MORPH_OPEN, kernel, iterations=1)
    red_mask = cv.morphologyEx(red_mask, cv.MORPH_CLOSE, kernel, iterations=1)

    if debug:
        cv.imshow(f"{imageName}", red_mask)
        cv.waitKey(0)
    return red_mask

def detect_circles(image, imageName, debug=False):
    """Return list[(x, y, r)] using HoughCircles. Accepts BGR image or single-channel mask/gray."""
    if image is None:
        return []

    # ensure single-channel gray
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # blur helps Hough; lighter blur for binary masks
    gray = cv.GaussianBlur(gray, (5, 5), 2)

    rows = gray.shape[0]
    minDist = max(10, rows // 8)

    circles = cv.HoughCircles(
        gray,
        cv.HOUGH_GRADIENT,
        dp=1.2,
        minDist=minDist,
        param1=100,                # Canny high threshold
        param2=18,# accumulator threshold; lower finds more (incl. noise)
        minRadius=5,
        maxRadius=0                # 0 = auto
    )

    if circles is None:
        return []

    circles = np.round(circles[0, :]).astype(int)
    out = [tuple(map(int, c)) for c in circles]

    if debug and len(out):
        vis = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
        for (x, y, r) in out:
            cv.circle(vis, (x, y), r, (0, 255, 0), 2)
            cv.circle(vis, (x, y), 2, (0, 0, 255), 3)
            #cropped = image[x - r:x + r, y - r:y + r]
        #cv.imshow("Cropped Image", cropped)
        cv.imshow(f"{imageName}", vis)
        cv.waitKey(0)
    return out


def process_images(image_folder, limit=10, debug=False, require_exactly_one_red=True):
    selected_images = []
    for img_path in glob.glob(os.path.join(image_folder, "*.png")):
        image = cv.imread(img_path, cv.IMREAD_COLOR)
        if image is None or image.size == 0:
            continue

        red_mask = detect_red_regions(image, img_path, debug=debug)
        if cv.countNonZero(red_mask) < 10:
            # very little red -> skip quickly
            continue

        masked = cv.bitwise_and(image, image, mask=red_mask)
        red_circles  = detect_circles(masked, img_path,  debug=debug)

        if not red_circles:
            continue
        if require_exactly_one_red and len(red_circles) != 1:
            continue
        if len(red_circles) == 1:
            circle = red_circles[0]
            x = circle[0]
            y = circle[1]
            r = circle[2]
            cropped = image[y - r:y + r, x - r:x + r]
            root, ext = os.path.splitext(img_path)
            cropped_save = f"{root}_cropped.jpeg"
            cv.imwrite(cropped_save, cropped)
            cv.imshow("cropped image", cropped)
            selected_images.append(cropped_save)
        if len(selected_images) >= limit:
            break

    print("Identified Images:")
    for img in selected_images:
        print(" -", img)
    # If you used debug=True and want to close windows:
    # cv.destroyAllWindows()
    return selected_images

# run
#process_images('./Images', debug=True)
target_img = process_images('./Images', debug=False)

#convert png images to JPEG
for i in range(len(target_img)):
    target_img[i] = (cv.imwrite(f'./Images/image_{i}.jpg', cv.imread(target_img[i])) and f'./Images/image_{i}.jpg')
# encrypt images
password = "ThisKeyForDemoOnly!"
encrypted_files = []
print("Encrypting images...")
for i in range(len(target_img)):
    encrypted_file = f'./encrypted_{i}.bin'
    aes.encyrpt(password, target_img[i], encrypted_file)
    encrypted_files.append(encrypted_file)

files = []

# prep images for transmission
for i in range(1):#in range(len(encrypted_files)):
    with open(encrypted_files[i], 'rb') as f:
        files.append(f.read())

# transmit images
t = transceiver.transceiver(port)
t.open()
t.transmit(files)