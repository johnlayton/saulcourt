import RPi.GPIO as GPIO
from time import sleep



GPIO.setmode(GPIO.BCM)

Motor1A = 23
Motor1B = 24
Motor1E = 25

Motor2A = 11
Motor2B = 9
Motor2E = 10

try:
  GPIO.setup(Motor1A,GPIO.OUT)
  GPIO.setup(Motor1B,GPIO.OUT)
  GPIO.setup(Motor1E,GPIO.OUT)

  GPIO.setup(Motor2A,GPIO.OUT)
  GPIO.setup(Motor2B,GPIO.OUT)
  GPIO.setup(Motor2E,GPIO.OUT)

  # GPIO.output(Motor1A,GPIO.LOW)
  # GPIO.output(Motor1B,GPIO.LOW)
  # GPIO.output(Motor1E,GPIO.HIGH)

  # sleep(10)

  '''
  GPIO.output(Motor1B,GPIO.LOW)
  GPIO.output(Motor2B,GPIO.LOW)
  GPIO.output(Motor1A,GPIO.LOW)
  GPIO.output(Motor2A,GPIO.LOW)
  GPIO.output(Motor1E,GPIO.HIGH)
  GPIO.output(Motor2E,GPIO.HIGH)

  A1 = GPIO.PWM(Motor1A, 100)
  A2 = GPIO.PWM(Motor2A, 100)
  B1 = GPIO.PWM(Motor1B, 100)
  B2 = GPIO.PWM(Motor2B, 100)

  # forward
  A1.start(60)
  A2.start(73)

  sleep(1)

  A1.stop()
  A2.stop()

  GPIO.output(Motor1B,GPIO.LOW)
  GPIO.output(Motor2B,GPIO.LOW)
  GPIO.output(Motor1A,GPIO.LOW)
  GPIO.output(Motor2A,GPIO.LOW)

  # forward
  B1.start(70)
  B2.start(90)

  B1.stop()
  B2.stop()

  GPIO.output(Motor1B,GPIO.LOW)
  GPIO.output(Motor2B,GPIO.LOW)
  GPIO.output(Motor1A,GPIO.LOW)
  GPIO.output(Motor2A,GPIO.LOW)

  #A1.start(70)
  # A2.start(70)

  # for i in range(0, 100, 10):
  #   print i
  #   A.ChangeDutyCycle(i)
  #   B.ChangeDutyCycle(i)
  sleep(1)
  '''
  # E1 = GPIO.PWM(Motor1E, 100)
  # E2 = GPIO.PWM(Motor2E, 100)
  #
  # E1.start(40)
  # E2.start(53)

  print "Going forwards"
  GPIO.output(Motor1A,GPIO.HIGH)
  GPIO.output(Motor1B,GPIO.LOW)
  GPIO.output(Motor1E,GPIO.HIGH)

  GPIO.output(Motor2A,GPIO.HIGH)
  GPIO.output(Motor2B,GPIO.LOW)
  GPIO.output(Motor2E,GPIO.HIGH)

  # for i in range(0, 40, 5):
  #   print i
  #   E1.ChangeDutyCycle(i)
  #   E2.ChangeDutyCycle(i + 13)
  #   sleep(0.05)
  #
  # sleep(2)
  #
  # print "Turn left"
  # E1.ChangeDutyCycle(30)
  # E2.ChangeDutyCycle(45)
  # GPIO.output(Motor1A,GPIO.LOW)
  # GPIO.output(Motor1B,GPIO.HIGH)
  # GPIO.output(Motor2A,GPIO.HIGH)
  # GPIO.output(Motor2B,GPIO.LOW)

  sleep(2)

  print "Going backwards"
  GPIO.output(Motor1A,GPIO.LOW)
  GPIO.output(Motor1B,GPIO.HIGH)
  GPIO.output(Motor1E,GPIO.HIGH)

  GPIO.output(Motor2A,GPIO.LOW)
  GPIO.output(Motor2B,GPIO.HIGH)
  GPIO.output(Motor2E,GPIO.HIGH)

  sleep(1)

  print "Now stop"
  E1.stop()
  E2.stop()
  GPIO.output(Motor1E,GPIO.LOW)
  GPIO.output(Motor2E,GPIO.LOW)

  GPIO.cleanup()

except KeyboardInterrupt:
  GPIO.cleanup()
