# Serial Packages
import sys
import glob
import serial

# Matplotlib Packages
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import numpy as np

# Time Packages
from datetime import datetime
from datetime import timedelta

# Arduino Commands
TEST_CONNECTION = 0
GET_AVERAGE_SPEED = 1
GET_AVERAGE_VOLTAGE = 2
CLEAR_BUFFERS = 3
GET_SPEED_BUFFER = 4
GET_VOLTAGE_BUFFER = 5

# Returns Available Serial Ports
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# Serial Port Object
ser = serial.Serial();

# Matplotlib Setup
mplstyle.use('dark_background')
fig, ax = plt.subplots(nrows = 1, ncols = 2)
fig.suptitle('Wind Turbine Demo')

# Matplotlib Animation Function
def animate(i):
    # TODO: read & plot data
    return

def testConnection():
    try:
        ser.open()
        # TODO: Send TEST_CONNECTION and check response.
        ser.close()
    except:
        return "Disconnected"
    else:
        return "Connnected"

def runDemo():

    return 0

def configureSerial():

    while(1):
        print("\nSERIAL INFORMATION: ")
        print("PORT: ".format(ser.port))
        print("BAUD: ".format(ser.baudrate))
        print("TEST: ".format(testConnection()))

        user = input("\nCOMMAND: ");

        if user == "PORT":
            # TODO: Configure Port
        elif user == "BAUD":
            # TODO: Configure Baudrate
        elif user == "TEST":
            # TODO: Test Connection
        elif user == "HELP":
            # TODO: Print Help Info
        else:
            print("ERROR: Invalid command '{}'".format(user))

    return 0

def setup():
    print("Welcome to the Innovative Engineer's Wind Turbine Demo!")
    print("Navigate by entering commands in the terminal.")
    print("Type 'HELP' at anytime to get information.")
    return 0

# Main Loop (Command Line Style)
def loop():

    # Print Ready Status
    # TODO: status flag after setup

    # Get Command From User
    user = input("\nCOMMAND: ")

    '''
        Supported Commands:
            - RUN
            - SETUP
            - HELP
    '''

    # COMMAND: RUN
    if user == "RUN":
        runDemo()

    # COMMAND: SETUP
    elif user == "SETUP":
        configureSerial()

    # COMMAND: HELP
    elif user == "HELP":
        print("Supported Commands: ")
        print("  RUN - Runs demo if serial port is configured. Enter 'QUIT' to stop.")
        print("  SETUP - Menu to configure serial port.")
        print("  HELP - Lists supported commands.")

    # INVALID COMMAND
    else:
        print("ERROR: Invalid command '{}'".format(user))
        print("NOTE: Enter 'HELP' to get list of supported commands.")

    return 0

if __name__ == '__main__':
    setup()
    while(1):
        loop()
