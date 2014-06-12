import RPi.GPIO as GPIO
import time

Motor1A = 23
Motor1B = 24
Motor1E = 25

Motor2A = 11
Motor2B = 9
Motor2E = 10

class Motor(object):
  def __init__(self, a, b, e):
    # self.x = start
    self.a = a
    self.b = b
    self.e = e
    GPIO.setup(a, GPIO.OUT)
    GPIO.setup(b, GPIO.OUT)
    GPIO.setup(e, GPIO.OUT)

  def forward(self):
    GPIO.output(self.a, GPIO.HIGH)
    GPIO.output(self.b, GPIO.LOW)
    GPIO.output(self.e, GPIO.HIGH)

  def reverse(self):
    GPIO.output(self.a, GPIO.LOW)
    GPIO.output(self.b, GPIO.HIGH)
    GPIO.output(self.e, GPIO.HIGH)

  def stop(self):
    GPIO.output(self.a, GPIO.LOW)
    GPIO.output(self.b, GPIO.LOW)
    GPIO.output(self.e, GPIO.LOW)

  def __call__(self, channel):
    return 10;

class Robot(object):
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    self.left = Motor(Motor1A, Motor1B, Motor1E)
    self.right = Motor(Motor2A, Motor2B, Motor2E)

  def forward(self):
    self.left.forward()
    self.right.forward()

  def stop(self):
    self.left.stop()
    self.right.stop()

try:
  terrence = Robot()
  terrence.forward()
  time.sleep(2)
  terrence.stop()
  GPIO.cleanup()

except KeyboardInterrupt:
  GPIO.cleanup()
