from datetime import datetime

import argparse
import serial

from api_request import ApiRequest
from config import config


def cpx_device():
    default_cpx_device = "cpx1"

    while True:
        print()

        cpx_device = input(f"Enter CPX device name (D for {default_cpx_device}): ").strip()

        if not cpx_device:
            print("Please enter a name for the CPX device.")
        elif cpx_device.upper() == "D":
            cpx_device = default_cpx_device
            break
        else:
            break

    return cpx_device


def serial_device():
    default_serial_device = "/dev/tty.usbmodem141401"

    while True:
        print()

        serial_device = input("Enter serial device name "
                              f"(D for {default_serial_device}): ").strip()

        if not serial_device:
            print("Please enter a name for the serial device.")
        elif serial_device.upper() == "D":
            serial_device = default_serial_device
            break
        else:
            break

    return serial_device


def baud_rate():
    default_baud_rate = "115200"

    while True:
        print()

        baud_rate = input(f"Enter baud rate (D for {default_baud_rate}): ").strip()

        if not baud_rate:
            print("Please enter an value for the baud rate.")
        elif baud_rate.upper() == "D":
            baud_rate = default_baud_rate
            break
        else:
            break
    
    return baud_rate


def env():
    parser = argparse.ArgumentParser(description='Run the script with the specified configuration environment. ' 
                                                 'Example environment values are dev and prod. The default is dev.')
    parser.add_argument('--env', default='dev', help='set the configuration environment e.g. prod (default is dev)')
    args = parser.parse_args()
    env = args.env
    print("Configuration environment:", env)

    return env


def log_data(data):
    host = config[env]['host']
    port = config[env]['port']
    path = config[env]['path']
    url = 'https://' + host + ':' + port + path

    try:
        data['temperature'] = float(data['temperature'])
    except:
        data['temperature'] = ''

    try:
        data['light'] = float(data['light'])
    except:
        data['light'] = ''

    try:
        data['sound'] = float(data['sound'])
    except:
        data['sound'] = ''

    data['humidity'] = ''
    data['device'] = cpx_device
    data['key'] = config[env]['key']

    print("LOGGING DATA")
    print("Post request to:", url)
    response = ApiRequest.make_api_post_request(url, data, verify=(False if env == 'dev' else True))
    print("Response:", response)

    return response


def process_serial_output(ser_output):
    print("SERIAL OUTPUT")
    print("{0}: {1}".format(datetime.now(), ser_output))

    data = {}
    raw_data = ser_output.split(',')
    data['status'] = raw_data[0]

    if log_ok_tag in data['status']:
        data['temperature'] = raw_data[1]
        data['light'] = raw_data[2]
        data['sound'] = raw_data[3]
        
    return data


def run():
    print()
    print("CPX device:", cpx_device)
    print("Serial device:", serial_device)
    print("Baud rate:", baud_rate)
    print()

    try:
        ser = serial.Serial(serial_device, baud_rate)

        while True:
            ser_output = ser.readline().decode().strip()
            if ser_output:
                data = process_serial_output(ser_output)
                if data['status'] == log_ok_tag:
                    log_data(data)
                    print()
                elif data['status'] == log_start_tag:
                    print("LOGGING STARTED")
                    print()
                elif data['status'] == log_stop_tag:
                    print("LOGGING STOPPED")
                    break

        if ((serial.VERSION.startswith('2') and ser.isOpen()) or
                (serial.VERSION.startswith('3') and ser.is_open)):
            ser.close()
            print("serial port closed")
            print("exiting script")
    except Exception as err:
        print("Serial port error:", str(err))


env = env()
log_ok_tag = "OK"
log_start_tag = "START"
log_stop_tag = "STOP"
cpx_device = cpx_device()
serial_device = serial_device()
baud_rate = baud_rate()

run()