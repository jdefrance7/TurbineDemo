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

# Serial Port Object
ser = serial.Serial()
ser.baudrate = 9600
SERIAL_ENABLED = False

# Data & Axes Indexes
WIND = 0
VOLTAGE = 1

# Max Values (to Scale Graphs)
MAX_WIND = 30
MAX_VOLTAGE = 6

# Refresh Rate of Matplotlib Animation (ms)
REFRESH = 750

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
        print("\nERROR: Serial port '{}' is not open.".format(ser.port))
        return -1

    # Read returning line of bytes from serial port
    try:
        data = ser.readline()
    except:
        print("\nERROR: Issue reading data '{}'.".format(data))
        return -1

    if DEBUG:
        print("\nDEBUG: Raw data = {}".format(repr(data)))

    # Convert bytes to string
    try:
        data = data.decode("utf-8")
    except:
        print("\nERROR: Issue decoding data '{}'.".format(data))
        return -1

    if DEBUG:
        print("\nDEBUG: Decoded data = {}".format(repr(data)))

    # Strips carriage return and newline from data
    try:
        data = data.rstrip('\r\n')
    except:
        print("\nERROR: Unable to strip trailing data '{}'.".format(data))

    if DEBUG:
        print("\nDEBUG: Stripped data = {}".format(data))

    # Split string into list by delimiter ','
    try:
        data = data.split(',')
    except:
        print("\nERROR: Issue splitting data '{}'.".format(data))
        return -1

    if DEBUG:
        print("\nDEBUG: Split data = {}".format(data))

    # Ensure list is correct length [averageSpeed, averageVoltage]
    if len(data) != 2:
        print("\nERROR: Data is incorrect length '{}'.".format(data))
        return -1

    # Convert list of strings to list of floats
    try:
        for n in range(len(data)):
            data[n] = float(data[n])
    except:
        print("\nERROR: Unable to cast data to float '{}'.".format(data))
        return -1

    if DEBUG:
        print("\nDEBUG: Float casted data = {}".format(data))

    # Return list of float data
    return data

# Matplotlib Animation Function
def animate(i):

    # Get data from serial port
    data = get_data()

    # No data...
    if data == -1:
        return -1

    ax[WIND].clear()
    ax[WIND].set_title('Wind Speed')
    # ax[WIND].set_xlabel()
    ax[WIND].set_ylabel("Meters/Second")
    ax[WIND].set_ylim(bottom = 0, top = MAX_WIND)
    ax[WIND].grid(alpha = GRID_ALPHA)
    ax[WIND].bar(str(data[WIND]), data[WIND])

    ax[VOLTAGE].clear()
    ax[VOLTAGE].set_title("Voltage")
    # ax[VOLTAGE].set_xlabel()
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
        print("\nERROR: Unable to open port '{}' with baudrate '{}'.".format(ser.port, ser.baudrate))
        return -1

    # # Turn on Data Broadcast
    # try:
    #     ser.write('B'.encode("utf-8"))
    # except:
    #     return -1

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
        print("\nERROR: No ports found. Check connection.")
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
            print("\nERROR: Invalid port '{}'.".format(user))
            return -1
        return 0

    # Check if port number was entered
    try:
        user = int(user)-1
    except:
        print("\nERROR: Invalid entry '{}.".format(user))
        return -1

    # Check if port number in valid range
    if 0 < user and user < len(ports)+1:
        try:
            ser.port = ports[user]
        except:
            print("\nERROR: Invalid port '{}'.".format(ports[user]))
            return -1
        return 0

    # Unable to set serial port
    print("\nERROR: Invalid port '{}'.".format(ports[user]))
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
        print("\nERROR: Invalid baudrate '{}'.".format(user))
        return -1

    # Attempt to set baudrate
    try:
        ser.baudrate = user
    except:
        print("\nERROR: Invalid baudrate '{}'.".format(user))
        return -1
    return 0

def test_connection(ser):

    # Open serial port
    try:
        ser.open()
    except:
        print("\nERROR: Unable to open port '{}' with baudrate '{}'.".format(ser.port, ser.baudrate))
        return False

    # # Exit broadcast mode on Arduino (if applicable)
    # try:
    #     ser.write('S'.encode("utf-8"))
    # except:
    #     return False

    # Clear serial input buffer
    while ser.in_waiting:
        ser.read()

    # # Send request for single data pair
    # try:
    #     ser.write('D'.encode("utf-8"))
    # except:
    #     return False

    # Check for return data
    if get_data() == -1:
        print("\nERROR: No response from serial port.")
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
        print("\nERROR: Invalid entry '{}'.".format(user))
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
                print("\nERROR: Exception '{}'.".format(e))
        else:
            print("\nERROR: Serial port must be connected before running demo.")

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
        print("\nERROR: Invalid entry '{}'.".format(user))

    # Return
    return 0

if __name__ == '__main__':
    setup()
    while(1):
        if loop() == -1:
            print("\nExiting demo...\n");
            break;
