#coding: utf-8
import cv2
import numpy as np

def cap_main(hoop_Coordinate):
    try:
        capture = cv2.VideoCapture(0)

        while(True):
            ret, frame = capture.read()

            if(not ret):
                raise ValueError("Failed to obtain camera image.")

            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            kernel = np.ones((5,5),np.float32)/25
            dst = cv2.filter2D(gray,-1,kernel)
            circles = cv2.HoughCircles(dst,cv2.HOUGH_GRADIENT,0.8,20,param1=75,param2=60,minRadius=0,maxRadius=0)
            hoop_Coordinate = circles

            #"""
            # 検出した円を描画するpg
            # circles = cv2.HoughCirclesで円が検出できないとnumpyarrayにならないからerror
            if(circles is not None):
                for i in circles[0,:]:
                    # draw the outer circle
                    cv2.circle(gray,(i[0],i[1]),i[2],(0,255,0),2)
            #"""

    except Exception as e:
        print("circles typw",type(circles))
        print("\n")
        print("my_camera.py cap_main try error : ",e)
        print("\n")

if __name__ == "__main__":
    cap_main(0)
