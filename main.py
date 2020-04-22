from datetime import datetime

import serial


log_ok_tag = "OK"
log_error_tag = "ERROR"
log_start_tag = "START"
log_stop_tag = "STOP"

try:
    serial_device = "/dev/tty.usbmodem141401"
    baud_rate = "115200"
    ser = serial.Serial(serial_device, baud_rate)

    while True:
        data = {}
        ser_output = ser.readline().decode().strip()
        if ser_output:
            print("{0}: {1}".format(datetime.now(), ser_output))
            raw_data = ser_output.split(',')
            status = raw_data[0]
            if log_ok_tag in status:
                data['status'] = status
                data['temperature'] = raw_data[1]
                data['light'] = raw_data[2]
                data['sound'] = raw_data[3]
                for k, v in data.items():
                    print(k, v, sep=": ", end=", ")
                print()
            elif log_stop_tag in status:
                print("stopped, now exiting")
                break

    if ((serial.VERSION.startswith('2') and ser.isOpen()) or
            (serial.VERSION.startswith('3') and ser.is_open)):
        ser.close()
except Exception as err:
    print("Serial port error:", str(err))
