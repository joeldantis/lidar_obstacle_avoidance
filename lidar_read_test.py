import time
from custom_libs.rplidar_parser import RPLidarParser
import serial

# Configure to your specific port (e.g., '/dev/ttyUSB0' or 'COM3')
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200  # Default for A1/A2. Note: A3/S1/S2 may use 256000 or 460800

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
parser = RPLidarParser()

ser.dtr = False
time.sleep(0.5)

#Clean Buffer
ser.reset_input_buffer()
ser.reset_output_buffer()

#ser.write(b"\xA5\x20")
#time.sleep(200)

ser.write(b"\xA5\x20")

#for i in range(2000):
while True:
    print(parser.feed_byte(ser.read(5)))

'''while True:
    ser.dtr = True
    time.sleep(0.5)
    ser.write(b"\xA5\x25")'''