import argparse

import numpy as np
import cv2
import time

DEBUG = True

def main(lower, upper, dyn=False):
    l = np.array(lower)
    u = np.array(upper)

    frame_counter = 0
    replace_bg = None

    f1_kernel = np.ones((9, 9), dtype=np.int)

    cap = cv2.VideoCapture(1)

    # set camera width and height
    cap.set(3, 1024)
    cap.set(4, 768)

    start_time = time.time()
    while(True):
        if DEBUG: it_start_time = time.time()

        _, frame = cap.read()

        # we need to skip a few first frames because they are corrupt
        if replace_bg is None or frame_counter < 3:
            replace_bg = frame

        #import pdb; pdb.set_trace()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, l, u)

        mask = cv2.medianBlur(mask, 9)
        mask = cv2.filter2D(mask, -1, f1_kernel)
        mask_inv = cv2.bitwise_not(mask)

        bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        fg = cv2.bitwise_and(replace_bg, replace_bg, mask=mask)

        res = cv2.add(bg, fg)

        _draw_mode(res, dyn)

        #cv2.imshow('original', frame)
        #cv2.imshow('mask',mask)
        cv2.imshow('res', res)

        if dyn and frame_counter % 15 == 0:
            replace_bg = res

        frame_counter += 1

        if DEBUG: processing_elapsed_time = time.time() - it_start_time
        if DEBUG: _log_elapsed_time("Frame processing time: ", processing_elapsed_time)

        # hadle keys
        key = cv2.waitKey(25) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('u'):
            # update background
            replace_bg = frame
        elif key == ord('d'):
            dyn = True
        elif key == ord('s'):
            dyn = False
            replace_bg = frame

        if DEBUG:
            processing_and_displaying_elapsed_time = time.time() - it_start_time
            _log_elapsed_time("Frame processing & displaying time: ", processing_and_displaying_elapsed_time)
            _log_elapsed_time("Frame/sec: ", frame_counter / (time.time() - start_time))

    cap.release()
    cv2.destroyAllWindows()


def _draw_mode(img, dyn):
    text = 'D' if dyn else 'S'
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, (5,25), font, 1, (255,255,255))


def _convert_hsv(h, s, v):
    return [179 / 365 * h, 255 / 100 * s, 255 / 100 * v]


def _log_elapsed_time(text, elapsed_time):
    print("{:<37}".format(text), '{:02.2f}'.format(elapsed_time))


# not used
def _find_contour(mask, res):
    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnt = max(contours, key=lambda c: len(c)) if contours is not None else None

    if cnt is not None:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        cv2.drawContours(res,[box],0,(0,0,255),2)


def save_background():
    cap = cv2.VideoCapture(0)

    for _ in range(0, 25):
        cap.read()

    _, frame = cap.read()

    cv2.imwrite('background.png', frame)

    cap.release()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dyn', dest='dyn', action='store_true')
    parser.set_defaults(dyn=False)
    args = parser.parse_args()

    #main(_convert_hsv(48, 6, 5), _convert_hsv(140, 200, 200))
    main(_convert_hsv(63, 10, 5), _convert_hsv(145, 140, 140), dyn=args.dyn)
