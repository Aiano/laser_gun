import cv2.cv2 as cv


def take_a_snap_shot():
    cam = cv.VideoCapture(1)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    cv.namedWindow("Snapshot")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame.")
            break

        resized_frame = cv.resize(frame, (640, 480))
        cv.imshow("Snapshot", resized_frame)

        key = cv.waitKey(1)
        if key % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif key % 256 == 32:
            # SPACE pressed
            img_name = "snapshot_{}.png".format(img_counter)
            cv.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    cv.destroyAllWindows()

    return


if __name__ == '__main__':
    take_a_snap_shot()
