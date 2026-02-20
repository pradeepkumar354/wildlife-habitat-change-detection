import cv2
import os
import numpy as np

def detect_change(before_path, after_path, output_path):
    """
    Performs simple image differencing to detect changes
    """

    img1 = cv2.imread(before_path)
    img2 = cv2.imread(after_path)

    if img1 is None or img2 is None:
        raise ValueError("Unable to read images")

    # Resize to same size (important)
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Grayscale difference (structural change)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    gray_diff = cv2.absdiff(gray1, gray2)

    # Green channel difference (vegetation change)
    green1 = img1[:, :, 1]
    green2 = img2[:, :, 1]
    green_diff = cv2.absdiff(green1, green2)

    # Combine both differences
    diff = cv2.addWeighted(gray_diff, 0.5, green_diff, 0.5, 0)



    # Threshold to highlight changes
    _, thresh = cv2.threshold(diff, 60, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)


    # ✅ Percentage calculation (IMPORTANT)
    changed_pixels = np.count_nonzero(thresh)
    total_pixels = thresh.size
    change_percentage = (changed_pixels / total_pixels) * 100

    # Save result
    cv2.imwrite(output_path, thresh)

    return output_path, round(change_percentage, 2)

