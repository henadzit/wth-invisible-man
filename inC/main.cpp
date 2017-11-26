//
//  main.cpp
//  wthInvisMan
//
//  Created by Alexey Dubrov on 11/25/17.
//  Copyright © 2017 Alexey Dubrov. All rights reserved.
//

#include "iostream"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "string"
#include "fstream"
#include "ctime"
#include "ratio"
#include "chrono"

using namespace cv;
using namespace std;
using namespace std::chrono;

Scalar convertHsv(double h, double s, double v) {
    return Scalar((double)179 / 365 * h, (double)255 / 100 * s, (double)255 / 100 * v);
}

bool isDynamic() {
    String fullfile = "/Work/Workspaces/Garage/wth3/inC/freeze";
    ifstream fin(fullfile);

    return !fin;
}

void logFps(high_resolution_clock::time_point start, high_resolution_clock::time_point now, int frame_counter) {
    duration<double> time_span = now - start;
    printf( "Frame/sec: %f \n", (double)(frame_counter / time_span.count()) );
}
 
int main(int argc, const char * argv[]) {
    Scalar l = convertHsv(63, 10, 5);
    Scalar u = convertHsv(140, 140, 140);
    
    VideoCapture cap(0);
    if(!cap.isOpened()) return -1;

    cap.set(CV_CAP_PROP_FRAME_WIDTH,640);
    cap.set(CV_CAP_PROP_FRAME_HEIGHT,480);
    
    Mat frame, hsv;
    
    namedWindow("Invisible Man", 1);
    
    int frame_counter = 0;
    bool isNone = true;
    Mat replace_bg;
    Mat f1_kernel = Mat::ones(9, 9, CV_64F);
    
    high_resolution_clock::time_point startTime = high_resolution_clock::now();
    for(;;) {
        cap >> frame;
        cvtColor(frame, hsv, COLOR_BGR2HSV);

        if (isNone || frame_counter < 3) {
            isNone = false;
            replace_bg = frame.clone();
        }
        
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
        
        if(frame_counter % 2 == 0 && isDynamic()) {
            replace_bg = show;
        }
        frame_counter++;
        
        if(waitKey(25) >= 0) break;

        high_resolution_clock::time_point now = high_resolution_clock::now();
        logFps(startTime, now, frame_counter);
    }
    return 0;
}
