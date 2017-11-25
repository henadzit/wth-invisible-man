import numpy as np
import cv2
import time

DEBUG = True

def main(lower, upper):
    l = np.array(lower)
    u = np.array(upper)

    cap = cv2.VideoCapture(0)

    replace_counter = 0
    replace_bg = cv2.imread('background.png')

    x = 1 # 0.1
    y = 1 # 0.00625
    f1_kernel = np.asarray([[y, y, y, y, y],
                            [y, x, x, x, y],
                            [y, x, x, x, y],
                            [y, x, x, x, y],
                            [y, y, y, y, y]])

    while(True):
        if DEBUG: start_time = time.time()

        _, frame = cap.read()

        #import pdb; pdb.set_trace()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, l, u)

        mask = cv2.medianBlur(mask, 9)
        mask = cv2.filter2D(mask, -1, f1_kernel)
        #mask = cv2.blur(mask, (5,5))
        #mask = cv2.medianBlur(mask, 9)
        mask_inv = cv2.bitwise_not(mask)

        bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        fg = cv2.bitwise_and(replace_bg, replace_bg, mask=mask)

        res = cv2.add(bg, fg)

        #cv2.imshow('original', frame)
        #cv2.imshow('mask',mask)
        cv2.imshow('res', res)

        if replace_counter % 15 == 0:
            replace_bg = cv2.add(bg, fg)

        replace_counter += 1

        if DEBUG: processing_elapsed_time = time.time() - start_time
        if DEBUG: _log_elapsed_time("Frame processing time: ", processing_elapsed_time)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        if DEBUG: processing_and_displaying_elapsed_time = time.time() - start_time
        if DEBUG: _log_elapsed_time("Frame processing & displaying time: ", processing_and_displaying_elapsed_time)

    cap.release()
    cv2.destroyAllWindows()


def _convert_hsv(h, s, v):
    return [179 / 365 * h, 255 / 100 * s, 255 / 100 * v]


def _log_elapsed_time(text, elapsed_time):
    print("{:<37}".format(text), '{:02.2f}'.format(elapsed_time))


# not used
def _find_contour():
    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if cnt is not None:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        #import pdb; pdb.set_trace()

        cv2.drawContours(res,[box],0,(0,0,255),2)

        #import pdb; pdb.set_trace()

        if replace_counter % 15 == 0:
            replace_bg = cv2.add(bg, fg)

        replace_counter += 1


def save_background():
    cap = cv2.VideoCapture(0)

    for _ in range(0, 25):
        cap.read()

    _, frame = cap.read()

    cv2.imwrite('background.png', frame)

    cap.release()

if __name__ == '__main__':
    #main(_convert_hsv(48, 6, 5), _convert_hsv(140, 200, 200))
    main(_convert_hsv(63, 10, 5), _convert_hsv(145, 140, 140))
