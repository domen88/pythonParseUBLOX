import serial
import signal 
import sys
import socket

#Open Serial Port
ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 115200

#TODO: open file in append? or write?
text_file = open("position.txt", 'w')

#Open Socket
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = ('0.0.0.0', 54321)
#s.bind(server_address)
#s.listen(1)

#register handler Ctrl-C
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
	#close the serial connection and text file
	text_file.write("\n")
	text_file.close()
	#ser.close()
	#s.close()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#signal.pause()

while 1:
	#print >> sys.stderr, '\nWaiting for a connection...\n'
	#connection, client_address = s.accept()	
	#try:
	#print 'Client connesso '

	x=ser.readline() #read LINE
	#x=ser.read() #read ONE

	#s.sendall(x)
	#connection.recv();

	#DEBUG
	#print x

	text_file.write(x)
	text_file.flush()

	#finally:
	#       connection.close()
