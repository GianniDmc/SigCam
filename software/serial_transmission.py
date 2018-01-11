import serial
import time
from time import gmtime, strftime
import struct

def serialsending(texttosend, port):

	dmm = serial.Serial('/dev/'+port+'')
	#dmm = serial.Serial(port='/dev/tty.usbserial-A700f1sK',baudrate=9600,bytesize=8,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,)
	#handling exceptions


	dmm.close()
	try:
		dmm.open()
	except Exception, e:
		print "problem while openning the port : " +str(e)
		exit()
	#print(dmm.name)         # check which port was really used

	print "Blabla"
	print "-------------------------------------------------------"
	dmm.isOpen()

		#file = open("/", "a")

	while True:

		dmm.write("AT+SF="+texttosend+""+'\r\n')

		#dmm.flushInput()


		#data = dmm.read(14)
		#if data == '':

		dmm.close()
	else:

		#print data

		time.sleep(1)
		#print >>file,data,' -> ',strftime("%d %b %Y,%H:%M:%S")

		#file.flush()

		#file.close()