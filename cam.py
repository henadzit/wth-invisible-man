import numpy as np
import cv2
import time

DEBUG = True

def main(lower, upper):
    replace_img = cv2.imread('background.png')

    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame

        if DEBUG: start_time = time.time()
        _, frame = cap.read()

        #import pdb; pdb.set_trace()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # 111, 31, 68
        l = np.array(lower)
        u = np.array(upper)

        mask = cv2.inRange(hsv, l, u)
        mask_inv = cv2.bitwise_not(mask)

        main = cv2.bitwise_and(frame, frame, mask=mask_inv)
        replaced = cv2.bitwise_and(replace_img, replace_img, mask=mask)

        cv2.imshow('mask',mask)
        cv2.imshow('res', cv2.add(main, replaced))
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


def save_background():
    cap = cv2.VideoCapture(0)

    for _ in range(0, 25):
        cap.read()

    _, frame = cap.read()

    cv2.imwrite('background.png', frame)

    cap.release()

if __name__ == '__main__':
    main(_convert_hsv(63, 10, 5), _convert_hsv(140, 140, 140))
