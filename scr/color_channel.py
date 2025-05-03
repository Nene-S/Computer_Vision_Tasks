import argparse
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

def pure_colors(zeros, ones, output_path=None):
    ''' 
    A function to plot pure colors such as black, white, red, green, and blue. 
    parameters:
        Zeros : A 2D numpy array of of zeros
        ones : A 2D numpy array of ones
    returns: 
        None
    '''
    ones = ones *255
    b_img = cv.merge((zeros, zeros, ones))
    g_img = cv.merge((zeros, ones, zeros))
    r_img = cv.merge((ones, zeros, zeros))
    white_img = cv.merge((ones, ones, ones))
    black_img = cv.merge((zeros, zeros, zeros))
    
    fig, ax = plt.subplots(2,3,sharex=True, sharey=True)
    ax = ax.flatten()

    title_list =["Blue image", "Green image", "Red image", "White image", "Black image"]
    image_list = [b_img, g_img, r_img, white_img, black_img]

    for i, (img, title) in enumerate(zip(image_list, title_list)):
        ax[i].imshow(img)
        ax[i].set_title(title)
        ax[i].set_xticks([])
        ax[i].set_yticks([])

    plt.tight_layout()
    if output_path is not None:
        path = output_path
        plt.savefig(path, dpi=300)
    plt.show()

def bgr_color_channel(image, output_path):
    '''
    A function that splits an image into it's three color channel, blue, red, green, and the plots it.
    parameter:
        image
     returns: 
        None
    '''
    b, r, g = cv.split(image) 
    zeros = np.zeros_like(b)
    b_img = cv.merge((zeros,zeros,b))
    g_img = cv.merge((zeros,g,zeros))
    r_img = cv.merge((r,zeros,zeros))

    img_split = [b_img, g_img, r_img]
    title = ["Blue","Green","Red"]

    fig, ax = plt.subplots(1,3)
    ax = ax.flatten()
    for i, (img, title) in enumerate(zip(img_split, title)):
        ax[i].imshow(img)
        ax[i].set_title(title)

    plt.tight_layout()
    if output_path is not None:
        path = output_path
        plt.savefig(path, dpi=300)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description=" color channels script")
    parser.add_argument("color", choices=["pure_colors", "bgr_colors"], help= "Type of color function to call")
    parser.add_argument("--image", type=str, help="Path to image")
    parser.add_argument("--zeros",nargs="+", type=int, help="A two tuple of zeros to be generated")
    parser.add_argument("--ones", nargs="+", type=int, help="A two tuple of ones to be generated")
    parser.add_argument("--output_path", type=str, help= "Path to save output plot")
    arg = parser.parse_args()

    if arg.color == "pure_colors":
        zeros = np.zeros(tuple(arg.zeros), dtype=np.uint8)
        ones = np.ones(tuple(arg.ones), dtype=np.uint8)
        pure_colors(zeros, ones, arg.output_path)
    elif arg.color == "bgr_colors":
        image = cv.imread(arg.image)
        bgr_color_channel(image, arg.output_path)
    else:
        print("invalid color choice")

if __name__ =="__main__": 
    main()
