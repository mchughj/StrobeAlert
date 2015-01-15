import serial
import sys
import time

# Super simple test harness to ensure that the embedded program running on the arduino 
# is functioning.

def main(duration):
    serial_speed = 9600
    serial_port = 'com26'

    print "Establishing the communication with the arduino"

    ser = serial.Serial(serial_port, serial_speed, timeout=1)

    print "Waiting for arduino bootloader to finish"
    time.sleep(2)

    duration = int(duration)
    print "Connected"
    s = "1," + str(duration) + "\n";
    ser.write(s);

    print "Done sending!"
    while( 1 ):
        sys.stdout.write(ser.read())


if __name__ == "__main__":
   if len(sys.argv) == 1:
        main(3000)
   else:
        main(sys.argv[1])

