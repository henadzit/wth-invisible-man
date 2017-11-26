//
//  OpenCVWrapper.m
//  iOSWTF
//
//  Created by Anthony Marchenko on 11/24/17.
//  Copyright © 2017 Anthony Marchenko. All rights reserved.
//

#import <vector>
#import <opencv2/opencv.hpp>
#import <opencv2/imgproc.hpp>
#import <opencv2/imgcodecs/ios.h>
#import <opencv2/imgproc.hpp>
#import <opencv2/highgui.hpp>

#import <Foundation/Foundation.h>
#import "OpenCVWrapper.h"

cv::Scalar convertHsv(double h, double s, double v) {
    return cvScalar((double)179 / 365 * h, (double)255 / 100 * s, (double)255 / 100 * v);
}

///// Restore the orientation to image.
static UIImage *RestoreUIImageOrientation(UIImage *processed, UIImage *original) {
    if (processed.imageOrientation == original.imageOrientation) {
        return processed;
    }
    return [UIImage imageWithCGImage:processed.CGImage scale:1.0 orientation:original.imageOrientation];
}

#pragma mark -

@implementation OpenCVWrapper {
    cv::CascadeClassifier cascade;
}

+ (nonnull UIImage *)cvtColorBGR2GRAY:(nonnull UIImage *)image {
    cv::Mat bgrMat;
    UIImageToMat(image, bgrMat);
    cv::Mat grayMat;
    cv::cvtColor(bgrMat, grayMat, CV_BGR2GRAY);
    
    //cv::Mat invertedOutput = 255 - grayMat;
    
    return RestoreUIImageOrientation(MatToUIImage(grayMat), image);
}

#pragma mark - Convert to grayscale
+ (UIImage *)convertToGrayscale:(UIImage *)image {
    cv::Mat imageMat;
    UIImageToMat(image, imageMat);
    
    if (imageMat.channels() == 1) return image;
    
    // Transform
    cv::Mat grayMat;
    cv::cvtColor(imageMat, grayMat, CV_BGR2GRAY);
    // Convert to UImage
    return MatToUIImage(grayMat);
}

#pragma mark - Classify Image
+ (nonnull UIImage *)classifyImage:(nonnull UIImage *)image {
    // Convert UIImage to CV Mat
    cv::Mat colorMat;
    UIImageToMat(image, colorMat);
    
    // Convert to grayscale
    cv::Mat grayMat;
    cv::cvtColor(colorMat, grayMat, CV_BGR2GRAY);
    
    // Load classifier from file
    cv::CascadeClassifier classifier;
    const NSString* cascadePath = [[NSBundle mainBundle]
                                   pathForResource:@"haarcascade_frontalface_default"
                                   ofType:@"xml"];
    classifier.load([cascadePath UTF8String]);
    
    // Initialize vars for classifier
    std::vector<cv::Rect> detections;
    
    const double scalingFactor = 1.1;
    const int minNeighbors = 2;
    const int flags = 0;
    const cv::Size minimumSize(300, 300);
    
    // Classify function
    classifier.detectMultiScale(
                                grayMat,
                                detections,
                                scalingFactor,
                                minNeighbors,
                                flags,
                                minimumSize
                                );
    
    // If no detections found, return nil
    if (detections.size() <= 0) {
        return nil;
    }
    
    // Range loop through detections
    for (auto &face : detections) {
        const cv::Point tl(face.x,face.y);
        const cv::Point br = tl + cv::Point(face.width, face.height);
        const cv::Scalar magenta = cv::Scalar(255, 0, 255);
        
        cv::rectangle(colorMat, tl, br, magenta, 4, 8, 0);
    }
    
    return MatToUIImage(colorMat);
}

- (id)init {
    self = [super init];
    
    // Reading Classifiers
    NSBundle *bundle = [NSBundle mainBundle];
    NSString *path = [bundle pathForResource:@"haarcascade_frontalface_alt" ofType:@"xml"];
    std::string cascadeName = (char *)[path UTF8String];
    
    if(!cascade.load(cascadeName)) {
        return nil;
    }
    
    return self;
}

- (nonnull UIImage *)recognizeFace:(nonnull UIImage *)image {
    // UIImage -> cv::Mat conversion
    CGColorSpaceRef colorSpace = CGImageGetColorSpace(image.CGImage);
    CGFloat cols = image.size.width;
    CGFloat rows = image.size.height;
    
    cv::Mat mat(rows, cols, CV_8UC4);
    
    CGContextRef contextRef = CGBitmapContextCreate(mat.data,
                                                    cols,
                                                    rows,
                                                    8,
                                                    mat.step[0],
                                                    colorSpace,
                                                    kCGImageAlphaNoneSkipLast |
                                                    kCGBitmapByteOrderDefault);
    
    CGContextDrawImage(contextRef, CGRectMake(0, 0, cols, rows), image.CGImage);
    CGContextRelease(contextRef);
    
    
    // Face detection
    std::vector<cv::Rect> faces;
    
    
    cascade.detectMultiScale(mat, faces,
                             1.1, 2,
                             CV_HAAR_SCALE_IMAGE,
                             cv::Size(30, 30));
    
    // Draw a circle at the position of the face
    std::vector<cv::Rect>::const_iterator r = faces.begin();
    for(; r != faces.end(); ++r) {
        cv::Point center;
        int radius;
        center.x = cv::saturate_cast<int>((r->x + r->width*0.5));
        center.y = cv::saturate_cast<int>((r->y + r->height*0.5));
        radius = cv::saturate_cast<int>((r->width + r->height) / 2);
        cv::circle(mat, center, radius, cv::Scalar(80,80,255), 3, 8, 0 );
    }
    
    // cv :: Mat -> UIImage conversion
    UIImage *resultImage = MatToUIImage(mat);
    
    return RestoreUIImageOrientation(resultImage, image);
}

+ (nonnull UIImage *)wtfMan:(nonnull UIImage *)image {
    cv::Mat bgrMat;
    UIImageToMat(image, bgrMat);
    
    cv::Mat grayMat;
    cv::cvtColor(bgrMat, grayMat, cv::COLOR_BGR2HSV);
    
    // cv::Mat invertedOutput = 255 - grayMat;
    
    cv::Scalar l = convertHsv(63, 10, 5);
    cv::Scalar u = convertHsv(140, 140, 140);
    
    int replace_counter = 0;
    
    UIImage *imageToReplace = [UIImage imageNamed:@"white.jpg"];
    cv::Mat replace_bg;// = 256 - bgrMat;
    UIImageToMat(imageToReplace,replace_bg);
    cv::Mat f1_kernel = cv::Mat::ones(5, 5, CV_64F);
    
    cv::Mat frame, hsv;
    frame = bgrMat;
    
    
    for(;;)
    {
        // cap >> frame;
        cvtColor(frame, hsv, cv::COLOR_BGR2HSV);
        
        cv::Mat mask;
        inRange(hsv, l, u, mask);
        
        medianBlur(mask, mask, 9);
        filter2D(mask, mask, -1, f1_kernel);
        
        cv::Mat maskInv;
        bitwise_not(mask, maskInv);
        
        cv::Mat bg;
        bitwise_and(frame, frame, bg, maskInv);
        
        cv::Mat fg;
        bitwise_and(replace_bg, replace_bg, fg, mask);
        
        cv::Mat show;
        add(bg, fg, show);
        //  imshow("edges", show);
        
        if(replace_counter % 15 == 0) {
            add(bg, fg, replace_bg);
        }
        replace_counter += 1;
        
        break;
    }
    
    return RestoreUIImageOrientation(MatToUIImage(replace_bg), image);
}

- (UIImage *)takeSnapShot {
    UIWindow *keyWindow = [[UIApplication sharedApplication] keyWindow];
    CGRect rect = [keyWindow bounds];
    UIGraphicsBeginImageContextWithOptions(rect.size,YES,0.0f);
    CGContextRef context = UIGraphicsGetCurrentContext();
    [keyWindow.layer renderInContext:context];
    UIImage *capturedScreen = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return capturedScreen;
}

@end

