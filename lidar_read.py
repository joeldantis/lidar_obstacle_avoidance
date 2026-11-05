from rplidar import RPLidar

# Connect to the LiDAR on its serial port
# Set your baud rate here (usually 115200 for A1/A2)
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME, baudrate=115200)

try:
    print('Fetching LiDAR info...')
    info = lidar.get_info()
    print(f"Model: {info['model']}, Firmware: {info['firmware']}")
    
    print('Reading sensor data. Press Ctrl+C to stop.')
    
    # iter_scans() automatically processes the raw binary data packet stream
    for i, scan in enumerate(lidar.iter_scans()):
        print(f"\n--- Scan #{i} ---")
        # Each scan contains a list of points: (quality, angle, distance_in_mm)
        #for quality, angle, distance in scan[:5]: # Print the first 5 points of each rotation
        #print(f"Angle: {angle:6.2f}° | Distance: {distance:7.2f} mm | Quality: {quality}")
        print(scan)
            
except KeyboardInterrupt:
    print('Stopping stream...')
finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
