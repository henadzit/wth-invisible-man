//
//  OpenCVWrapper.m
//  iOSWTF
//
//  Created by Anthony Marchenko on 11/24/17.
//  Copyright © 2017 Anthony Marchenko. All rights reserved.
//

#ifdef __cplusplus
#undef NO
#undef YES
#import <opencv2/opencv.hpp>
#endif
#import "OpenCVWrapper.h"

@implementation OpenCVWrapper

+ (NSString *)openCVVersion {
    return [NSString stringWithFormat:@"OpenCV Version - %s", CV_VERSION];
}

@end
