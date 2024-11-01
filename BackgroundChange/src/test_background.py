import cv2
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # loading main image
    main_image = cv2.imread("../pisici.jpg")

    # loading background image
    background_image = cv2.imread("../perdea.jpg")

    # converting the main image to grayscale for thresholding
    gray_image = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)

    # apply binary thresholding to separate the foreground (el gatos)
    # adjust the threshold value for the best result
    _, binary_mask = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY_INV)

    # resize the background image to match the main image's dimensions)
    background_resized = cv2.resize(background_image, (main_image.shape[1], main_image.shape[0]))

    # create a mask for the main subject
    # flood fill to create the inverse of the mask
    flood_filled = binary_mask.copy()
    h, w = binary_mask.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood_filled, mask, (0, 0), 255)
    flood_filled_inv = cv2.bitwise_not(flood_filled)

    # use the mask to extract the subject from the main image
    foreground = cv2.bitwise_and(main_image, main_image, mask=flood_filled_inv)

    # mask the background to replace it with the texture
    background = cv2.bitwise_and(background_resized, background_resized, mask=flood_filled)

    # combine the subject with the new background
    result = cv2.add(foreground, background)

    # display the result
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("Final image with background")
    plt.axis('off')
    plt.show()