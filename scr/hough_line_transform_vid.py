import cv2 as cv
import numpy as np
import argparse

def hough_line_transform(video):
    while True:
        success, frame = video.read()
        frame = cv.resize(frame, None, fx=1, fy=0.4 )
        img_blur = cv.GaussianBlur(frame, (5,5), 3)
        edge = cv.Canny(img_blur, 50, 180)
        lines = cv.HoughLinesP(edge, 1, np.pi/180, 130, maxLineGap=50)

        if lines is not None:
             for line in lines:
                  x1, y1, x2, y2 = line[0]
                  cv.line(frame, (x1,y1), (x2,y2), (0,255,0), 5)
                  
        cv.imshow("video",frame)
        cv.imshow("edge", edge)
        cv.waitKey(5)

        if cv.waitKey(1) & 0xFF == ord('q'):
                break
        
def main():
    parser = argparse.ArgumentParser(description="Apply hough line transformation to a video")
    parser.add_argument("input_path", type=str, help="Path to video")
    arg = parser.parse_args()
            
    cap = cv.VideoCapture(arg.input_path)
    hough_line_transform(cap)
    
if __name__ == "__main__":
    main()
    