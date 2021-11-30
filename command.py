import uart
import time


def init(port):
    uart.init_serial(port)


def set_angle(motor_a, motor_b):
    uart.send('A' + str(motor_a) + '\n')
    uart.send('B' + str(motor_b) + '\n')


def set_laser(status):
    if status is True:
        uart.send('LO\n')
    else:
        uart.send('LF\n')


def get_distance():
    uart.send('D\n')
    _distance = uart.receive()
    if len(_distance) != 0:
        _distance = _distance.strip("distance:")
        return int(_distance)
    else:
        return 0


if __name__ == '__main__':
    init('COM8')

    while True:
        # set_laser(True)
        # set_angle(0.3, 0.3)
        # time.sleep(3)
        #
        # set_laser(False)
        # set_angle(-0.3, -0.3)
        # time.sleep(3)
        distance = get_distance()
        print(distance)
        time.sleep(0.1)
