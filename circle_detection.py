import time

import cv2.cv2 as cv
import numpy as np
import command
import math

frame_width = 1280
frame_height = 720
central_roi_width = 640
central_roi_height = 360


def detect_circle(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # gray_blurred = cv.blur(gray, (3, 3))

    # cv.imshow("gray_blurred",gray_blurred)

    _detected_circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=55, minRadius=1,
                                        maxRadius=50)

    return _detected_circles


half_central_roi_width = central_roi_width / 2
half_central_roi_height = central_roi_height / 2
k1 = 0.0012
k2 = 0.0015
x_offset = 0.03
y_offset = 0.018


def compute_angles(x, y):
    delta_x = x - half_central_roi_width
    delta_y = -(y - half_central_roi_height)

    _angle_a = math.atan(k1 * delta_x) + x_offset
    _angle_b = math.atan(k2 * delta_y) + y_offset

    _angle_a = round(_angle_a, 2)
    _angle_b = round(_angle_b, 2)

    return _angle_a, _angle_b


def run_task(_angle_a, _angle_b):
    print("angle_a:%.2f\tangle_b:%.2f" % (_angle_a, _angle_b))
    command.set_angle(_angle_a, _angle_b)
    time.sleep(6)

    # get mean value of distance
    distances = []
    distance = 0
    for i in range(5):
        distance = command.get_distance()

        print(distance)
        if 20 < distance < 8000:
            distances.append(distance)
        time.sleep(0.1)
    if len(distances) == 0:
        distance = 1500
    else:
        distance = np.mean(distances)
    print("distance:" + str(distance) + "\n")

    command.set_laser(True)
    print('Laser ON')
    time.sleep(3.5)
    command.set_laser(False)
    print('Laser OFF')

    command.set_angle(0, 0)
    print("Finished.")


if __name__ == '__main__':
    command.init('COM8')
    command.set_laser(False)
    command.set_angle(0, 0)

    cv.namedWindow("Detected Circle", cv.WINDOW_NORMAL)
    cv.moveWindow("Detected Circle", 100, 100)

    cam = cv.VideoCapture(1)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, frame_width)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, frame_height)

    p1 = [frame_width / 2 - central_roi_width / 2, frame_height / 2 - central_roi_height / 2]
    p2 = [frame_width / 2 + central_roi_width / 2, frame_height / 2 + central_roi_height / 2]
    p1 = np.int_(np.around(p1))
    p2 = np.int_(np.around(p2))

    while True:
        ret, frame = cam.read()

        roi = frame[p1[1]:p2[1], p1[0]:p2[0]]
        # roi = frame
        # cv.imshow("Roi", roi)
        if not ret:
            print("failed to grab frame.")
            break

        detected_circles = detect_circle(roi)
        angle_a, angle_b = 0, 0
        angle_a_list, angle_b_list = [], []

        if detected_circles is not None:
            # Convert the circles parameters a, b and r to intergers
            detected_circles = np.int_(np.around(detected_circles))
            # Unpack the outer list    [[]] -> []
            detected_circles = detected_circles[0]
            for pt in detected_circles:
                a, b, r = pt[0], pt[1], pt[2]
                # a -> x  b -> y

                # draw the circle
                cv.circle(roi, (a, b), r, (0, 255, 0), 2)
                cv.circle(roi, (a, b), 1, (0, 0, 255), 3)

                angle_a, angle_b = compute_angles(a, b)
                angle_a_list.append(angle_a)
                angle_b_list.append(angle_b)
                # print("angle_a:"+str(angle_a)+"\tangle_b:"+str(angle_b))

        # resized_frame = cv.resize(frame, (640, 360))
        cv.imshow("Detected Circle", roi)

        key = cv.waitKey(1)

        if key == ord('q'):
            break
        elif key == ord('1'):
            cv.namedWindow("Task1", cv.WINDOW_NORMAL)
            cv.moveWindow("Task1", 600, 100)
            cv.imshow("Task1", roi)
            cv.waitKey(1)

            if angle_a != 0 or angle_b != 0:
                run_task(angle_a, angle_b)
        elif key == ord('2'):
            cv.namedWindow("Task2", cv.WINDOW_NORMAL)
            cv.moveWindow("Task2", 600, 100)
            cv.imshow("Task2", roi)
            cv.waitKey(1)

            for a, b in zip(angle_a_list, angle_b_list):
                run_task(a, b)
