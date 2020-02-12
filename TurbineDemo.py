# Logging Package
import logging

# Serial Package
import serial

# Serial Support Packages
import sys
import glob

# Matplotlib Packages
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib.animation as animation
import numpy as np

# Debug Flag
DEBUG = True

# Log Setup
log = logging.getLogger('TurbineDemo')
log.setLevel(logging.DEBUG)
sth = logging.StreamHandler()
sth.setLevel(logging.DEBUG)
fmt = logging.Formatter('\n%(levelname)s: %(message)s')
sth.setFormatter(fmt)
log.addHandler(sth)

# Serial Port Object
ser = serial.Serial()
ser.baudrate = 9600
SERIAL_ENABLED = False

# Data & Axes Indexes
DATA_LENGTH = 2
WIND = 0
VOLTAGE = 1

# Max Values (to Scale Graphs)
MAX_WIND = 10
MAX_VOLTAGE = 4

# Refresh Rate of Matplotlib Animation (ms)
REFRESH = 1000

# Matplotlib Grid Strength
GRID_ALPHA = 0.2

# Returns Available Serial Ports
def serial_ports():
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

# Matplotlib Setup
mplstyle.use('dark_background')
fig, ax = plt.subplots(nrows = 1, ncols = 2)
fig.suptitle('Wind Turbine Demo')

def get_data():

    # Check if serial port is open
    if ser.isOpen() == False:
        log.error("Serial port {} is not open.".format(ser.port))
        return -1

    # Clear Input Buffer
    while(ser.in_waiting):
        try:
            ser.readline()
        except:
            log.error("Unable to clear input buffer.")
            return -1

    # Read new line of bytes from serial port
    try:
        data = ser.readline()
    except:
        log.error("Issue reading data '{}'.".format(data))
        return -1

    log.debug("Raw data = {}.".format(repr(data)))

    # Convert bytes to string
    try:
        data = data.decode("utf-8")
    except:
        log.error("Issue decoding data '{}'.".format(data))
        return -1

    log.debug("Decoded data = {}.".format(repr(data)))

    # Strips carriage return and newline from data
    try:
        data = data.rstrip('\r\n')
    except:
        log.error("Unable to strip trailing data.")
        return -1

    log.debug("Stripped data = {}.".format(data))

    # Split string into list by delimiter ','
    try:
        data = data.split(',')
    except:
        log.error("Issue splitting data '{}'.".format(data))
        return -1

    log.debug("Split data = {}.".format(data))

    # Ensure list is correct length [averageSpeed, averageVoltage]
    if len(data) != DATA_LENGTH:
        log.error("Data is incorrect length '{}'.".format(data))
        return -1

    # Convert list of strings to list of floats
    try:
        for index, value in enumerate(data):
            data[index] = float(value)

    except:
        log.error("Unable to cast data to float '{}'.".format(data))
        return -1

    log.debug("Float casted data = {}.".format(data))

    # Return list of float data
    return data

# Matplotlib Animation Function
def animate(i):

    # Get data from serial port
    data = get_data()

    # No data...
    if data == -1:
        log.debug("Unable to read data for plotting.")
        return -1

    ax[WIND].clear()
    ax[WIND].set_title('Wind Speed')
    ax[WIND].set_xlabel("Value")
    ax[WIND].set_ylabel("Meters/Second")
    ax[WIND].set_ylim(bottom = 0, top = MAX_WIND)
    ax[WIND].grid(alpha = GRID_ALPHA)
    ax[WIND].bar(str(data[WIND]), data[WIND])

    ax[VOLTAGE].clear()
    ax[VOLTAGE].set_title("Voltage")
    ax[VOLTAGE].set_xlabel("Value")
    ax[VOLTAGE].set_ylabel("Volts")
    ax[VOLTAGE].set_ylim(bottom = 0, top = MAX_VOLTAGE)
    ax[VOLTAGE].grid(alpha = GRID_ALPHA)
    ax[VOLTAGE].bar(str(data[VOLTAGE]), data[VOLTAGE])

    return 0

def run_demo():

    # Open Serial Port
    try:
        ser.open()
    except:
        log.error("Unable to open port '{}' with baudrate '{}'.".format(ser.port, ser.baudrate))
        return -1

    ani = animation.FuncAnimation(fig, animate, interval = REFRESH)

    plt.show()

    user = input("\nPRESS ENTER TO QUIT")

    ser.close()

    return 0

def demo_status():
    if SERIAL_ENABLED:
        return "AVAILABLE"
    return "UNAVAILABLE"

def port_status():
    if SERIAL_ENABLED:
        return "CONNECTED"
    return "DISCONNECTED"

def set_port(ser):

    # Get list of available serial ports
    ports = serial_ports()

    # If no ports were found
    if len(ports) == 0:
        log.error("No ports found. Check connection.")
        return -1

    # Print available ports with numbered list
    print("\nAVAILABLE PORTS:\n")
    for n in range(1, len(ports)+1):
        print(" {}. {}".format(n, ports[n-1]))

    # Get user selection
    user = input("\nPORT: ")

    # Check if port name was enetered
    if user in ports:
        try:
            ser.port = user
        except:
            log.error("Invalid port '{}'.".format(user))
            return -1
        return 0

    # Check if port number was entered
    try:
        user = int(user)
        user = user-1
    except:
        log.error("Invalid entry '{}'.".format(user))
        return -1

    # Check if port number in valid range
    if 0 < user and user < len(ports)+1:
        try:
            ser.port = ports[user]
        except:
            log.error("Invalid port '{}'.".format(ports[user]))
            return -1
        return 0

    # Unable to set serial port
    log.error("Invalid port '{}'".format(ports[user]))
    return -1

def set_baudrate(ser):

    # List of standard Arduino baudrates
    baudrates = (300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200)

    # Print baudrates
    print("\nSTANDARD BAUDRATES:\n")
    for baud in baudrates:
        print(baud)

    # Get user selection
    user = input("\nBAUDRATE: ")

    # Attempt to get baudrate
    try:
        user = int(user)
    except:
        log.error("Invalid baudrate '{}'.".format(user))
        return -1

    # Attempt to set baudrate
    try:
        ser.baudrate = user
    except:
        log.error("Invalid baudrate '{}'.".format(user))
        return -1
    return 0

def test_connection(ser):

    # Open serial port
    try:
        ser.open()
    except:
        log.error("Unable to open port '{}' with baudrate '{}'.".format(ser.port, ser.baudrate))
        return False

    # Clear serial input buffer
    while ser.in_waiting:
        ser.read()

    # Check for return data
    if get_data() == -1:
        log.error("No response from serial port.")
        return False

    ser.close()

    return True

def setup():
    # Welcome message, prints once upon execution
    print("\nWelcome to the Innovative Engineer's Wind Turbine Demo!")
    print("Navigate by entering option numbers or values in the terminal.")
    return 0

def loop():

    # Global flag for serial connectoin
    global SERIAL_ENABLED

    # Print options
    print("\nMAIN MENU:\n")
    print("  1. DEMO [{}]".format(demo_status()))
    print("  2. TEST [{}]".format(port_status()))
    print("  3. PORT [{}]".format(ser.port))
    print("  4. BAUD [{}]".format(ser.baudrate))

    # Get user input
    user = input("\nENTER: ")

    # Dictionary of input options
    options = {
        "DEMO": 1,
        "TEST": 2,
        "PORT": 3,
        "BAUD": 4
    }

    # Check if command was entered
    if user in options.keys():
        user = options[user]

    # Convert to number
    try:
        user = int(user)
    except:
        log.error("Invalid entry '{}'.".format(user))
        return -1

    # Quit execution
    if user == -1:
        return -1

    # Run the demo
    elif user == 1:
        if SERIAL_ENABLED:
            try:
                run_demo()
            except Exception as e:
                log.error("Exception '{}'.".format(e))
        else:
            log.error("Serial port must be connected before running demo.")

    # Test connection with Arduino
    elif user == 2:
        SERIAL_ENABLED = test_connection(ser)

    # Set serial port on device
    elif user == 3:
        set_port(ser)

    # Set baudrate on device
    elif user == 4:
        set_baudrate(ser)

    # Unrecognized input
    else:
        log.error("Invalid entry '{}'.".format(user))

    # Return
    return 0

if __name__ == '__main__':
    setup()
    while(1):
        if loop() == -1:
            log.info("Exiting demo...\n")
            break;
