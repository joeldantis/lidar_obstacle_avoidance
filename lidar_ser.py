import time
import serial

# Replace with your serial port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux)
PORT = "/dev/ttyUSB0"
BAUDRATE = 115200

# Open the serial port
ser = serial.Serial(
    port=PORT,
    baudrate=BAUDRATE,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1.0,
)

# Clear any residual data in the buffers
ser.reset_input_buffer()
ser.reset_output_buffer()

# 1. Send STOP command: 0xA5 0x25
ser.write(b"\xA5\x25")
time.sleep(0.02)  # Allow LIDAR to transition to Idle

# 2. Send GET_HEALTH command: 0xA5 0x52
ser.write(b"\xA5\x52")

# Read the 7-byte response descriptor
response_descriptor = ser.read(7)
print("Response Descriptor:", response_descriptor.hex())

# Read the 3-byte GET_HEALTH payload (status and error code)
health_data = ser.read(3)
print("Health Data:", health_data.hex())

# 3. Send SCAN command: 0xA5 0x20
ser.write(b"\xA5\x20")

# Read the 7-byte scan response descriptor
scan_descriptor = ser.read(7)
print("Scan Descriptor:", scan_descriptor.hex())

# Continuously read 5-byte scan measurement sample packets
try:
    for _ in range(10):  # read first 10 sample packets
        sample = ser.read(5)
        print("Sample Data:", sample.hex())
finally:
    # Always send STOP before closing
    ser.write(b"\xA5\x25")
    ser.close()