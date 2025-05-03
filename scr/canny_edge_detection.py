import cv2 as cv
import matplotlib.pyplot as plt
import argparse

def call_back(input):
   pass

def canny_edge(image):
    '''A function for canny edge detection of an image
    parameters:
        image: input image
    '''
    window_name = "canny edge"
    cv.namedWindow(window_name)
    cv.createTrackbar("max_treshold",window_name, 00, 255, call_back)
    cv.createTrackbar("min_treshold",window_name, 0, 255, call_back)

    while True:
        if cv.waitKey(1) == ord("q"):
            break
        min_treshold = cv.getTrackbarPos("min_treshold", window_name)
        max_treshold = cv.getTrackbarPos("max_treshold", window_name)
        edges = cv.Canny(image, min_treshold, max_treshold)
        cv.imshow(window_name, edges)
    cv.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description="Apply canny edge detection on images")
    parser.add_argument("image", type=str, help="Path to image")
    arg = parser.parse_args()
    image = cv.imread(arg.image)
    canny_edge(image)

if __name__ == "__main__":
    main()
    