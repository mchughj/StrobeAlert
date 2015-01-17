import serial
import serial.tools.list_ports
import sys
import time
import httplib

# Super simple test harness to ensure that the embedded program running on the arduino 
# is functioning.

serverInstance = "pechuk.devserver"
serverPort = 8080
defaultAlarmDuration = 10000

def findSerialPort():
    for l in list(serial.tools.list_ports.comports()):
       if l[1].find( "rduino") != -1:
          return l[0]
    
    print "Unable to find arduino in: " + str(list(serial.tools.list_ports.comports()))

def main():
    serial_speed = 9600
    serial_port = findSerialPort()

    print "Establishing the communication with the arduino on " + serial_port

    ser = serial.Serial(serial_port, serial_speed, timeout=1)

    print "Waiting for arduino bootloader to finish"
    time.sleep(2)
    print "Connected"

    while( 1 ):
       try: 
           print "Connecting to " + serverInstance
           connection = httplib.HTTPConnection(serverInstance, serverPort, timeout=30)
           print "Making http request"
           connection.request( "GET", "/" )
           result = connection.getresponse()
       
           print result.status, result.reason

           if result.status == 200: 
               count = int(result.read())
               print "Number of alerts: " + str(count)
               if count > 0:
                   s = "1," + str(defaultAlarmDuration) + "\n";
                   ser.write(s);

       except Exception as e:  
           print "Exception: " + str(e)


       print "Reading from arduino: "
       bytesRead = 0
       while( bytesRead < 4096 ):
           b = ser.read()
           if( b == "" ):
               break
           else:
               print str(b),
           bytesRead = bytesRead + 1

       if bytesRead > 0:
           print

       print "Sleeping"
       time.sleep(10)    



if __name__ == "__main__":
    main()

