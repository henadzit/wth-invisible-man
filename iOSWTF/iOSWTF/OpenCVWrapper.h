//
//  OpenCVWrapper.h
//  iOSWTF
//
//  Created by Anthony Marchenko on 11/24/17.
//  Copyright © 2017 Anthony Marchenko. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

@interface OpenCVWrapper : NSObject

/// Converts a full color image to grayscale image with using OpenCV.
+ (nonnull UIImage *)cvtColorBGR2GRAY:(nonnull UIImage *)image;
+ (nonnull UIImage *)classifyImage:(nonnull UIImage *)image;
- (nonnull UIImage *)recognizeFace:(nonnull UIImage *)image;
+ (nonnull UIImage *)wtfMan:(nonnull UIImage *)image;

@end
