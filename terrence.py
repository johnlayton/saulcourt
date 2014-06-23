import RPi.GPIO as GPIO
import threading
import Queue
import time
import sys
import os
import termios
import tty

Motor1A = 17#23
Motor1B = 27#24
Motor1E = 22#25

Odometer1 = 14

Motor2A = 11
Motor2B = 9
Motor2E = 10

Odometer2 = 15

class Buffer:
  def __init__(self, size):
    self.size = size
    self.data = [None for i in xrange(size)]

  def append(self, x):
    self.data.pop(0)
    self.data.append(x)

  def get(self):
    return self.data

  def reset(self):
    self.data = [None for i in xrange(self.size)]

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

    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=self, bouncetime=10)

    # GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.add_event_detect(pin, GPIO.FALLING, callback=self, bouncetime=10)

  def __call__(self, channel):
    self.counter.increment()
    self.buffer.append(time.time())

  def reset(self):
    self.buffer.reset();

  def speed(self):
    # print self.counter.get()
    # print self.buffer.get()
    if ( None in self.buffer.get() or ( ( time.time() - self.buffer.get()[4]  ) > 2 ) ):
      return 0.0
    else:
      return ( 5.0 * ( 6.0 / 1000.0 ) ) / ( self.buffer.get()[4] - self.buffer.get()[0] )

class Motor(object):
  def __init__(self, a, b, e, o):
    self.a = a
    self.b = b
    self.e = e
    self.o = o
    GPIO.setup(a, GPIO.OUT)
    GPIO.setup(b, GPIO.OUT)
    GPIO.setup(e, GPIO.OUT)
    self.p = GPIO.PWM(e, 10000)
    self.p.start(0)

  def reverse(self, speed=100):
    GPIO.output(self.a, GPIO.LOW)
    GPIO.output(self.b, GPIO.HIGH)
    self.p.ChangeDutyCycle(speed)

  def forward(self, speed=100):
    GPIO.output(self.a, GPIO.HIGH)
    GPIO.output(self.b, GPIO.LOW)
    self.p.ChangeDutyCycle(speed)

  def stop(self):
    GPIO.output(self.a, GPIO.LOW)
    GPIO.output(self.b, GPIO.LOW)
    self.p.ChangeDutyCycle(0)
    # self.p.stop()
    # GPIO.output(self.e, GPIO.LOW)

  def reset(self):
    self.o.reset()

  def speed(self):
    return self.o.speed()

class Logging(threading.Thread):
  def __init__(self, robot):
    threading.Thread.__init__(self)
    self.robot = robot
    self.file = open("./logging.csv", "a")

  def run(self):
    while True:
      # print "%s" % ( self.robot.speed() )
      self.file.write( "%s" % ( self.robot.speed() ) )
      self.file.write( "\n" )
      self.file.flush()
      time.sleep(.25)

  def title(self, text):
    self.file.write(text)
    self.file.write( "\n" )
    self.file.flush()

class Robot(object):
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    self.lft = Motor(Motor1A, Motor1B, Motor1E, Odometer( Odometer1, "left" ) )
    self.rgt = Motor(Motor2A, Motor2B, Motor2E, Odometer( Odometer2, "right" ) )
    self.log = Logging(self)
    self.log.setDaemon(True)
    self.log.start()

  def forward(self, speed=100):
    self.log.title("Forward")
    self.rgt.forward(speed)
    self.lft.forward(speed)

  def reverse(self, speed=100):
    self.log.title("Reverse")
    self.rgt.reverse(speed)
    self.lft.reverse(speed)

  def forward_right(self):
    self.log.title("Forward Right")
    self.lft.forward(100)
    self.rgt.forward(0)

  def forward_left(self):
    self.log.title("Forward Left")
    self.lft.forward(0)
    self.rgt.forward(100)

  def reverse_right(self):
    self.log.title("Reverse Right")
    self.lft.reverse(100)
    self.rgt.reverse(0)

  def reverse_left(self):
    self.log.title("Reverse Left")
    self.lft.reverse(00)
    self.rgt.reverse(100)

  def right(self):
    self.log.title("Right")
    self.lft.forward(100)
    self.rgt.reverse(100)

  def left(self):
    self.log.title("Left")
    self.lft.reverse(100)
    self.rgt.forward(100)

  def stop(self):
    self.log.title("Stop")
    self.rgt.stop()
    self.lft.stop()

  def reset(self):
    self.log.title("Reset")
    self.rgt.reset()
    self.lft.reset()

  def speed(self):
    return "%2.8f,%2.8f" % ( self.lft.speed(), self.rgt.speed() )


class Demo(object):
  # def __init__(self):

  def run_func(self, title, r, func, after, delay):
    print title
    r.reset()
    time.sleep(2)
    func()
    time.sleep(delay)
    after()
    r.reset()

  def run(self):
    try:
      r = Robot()

      self.run_func("reverse right", r, r.rgt.reverse, r.rgt.stop, 20);
      self.run_func("forward right", r, r.rgt.forward, r.rgt.stop, 20);

      self.run_func("reverse left", r, r.lft.reverse, r.lft.stop, 20);
      self.run_func("forward left", r, r.lft.forward, r.lft.stop, 20);

      self.run_func("reverse both", r, r.reverse, r.stop, 20);
      self.run_func("forward both", r, r.forward, r.stop, 20);

      GPIO.cleanup()

    except KeyboardInterrupt:
      GPIO.cleanup()


class Console(object):

  def __init__(self):
    self.rr = Robot()

  def key(self):
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
    new[6][termios.VMIN] = 1
    new[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, new)
    key = None
    try:
      key = os.read(fd, 3)
    finally:
      termios.tcsetattr(fd, termios.TCSAFLUSH, old)
    return key

  def run(self):
    try:
      while True:
        key = str(self.key() )
        if key == "y":
          self.rr.forward(10)
        elif key == "b":
          self.rr.reverse(10)

        elif key == "h":
          self.rr.right()
        elif key == "g":
          self.rr.left()

        elif key == "u":
          self.rr.forward_right()
        elif key == "t":
          self.rr.forward_left()
        elif key == "n":
          self.rr.reverse_right()
        elif key == "v":
          self.rr.reverse_left()

        elif key == " ":
          self.rr.stop()

    except KeyboardInterrupt:
      GPIO.cleanup()

# Demo().run()
Console().run()
