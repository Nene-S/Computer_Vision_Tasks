import argparse
import cv2 as cv
import matplotlib.pyplot as plt
  
def gray_histogram(image):
    ''' A function that plots the histogram of a gray image
    parameter:
        image: Input image
    '''
    cv.imshow("Gray image",image)
    cv.waitKey(3)

    hist = cv.calcHist([image], [0], None, [256], [0,256])
    plt.figure()
    plt.plot(hist)

    plt.title("Grayscale Image Histogram")
    plt.ylabel("number of pixels")
    plt.xlabel("intensity of pixels")
    plt.show()

def color_histogram(image, color_space,colors):
    ''' A function that plots the histogram of an image in a specified color space.
    parameter:
        image: Input image.
        color_space (str): Color space (e.g., 'BGR', 'HSV', 'Lab').
        colors (list): Channel colors (e.g., ['blue', 'green', 'red']).
    '''
    cv.imshow(color_space,image)
    cv.waitKey(3)

    channels = [0,1,2]

    plt.figure()
    for channel, color in zip(channels, colors):
        hist = cv.calcHist([image],[channel],None,[256],[0,256])
        plt.plot(hist,color)
        
    plt.title(f"{color_space} Histogram")
    plt.ylabel("number of pixels")
    plt.xlabel("intensity of pixels")
    plt.legend(colors)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description=" image histogram plot script")
    parser.add_argument("image", type=str, help="Path to input image")
    parser.add_argument("histogram", choices=["gray_histogram", "color_histogram"], help= "Type of histogram plot function to call")
    parser.add_argument("--color_space", choices=["BGR", "HSV", "LAB"], help="The color space of the image")
    parser.add_argument("--colors", nargs="+", help="A list of color names, e.g., red green blue")
    arg = parser.parse_args()

    image = cv.imread(arg.image)
    if arg.histogram == "gray_histogram":
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gray_histogram(image)
    elif arg.histogram == "color_histogram" and arg.color_space == "BGR":
        color_histogram(image, arg.color_space, arg.colors)
    elif arg.histogram == "color_histogram" and arg.color_space == "HSV":
        hsv_img = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        color_histogram(hsv_img, arg.color_space, arg.colors)
    elif arg.histogram == "color_histogram" and arg.color_space == "LAB":
        lab_img = cv.cvtColor(image, cv.COLOR_BGR2Lab)
        color_histogram(lab_img, arg.color_space, arg.colors)
    else:
        print("invalid color choice")

if __name__ =="__main__": 
    main()

