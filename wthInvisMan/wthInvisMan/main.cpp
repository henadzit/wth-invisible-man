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
    Scalar l = convertHsv(63, 10, 5);
    Scalar u = convertHsv(140, 140, 140);
    
    VideoCapture cap(0);
    if(!cap.isOpened()) return -1;
    
    Mat frame, hsv;
    
    namedWindow("Invisible Man", 1);
    
    int replace_counter = 0;
    Mat replace_bg = imread("/Work/Workspaces/Garage/wth3/wth-invisible-man/background.png");
    Mat f1_kernel = Mat::ones(5, 5, CV_64F);
    
    for(;;)
    {
        cap >> frame;
        cvtColor(frame, hsv, COLOR_BGR2HSV);
        
        Mat mask;
        inRange(hsv, l, u, mask);
        
        medianBlur(mask, mask, 9);
        filter2D(mask, mask, -1, f1_kernel);
        
        Mat maskInv;
        bitwise_not(mask, maskInv);
        
        Mat bg;
        bitwise_and(frame, frame, bg, maskInv);
        
        Mat fg;
        bitwise_and(replace_bg, replace_bg, fg, mask);
        
        Mat show;
        add(bg, fg, show);
        imshow("edges", show);
        
        if(replace_counter % 15 == 0) {
            add(bg, fg, replace_bg);
        }
        replace_counter += 1;
        
        if(waitKey(30) >= 0) break;
    }
    return 0;
}
