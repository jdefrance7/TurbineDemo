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
TEST_RESPONSE   = 0x3
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
ser = serial.Serial()
SERIAL_ENABLED = False

# Matplotlib Setup
mplstyle.use('dark_background')
fig, ax = plt.subplots(nrows = 1, ncols = 2)
fig.suptitle('Wind Turbine Demo')

# Matplotlib Animation Function
def animate(i):
    # TODO: read & plot data
    return

def configurePort():
    while(1):
        ports = serial_ports()
        print("\nPORTS: ")
        for n in range(len(ports)):
            print(" {}. {}".format(n, ports[n]))
        user = input("\n SELECT: ")

        if user == "HELP":
            print("HELP: Enter port number from list or type port name.")
        elif user == "EXIT":
            return 0
        elif user in ports:
            try:
                ser.port = user
            except:
                print("ERROR: Unable to set port to '{}'.".format(user))
            else:
                return 0
        else:
            try:
                user = int(user)
            except:
                print("ERROR: Invalid entry '{}''.".format(user))
            else:
                if user < len(ports):
                    try:
                        ser.port = ports[user]
                    except:
                        print("ERROR: Unable to set port to '{}'.".format(ports[user]))
                    else:
                        return 0
                else:
                    print("ERROR: Entry outside of range.")
    return 0

def configureBaudrate():
    while(1):
        baudrates = BAUDRATES
        print("\nBAUDRATES: ")
        for n in range(len(baudrates)):
            print(" {}. {}".format(n, baudrates[n]))
        user = input("\n SELECT: ")

        if user == "HELP":
            print("HELP: Enter baudrate number from list or type baudrate value.")
        elif user == "EXIT":
            return 0
        else:
            try:
                user = int(user)
            except:
                print("ERROR: Invalid entry '{}'.".format(user))
            else:
                if 0 < user and user < len(baudrates):
                    try:
                        ser.baudrate = baudrates[user]
                    except:
                        print("ERROR: Unable to set baudrate to '{}'.".format(baudrates[user]))
                    else:
                        return 0
                elif user > len(baudrates):
                    try:
                        ser.baudrate = user
                    except:
                        print("ERROR: Unable to set baudrate to '{}'.".format(user))
                    else:
                        return 0
                else:
                    print("ERROR: Invalid entry '{}'.".format(user))
    return 0

def testConnection():
    try:
        ser.open()
    except:
        print("ERROR: Unable to open port '{}' with baud '{}'".format(ser.port, ser.baudrate))
        SERIAL_ENABLED = False
    else:
        try:
            ser.write(bytes([TEST_CONNECTION]))
            time.sleep(1)
            if ser.in_waiting:
                data = int.from_bytes(ser.read(), 'little')
                if data == TEST_RESPONSE:
                    print("OKAY: Serial port connected.")
                    SERIAL_ENABLED = True
                else:
                    print("ERROR: Response '{}' did not match expected '{}'".format(data, TEST_RESPONSE))
                    SERIAL_ENABLED = False
            else:
                print("ERROR: No response from serial port.")
                SERIAL_ENABLED = False
        except:
            print("ERROR: A problem occured during serial transmission.")
            SERIAL_ENABLED = False
        finally:
            ser.close()

    return SERIAL_ENABLED

def runDemo():

    return 0

def configureSerial():
    while(1):
        print("\nSERIAL INFORMATION: ")
        print("PORT: {}".format(ser.port))
        print("BAUD: {}".format(ser.baudrate))
        print("TEST: {}".format(SERIAL_ENABLED)

        user = input("\nCOMMAND: ");

        if user == "PORT":
            configurePort()
        elif user == "BAUD":
            configureBaudrate()
        elif user == "TEST":
            testConnection()
        elif user == "HELP":
            print("Supported Commands: ")
            print("  PORT - Select port from available list.")
            print("  BAUD - Select baudrate from available list.")
            print("  TEST - Test connection with port and baudrate.")
            print("  HELP - Prints list of supported commands.")
            print("  EXIT - Return to main menu.")
        elif user == "EXIT":
            return
        else:
            print("ERROR: Invalid command '{}'".format(user))

    return 0

def setup():
    print("Welcome to the Innovative Engineer's Wind Turbine Demo!")
    print("Navigate by entering commands in the terminal.")
    print("Type 'HELP' at anytime to get menu information.")
    return 0

# Main Loop (Command Line Style)
def loop():

    # Print Ready Status
    if SERIAL_ENABLED:
        print("STATUS: READY")
    else:
        print("STATUS: NOT READY")

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
        print("  RUN - Runs demo if serial port is configured.")
        print("  SETUP - Menu to configure serial port and test connection.")
        print("  HELP - Lists supported commands.")

    # INVALID COMMAND
    else:
        print("ERROR: Invalid command '{}'".format(user))
        print("INFO: Enter 'HELP' to get list of supported commands.")

    # Return
    return 0

if __name__ == '__main__':
    setup()
    while(1):
        loop()
