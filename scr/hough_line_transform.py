import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import argparse

def hough_line_transform(image, output_path=None):
    '''A function for detecting straight lines in an image.
    Parameters:
        image: input image
        output_path: path to save the processed image (optional)
    '''
    image = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    img_blur = cv.GaussianBlur(image, (21,21), 3)
    canny_edge = cv.Canny(img_blur, 50,180)

    plt.subplot(131)
    plt.imshow(img_blur, cmap="gray")
    plt.title("Blurred Image")
    plt.subplot(132)
    plt.imshow(canny_edge)
    plt.title("Canny Edge Image ")

    distance_resolution = 1
    angle_resolution = np.pi/180
    threshold = 130
    lines = cv.HoughLines(canny_edge,distance_resolution,angle_resolution,threshold)

    k = 3000
    for line in lines:
        rho, theta = line[0]
        dhat = np.array([[np.cos(theta)], [np.sin(theta)]])
        d = rho * dhat
        lhat = np.array([[-np.sin(theta)], [np.cos(theta)]])
        p1 = d + k*lhat
        p2 =  d - k*lhat
        p1 = p1.astype(int)
        p2 = p2.astype(int)
        cv.line(image,(p1[0][0], p1[1][0]), (p2[0][0], p2[1][0]), (0,255,0),5)

    plt.subplot(133)
    plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    plt.title("Hough Lines")
    if output_path is not None:
        path = output_path
        plt.savefig(path)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Apply hough line transformation on images")
    parser.add_argument("input_path", type=str, help="Path to image")
    parser.add_argument("--output_path", type=str, help="Path to save outcome image")
    arg = parser.parse_args()

    image = cv.imread(arg.input_path)
    if image is None:
        print("Error: Could not load image. Check the file path.")
        return
    hough_line_transform(image, arg.output_path)
    
if __name__ == "__main__":
    main()
