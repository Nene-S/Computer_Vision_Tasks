import cv2 as cv
import argparse
import os 

def paranoma_stitch(directory):
    folder_list = os.listdir(directory)

    for folder in folder_list:
        path = os.path.join(directory, folder)
        image_folder = os.listdir(path)
        images = []
        for image in image_folder:
           cur_img = cv.imread(os.path.join(path, image))
           cur_img = cv.resize(cur_img,(0,0),None, 0.2,0.2)
           images.append(cur_img)

        stitcher = cv.Stitcher.create()
        status, result = stitcher.stitch(images)
        if status == cv.STITCHER_OK:
            print("panarama generated successfully")
            cv.imshow(image, result)
            cv.waitKey(1)
        else:
            print("unsuccessful")

    cv.waitKey(0)

def main():
    parser = argparse.ArgumentParser(description="Script for paranoma stitching")
    parser.add_argument("directory", type=str, help="Path to directory that contains images to be stitched")
    arg = parser.parse_args()
    paranoma_stitch(arg.directory)

if __name__ == "__main__":
    main()
