import time
import RPi.GPIO as GPIO

DEBUG = True

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 8
GPIO_ECHO    = 7

Motor1A = 23
Motor1B = 24
Motor1E = 25

Motor2A = 11
Motor2B = 9
Motor2E = 10

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)      # Echo

GPIO.output(GPIO_TRIGGER,GPIO.LOW)

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

GPIO.output(Motor1A,GPIO.LOW)
GPIO.output(Motor1B,GPIO.LOW)
GPIO.output(Motor1E,GPIO.LOW)

GPIO.output(Motor2A,GPIO.LOW)
GPIO.output(Motor2B,GPIO.LOW)
GPIO.output(Motor2E,GPIO.LOW)

E1 = GPIO.PWM(Motor1E, 100)
E2 = GPIO.PWM(Motor2E, 100)

E1.start(40)
E2.start(55)

def speed(value):
  E1.ChangeDutyCycle(value)
  E2.ChangeDutyCycle(value + 15)

def ping():
  # Trigger high for 0.0001s then low
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.0001)
  GPIO.output(GPIO_TRIGGER, False)

  # Wait for echo to go high (or timeout)
  intcountdown = 2100

  while (GPIO.input(GPIO_ECHO) == 0 and intcountdown > 0):
    intcountdown = intcountdown - 1

  # If echo is high
  if intcountdown > 0:

    # Start timer and init timeout countdown
    echostart = time.time()
    intcountdown = 2100

    # Wait for echo to go low (or timeout)
    while (GPIO.input(GPIO_ECHO) == 1 and intcountdown > 0):
      intcountdown = intcountdown - 1

    # Stop timer
    echoend = time.time()

    # Echo duration
    echoduration = echoend - echostart

  # Display distance
  if intcountdown > 0:
    intdistance = (echoduration*1000000)/58
    # print "Distance = " + str(int(intdistance)) + "cm [" + str( echoduration *1000000 ) + "s]"
    return intdistance
  else:
    return 0

def measure_average():
  if DEBUG:
    print "Measure average"
  distance = ping() + ping() + ping()
  distance = distance / 3
  return distance

def forward():
  if DEBUG:
    print "Going forwards"
  GPIO.output(Motor1A,GPIO.HIGH)
  GPIO.output(Motor1B,GPIO.LOW)
  # GPIO.output(Motor1E,GPIO.HIGH)

  GPIO.output(Motor2A,GPIO.HIGH)
  GPIO.output(Motor2B,GPIO.LOW)
  # GPIO.output(Motor2E,GPIO.HIGH)

def backward():
  if DEBUG:
    print "Going backwards"
  GPIO.output(Motor1A,GPIO.LOW)
  GPIO.output(Motor1B,GPIO.HIGH)
  # GPIO.output(Motor1E,GPIO.HIGH)

  GPIO.output(Motor2A,GPIO.LOW)
  GPIO.output(Motor2B,GPIO.HIGH)
  # GPIO.output(Motor2E,GPIO.HIGH)

def left():
  if DEBUG:
    print "Turn left"
  GPIO.output(Motor1A,GPIO.HIGH)
  GPIO.output(Motor1B,GPIO.LOW)
  # GPIO.output(Motor1E,GPIO.HIGH)

  GPIO.output(Motor2A,GPIO.LOW)
  GPIO.output(Motor2B,GPIO.HIGH)
  # GPIO.output(Motor2E,GPIO.HIGH)

def right():
  if DEBUG:
    print "Turn right"
  GPIO.output(Motor1A,GPIO.LOW)
  GPIO.output(Motor1B,GPIO.HIGH)
  # GPIO.output(Motor1E,GPIO.HIGH)

  GPIO.output(Motor2A,GPIO.HIGH)
  GPIO.output(Motor2B,GPIO.LOW)
  # GPIO.output(Motor2E,GPIO.HIGH)

def stop():
  if DEBUG:
    print "Now stop"
  E1.stop()
  E2.stop()

  GPIO.output(Motor1A,GPIO.LOW)
  GPIO.output(Motor1B,GPIO.LOW)
  GPIO.output(Motor1E,GPIO.LOW)

  GPIO.output(Motor2A,GPIO.LOW)
  GPIO.output(Motor2B,GPIO.LOW)
  GPIO.output(Motor2E,GPIO.LOW)

def exit():
  if DEBUG:
    print "Now exit"
  GPIO.cleanup()

time.sleep(2)

speed(40)

try:
  while True:
    distance = measure_average()
    print "Distance : %.1f" % distance
    if distance < 10:
      left()
    elif distance > 10 and distance < 50:
      speed(40)
      left()
    elif distance > 50 and distance < 100:
      speed(40)
      forward()
    elif distance > 100:
      speed(40)
      forward()
    else:
      forward()
    time.sleep(0.1)

except KeyboardInterrupt:
  GPIO.cleanup()
