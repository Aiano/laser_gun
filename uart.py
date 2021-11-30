import serial
import time

ser = None


def init_serial(port, baud_rate=115200, timeout=50):
    global ser
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    print("Port:" + port)


def receive_loop():
    line = ser.readline(10)
    if line is not None:
        print("Receive:" + line)
        return line
    else:
        return None


def receive():
    data = ser.read_all()
    if data is not None:
        data = data.decode(encoding="utf-8")
        enter_index = data.find('\n')
        data = data[:enter_index]
        print(data)
        return data
    return None

def send(data):
    ser.write(data.encode(encoding="utf-8"))


def de_init_serial():
    ser.close()


if __name__ == '__main__':
    init_serial('COM9')

    while True:
        send('L\n')
        send('B0.2\n')
        time.sleep(3)

        send('D\n')
        receive()

        time.sleep(1)
        send('B-0.2\n')

        time.sleep(3)
