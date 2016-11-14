import pyfirmata
import time
import Adafruit_DHT
import serial
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)

gpio.setwarnings(False)
trig= 23
echo=24

gpio.setup(trig,gpio.OUT)
gpio.setup(echo,gpio.IN)
gpio.setup(motorPin,gpio.OUT)

gpio.output(trig,False)

sensor = Adafruit_DHT.DHT11

tempPin = 17
motorPin = 22

board = pyfirmata.Arduino('/dev/ttyACM1')
analog_pin = board.get_pin('a:0:i')
digital_pinRed = board.get_pin('d:13:o')
digital_pinWhite = board.get_pin('d:12:o')
digital_pinYellow = board.get_pin('d:11:o')
digital_pinBlue = board.get_pin('d:10:o')
digital_pinGreen = board.get_pin('d:9:o')
digital_pinBuzzer = board.get_pin('d:8:o')

temp_extreme=30.0
temp_low=20.0

moisture_wet=150
moisture_humid=400
moisture_dry=1000

it = pyfirmata.util.Iterator(board)
it.start()
analog_pin.enable_reporting()

while True:
	humidity, temp = Adafruit_DHT.read_retry(sensor, tempPin)
	moisture = analog_pin.read()
	moisture=moisture*1000
	
	#gpio.output(trig,True)
	#time.sleep(0.00001)
	#gpio.output(trig,False)
	
	#while gpio.input(echo) == 0:
	#	pulse_start = time.time()

	#while gpio.input(echo) == 1:
	#	pulse_end = time.time()

	#pulse_duration= pulse_end - pulse_start
	#distance = pulse_duration*17150
	#distance = round(distance,2)

	if temp is not None and moisture is not None:
		print 'Temp={0:0.1f}*C'.format(temp)
		print('Moisture=%f'%moisture)
	else:
		print 'Failed to get reading. Try again!'

	if temp<=temp_low:
		if moisture>=moisture_dry:
			digital_pinYellow.write(1)
			time.sleep(1)
			digital_pinYellow.write(0)
			
			gpio.output(motorPin,True)
			time.sleep(6)
			gpio.output(motorPin,False)

		if moisture<moisture_dry and moisture >= moisture_humid:		
			digital_pinWhite.write(1)
			time.sleep(1)
			digital_pinWhite.write(0)
			
			gpio.output(motorPin,True)
			time.sleep(4)
			gpio.output(motorPin,False)

		if moisture >= moisture_wet and moisture<moisture_humid:
			digital_pinRed.write(1)
			time.sleep(1)
			digital_pinRed.write(0)
			
			gpio.output(motorPin,True)
			time.sleep(2)
			gpio.output(motorPin,False)

	if temp<temp_extreme and temp>temp_low:
		if moisture>=moisture_dry:
			digital_pinBlue.write(1)
			time.sleep(1)
			digital_pinBlue.write(0)
			
			gpio.output(motorPin,True)
			time.sleep(8)
			gpio.output(motorPin,False)

		if moisture<moisture_dry and moisture >= moisture_humid:		
			digital_pinYellow.write(1)
			time.sleep(1)
			digital_pinYellow.write(0)
			
			gpio.output(motorPin,True)
			time.sleep(6)
			gpio.output(motorPin,False)

		if moisture >= moisture_wet and moisture<moisture_humid:
			digital_pinWhite.write(1)
			time.sleep(1)
			digital_pinWhite.write(0)
			
			gpio.output(motorPin,True)
			time.sleep(4)
			gpio.output(motorPin,False)

	if temp>=temp_extreme:
		if moisture>moisture_dry:
			digital_pinGreen.write(1)
			time.sleep(1)
			digital_pinGreen.write(0)
			
			gpio.output(motorPin,True)
			time.sleep(10)
			gpio.output(motorPin,False)

		if moisture<moisture_dry and moisture>=moisture_humid:		
			digital_pinBlue.write(1)
			time.sleep(1)
			digital_pinBlue.write(0)
			
			gpio.output(motorPin,True)
			time.sleep(8)
			gpio.output(motorPin,False)

		if moisture>=moisture_wet and moisture<moisture_humid:
			digital_pinYellow.write(1)
			time.sleep(1)
			digital_pinYellow.write(0)
			
			gpio.output(motorPin,True)
			time.sleep(6)
			gpio.output(motorPin,False)

	Wlevel=300-distance
	
	while Wlevel<50:
		digital_pinBuzzer.write(1)
		time.sleep(0.5)
		digital_pinBuzzer.write(0)
		time.sleep(0.5)
