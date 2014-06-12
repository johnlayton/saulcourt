import RPi.GPIO as GPIO
import threading
import Queue
import time

Motor1A = 23
Motor1B = 24
Motor1E = 25

Odometer1 = 14

Motor2A = 11
Motor2B = 9
Motor2E = 10

Odometer2 = 15

Epoch =  time.mktime( time.gmtime(0) )

class Buffer:
  def __init__(self, size):
    self.data = [Epoch for i in xrange(size)]
    # self.data = [None for i in xrange(size)]

  def append(self, x):
    self.data.pop(0)
    self.data.append(x)

  def get(self):
    return self.data

class Counter(object):
  def __init__(self):
    self.x = 0

  def increment(self):
    self.x += 1

  def get(self):
    return self.x

class Odometer(object):
  def __init__(self, pin, name = "unknown"):
    self.name = name
    self.counter = Counter()
    self.buffer = Buffer(5)
    # GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.add_event_detect(pin, GPIO.RISING, callback=self, bouncetime=10)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=self, bouncetime=10)

  def __call__(self, channel):
    self.counter.increment()
    self.buffer.append(time.time())

  def speed(self):
    # print self.counter.get()
    # print self.buffer.get()
    if ( self.buffer.get()[0] == Epoch ):
      return 0.0
    else:
      return ( 5.0 * ( 6.0 / 1000.0 ) ) / ( self.buffer.get()[4] - self.buffer.get()[0] )

class Motor(object):
  def __init__(self, a, b, e, o):
    # self.x = start
    self.a = a
    self.b = b
    self.e = e
    self.o = o
    GPIO.setup(a, GPIO.OUT)
    GPIO.setup(b, GPIO.OUT)
    GPIO.setup(e, GPIO.OUT)
    self.p = GPIO.PWM(e, 100)
    self.p.start(0)

  def forward(self, speed=100):
    GPIO.output(self.a, GPIO.LOW)
    GPIO.output(self.b, GPIO.HIGH)
    self.p.ChangeDutyCycle(speed)
    # GPIO.output(self.e, GPIO.HIGH)

  def reverse(self, speed=100):
    GPIO.output(self.a, GPIO.HIGH)
    GPIO.output(self.b, GPIO.LOW)
    self.p.ChangeDutyCycle(speed)
    # GPIO.output(self.e, GPIO.HIGH)

  def stop(self):
    self.p.stop()
    GPIO.output(self.a, GPIO.LOW)
    GPIO.output(self.b, GPIO.LOW)
    GPIO.output(self.e, GPIO.LOW)

  def speed(self):
    return self.o.speed()

class Logging(threading.Thread):
  def __init__(self, robot):
    threading.Thread.__init__(self)
    self.robot = robot

  def run(self):
    while True:
      print "Speed is: %s" % ( self.robot.speed() )
      time.sleep(1.0)

class Robot(object):
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    self.a = Motor(Motor1A, Motor1B, Motor1E, Odometer( Odometer1, "1" ) )
    self.b = Motor(Motor2A, Motor2B, Motor2E, Odometer( Odometer2, "2" ) )
    self.t = Logging(self)
    self.t.setDaemon(True)
    self.t.start()

  def forward(self, speed=100):
    self.a.forward(speed)
    self.b.forward(speed)

  def reverse(self, speed=100):
    self.a.reverse(speed)
    self.b.reverse(speed)

  def forward_right(self):
    self.b.forward(100)
    self.a.forward(50)

  def forward_left(self):
    self.b.forward(50)
    self.a.forward(100)

  def reverse_right(self):
    self.b.reverse(100)
    self.a.reverse(50)

  def reverse_left(self):
    self.b.reverse(50)
    self.a.reverse(100)

  def right(self):
    self.b.forward(100)
    self.a.reverse(50)

  def left(self):
    self.b.reverse(50)
    self.a.forward(100)

  def stop(self):
    self.a.stop()
    self.b.stop()

  def speed(self):
    return "A = %2.8f, B = %2.8f" % ( self.a.speed(), self.b.speed() )

# try:
#   r = Robot()
#
#   t = Logging(r)
#   t.setDaemon(True)
#   t.start()
#
#   r.reverse()
#   time.sleep(5)
#
#   r.forward( 100 )
#   time.sleep(2)
#
#   r.left()
#   time.sleep(2)
#
#   r.right()
#   time.sleep(2)
#   r.forward( 50 )
#
#   time.sleep(2)
#   r.reverse()
#
#   time.sleep(2)
#   r.stop()
#
#   GPIO.cleanup()
#
# except KeyboardInterrupt:
#   GPIO.cleanup()
