import numpy as np
import cv2


def main(lower, upper):
    #replace_img = cv2.imread('background.png')

    l = np.array(lower)
    u = np.array(upper)

    cap = cv2.VideoCapture(0)

    replace_counter = 0
    replace_bg = cv2.imread('background.png')

    x = 0.05 # 0.1
    y = 0.05 # 0.00625
    f1_kernel = np.asarray([[y, y, y, y, y],
                            [y, x, x, x, y],
                            [y, x, x, x, y],
                            [y, x, x, x, y],
                            [y, y, y, y, y]])

    while(True):
        _, frame = cap.read()

        #import pdb; pdb.set_trace()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, l, u)
        #mask = cv2.filter2D(mask, -1, f1_kernel)
        #mask = cv2.blur(mask, (5,5))
        mask = cv2.medianBlur(mask, 9)
        mask_inv = cv2.bitwise_not(mask)

        bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        fg = cv2.bitwise_and(replace_bg, replace_bg, mask=mask)

        # cv2.imshow('mask',mask)
        cv2.imshow('res', cv2.add(bg, fg))

        if replace_counter % 5 == 0:
            replace_bg = cv2.add(bg, fg)
        replace_counter += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def _convert_hsv(h, s, v):
    return [179 / 365 * h, 255 / 100 * s, 255 / 100 * v]


def save_background():
    cap = cv2.VideoCapture(0)

    for _ in range(0, 25):
        cap.read()

    _, frame = cap.read()

    cv2.imwrite('background.png', frame)

    cap.release()

if __name__ == '__main__':
    #main(_convert_hsv(48, 6, 5), _convert_hsv(140, 200, 200))
    main(_convert_hsv(63, 10, 5), _convert_hsv(140, 140, 140))
