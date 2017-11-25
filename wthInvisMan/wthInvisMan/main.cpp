//
//  main.cpp
//  wthInvisMan
//
//  Created by Alexey Dubrov on 11/25/17.
//  Copyright © 2017 Alexey Dubrov. All rights reserved.
//

#include <iostream>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>

using namespace cv;

Scalar convertHsv(double h, double s, double v) {
    return Scalar((double)179 / 365 * h, (double)255 / 100 * s, (double)255 / 100 * v);
}

int main(int argc, const char * argv[]) {
    VideoCapture cap(0);
    if(!cap.isOpened()) return -1;
    
    Mat frame, hsv;
    
    namedWindow("edges", 1);
    Mat replaceImg = imread("/Work/Workspaces/Garage/wth3/wth-invisible-man/background.png");
    
    for(;;)
    {
        cap >> frame;
        cvtColor(frame, hsv, COLOR_BGR2HSV);
        
        Scalar l = convertHsv(63, 10, 5);
        Scalar u = convertHsv(140, 140, 140);
        
        Mat mask;
        inRange(hsv, l, u, mask);
        Mat maskInv;
        bitwise_not(mask, maskInv);
        
        Mat main;
        bitwise_and(frame, frame, main, maskInv);
        
        Mat replaced;
        bitwise_and(replaceImg, replaceImg, replaced, mask);
        
        Mat show;
        add(main, replaced, show);
        //imshow("edges", mask);
        imshow("edges", show);
        if(waitKey(30) >= 0) break;
    }
    return 0;
}
