#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import threading
import logging
from multiprocessing import Queue
import time
#import serial


# from rpi_ws281x import *
# import argparse

#set serial

#set = serial.Serial ("/dev/ttyS0", 9600)
#def setup_rs(port, baudrate=9600, timeout=1):
#  ser = serial.Serial(
#  port=port,
#  baudrate=baudrate,
#  bytesize=serial.EIGHTBITS,
#  parity=serial.PARITY_NONE,
#  stopbit=serial.STOPBITS_ONE,
#  timeout=timeout
#  )
#  return ser
#  print(serial.)

#def receive_rs(ser):
#  if  ser.is_open:
#    data = ser.read(ser.in_waiting or 1).decode('utf-8')
#    if data:
#      print(f"Data receive {data}")
#    return data
#  else:
#    print("port failed")
#    return None

#def rsSerial():
#  rs_port = '/dev/ttyS0'
#  baudrate = 9600
#  ser = setup_rs(rs_port, baudrate)
#  try:
#    if ser.is_open:
#      print("Port serial terbuka")
#    else: 
#      ser.open()
#      print("port serial dibuka")
 #   receive_rs(ser)
#  except Exception as e:
#    print(f"terjadi kesalahan: {e}")
#  finally: 
#    if ser.is_open:
#      ser.close()
#      print("Port serial ditutup")


#set gpio mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#set input pin
GPIO.setup(6, GPIO.IN,pull_up_down=GPIO.PUD_UP)  # DIN 1
GPIO.setup(7, GPIO.IN,pull_up_down=GPIO.PUD_UP)  # DIN 2
GPIO.setup(8, GPIO.IN,pull_up_down=GPIO.PUD_UP)  # DIN 3
GPIO.setup(9, GPIO.IN,pull_up_down=GPIO.PUD_UP)  # DIN 4
GPIO.setup(10, GPIO.IN,pull_up_down=GPIO.PUD_UP) # DIN 5
GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP) # LM1
GPIO.setup(13, GPIO.IN,pull_up_down=GPIO.PUD_UP) # LM2
GPIO.setup(25, GPIO.IN,pull_up_down=GPIO.PUD_UP) # DIN 6

#set output pin
GPIO.setup(17, GPIO.OUT) # RELAY 1
GPIO.setup(26, GPIO.OUT) # RELAY 2
GPIO.setup(22, GPIO.OUT) # RELAY 3
GPIO.setup(23, GPIO.OUT) # RELAY 4
GPIO.setup(24, GPIO.OUT) # RELAY 5


GPIO.setup(27, GPIO.OUT) # BUZZER
GPIO.setup(16, GPIO.OUT) # INDICATOR 1
GPIO.setup(19, GPIO.OUT) # INDICATOR 2
GPIO.setup(20, GPIO.OUT) # INDICATOR 3

# LED strip configuration:
LED_COUNT      = 30     # Number of LED pixels.
LED_PIN        = 26      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0     # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.
# def colorWipe(strip, color, wait_ms=50):
#     """Wipe color across display a pixel at a time."""
#     for i in range(strip.numPixels()):
#         strip.setPixelColor(i, color)
#         strip.show()
#         time.sleep(wait_ms/1000.0)

# def theaterChase(strip, color, wait_ms=50, iterations=10):
#     """Movie theater light style chaser animation."""
#     for j in range(iterations):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, color)
#             strip.show()
#             time.sleep(wait_ms/1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, 0)

# def wheel(pos):
#     """Generate rainbow colors across 0-255 positions."""
#     if pos < 85:
#         return Color(pos * 3, 255 - pos * 3, 0)
#     elif pos < 170:
#         pos -= 85
#         return Color(255 - pos * 3, 0, pos * 3)
#     else:
#         pos -= 170
#         return Color(0, pos * 3, 255 - pos * 3)

# def rainbow(strip, wait_ms=20, iterations=1):
#     """Draw rainbow that fades across all pixels at once."""
#     for j in range(256*iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((i+j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)

# def rainbowCycle(strip, wait_ms=20, iterations=5):
#     """Draw rainbow that uniformly distributes itself across all pixels."""
#     for j in range(256*iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)

# def theaterChaseRainbow(strip, wait_ms=50):
#     """Rainbow movie theater light style chaser animation."""
#     for j in range(256):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, wheel((i+j) % 255))
#             strip.show()
#             time.sleep(wait_ms/1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, 0)

class inputPort(threading.Thread):
  def __init__(self, queue_t):
    threading.Thread.__init__(self)
    self.daemon = True
    self.queue_ = queue_t
    self.setName = "inputProcessor"
    self.start()

  def run(self):
    index = 0
    while True:
      DIN1 = GPIO.input(6)
      DIN2 = GPIO.input(7)
      DIN3 = GPIO.input(8)
      DIN4 = GPIO.input(9)
      DIN5 = GPIO.input(10)
      DIN6 = GPIO.input(25)

      LM1 = GPIO.input(12)
      LM2 = GPIO.input(13)
      if DIN1 == 0:
        print("DIN 1", GPIO.input(6)) # DIN 1
      elif DIN2 == 0:
        print("DIN 2", GPIO.input(7)) # DIN 2
      elif DIN3 == 0:
        print("DIN 3", GPIO.input(8)) # DIN 3
      elif DIN4 == 0:
        print("DIN 4", GPIO.input(9)) # DIN 4
      elif DIN5 == 0:
        print("DIN 5", GPIO.input(10)) # DIN 5
      elif DIN6 == 0:
        print("DIN 6", GPIO.input(25)) # DIN 6 
      elif LM1 == 0:
        print("LM1", GPIO.input(12)) # LM1
      elif LM2 == 0:
        print("LM2", GPIO.input(13)) # LM2
      time.sleep(0.1)
      pass
class outputPort(threading.Thread):
  def __init__(self, queue_t):
    threading.Thread.__init__(self)
    self.daemon = True
    self.queue_ = queue_t
    self.setName = "outputController"
    self.start()

  def run(self):        
    index = 0
    while True:
      GPIO.output(17, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(26, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(22, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(23, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(24, GPIO.HIGH)
      time.sleep(0.1)    
      GPIO.output(16, GPIO.HIGH)
      time.sleep(0.1)    
      GPIO.output(19, GPIO.HIGH)
      time.sleep(0.1)    
      GPIO.output(20, GPIO.HIGH)
      time.sleep(0.1)    
    
      GPIO.output(17, GPIO.LOW)
      GPIO.output(26, GPIO.LOW)
      GPIO.output(22, GPIO.LOW)
      GPIO.output(23, GPIO.LOW)
      GPIO.output(24, GPIO.LOW) 
      time.sleep(0.1)

if __name__ == "__main__":
  try: 
    queue = Queue()  
    inputPort(queue)
    outputPort(queue)
#  rsSerial()
    buz = GPIO.PWM(27,1000)

    while 1:
      buz.start(50)
      time.sleep(.5)
      buz.stop()
      time.sleep(.5)
       
  except KeyboardInterrupt:
    GPIO.cleanup()
    buz.stop()
 


#   parser = argparse.ArgumentParser()
#   parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
#   args = parser.parse_args()

#   # Create NeoPixel object with appropriate configuration.
#   strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
#   # Intialize the library (must be called once before other functions).
#   strip.begin()

#   print ('Press Ctrl-C to quit.')
#   if not args.clear:
#     print('Use "-c" argument to clear LEDs on exit')
#   try:
#     while True:
#       print ('Color wipe animations.')
#       colorWipe(strip, Color(255, 0, 0))  # Red wipe
#       colorWipe(strip, Color(0, 255, 0))  # Blue wipe
#       colorWipe(strip, Color(0, 0, 255))  # Green wipe
#       print ('Theater chase animations.')
#       theaterChase(strip, Color(127, 127, 127))  # White theater chase
#       theaterChase(strip, Color(127,   0,   0))  # Red theater chase
#       theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
#       print ('Rainbow animations.')
#       rainbow(strip)
#       rainbowCycle(strip)
#       theaterChaseRainbow(strip)
#   except KeyboardInterrupt:
#     if args.clear:
#       colorWipe(strip, Color(0,0,0), 10)


#    pass
