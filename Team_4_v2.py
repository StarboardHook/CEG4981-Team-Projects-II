import cv2 as cv
import numpy as np
import glob

#load in images 1 by 1 from a folder and check if the file path is valid
#create a red mask for the image and an output vector of the found circles
#create an image using the red mask to pull circle output vector
#check if there are at least 1 circle in each red and base image
def process_images(image_folder):
    selected_images = []
    for img_path in glob.glob(f"{image_folder}/*.png"):
        image = cv.imread(img_path)
        if image is None:
            continue
        red_mask = detect_red_regions(image)
        gray_circles = detect_circles(image)
        red_circles = detect_circles(cv.bitwise_and(image, image, mask=red_mask))
        if len(gray_circles) >= 1 and len(red_circles) is 1:
            #circle vector is stores as [x, y, r]
            #where x and y are the center coords and r is the radius
            for i, circle1 in enumerate(gray_circles):
                #if any(is_circle_overlap(circle1, circle2) for j, circle2 in enumerate(red_circles)):
                if is_circle_overlap(circle1, red_circles[0]):
                    selected_images.append(img_path)
                    break
        if len(selected_images) == 10:
            break
    print("Identified Images:", selected_images)

process_images('./Images')

