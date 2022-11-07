#!/usr/bin/python
#
# Python Module to externalise all Initio/RoboHAT specific hardware
#
# Created by Gareth Davies, Feb 2016
# Copyright 4tronix
#
# This code is in the public domain and may be freely copied and used
# No warranty is provided or implied
#
# ======================================================================


# ======================================================================
# General Functions
#
# init(). Initialises GPIO pins, switches motors off, etc
# cleanup(). Sets all motors off and sets GPIO to standard values
# version(). Returns 2. Invalid until after init() has been called
# ======================================================================


# ======================================================================
# Motor Functions
#
# stop(): Stops both motors
# forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
# reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
# spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
# spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
# turnForward(leftSpeed, rightSpeed): Moves forwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
# turnreverse(leftSpeed, rightSpeed): Moves backwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
# ======================================================================


# ======================================================================
# UltraSonic Functions
#
# getDistance(). Returns the distance in cm to the nearest reflecting object. 0 == no object
# ======================================================================

# ======================================================================
# Servo Functions
# 
# startServos(). Initialises the servo background process
# stop Servos(). terminates the servo background process
# setServo(Servo, Degrees). Sets the servo to position in degrees -90 to +90
# ======================================================================


# Import all necessary libraries
import RPi.GPIO as GPIO, sys, threading, time, os, subprocess

# Pins 35, 36 Left Motor
# Pins 32, 33 Right Motor
LS = 7
LD = 11
RS = 13
RD = 15

# Define Sonar Pin (Uses same pin for both Ping and Echo)
#sonar = 38

ServosActive = False


# ======================================================================
# General Functions
#
# init(). Initialises GPIO pins, switches motors and LEDs Off, etc
def init():
    global p, q, a, b

    GPIO.setwarnings(False)

    # use physical pin numbering
    GPIO.setmode(GPIO.BOARD)

    #p LS
    q = LD
    #a RS
    b =RD

    # use pwm on inputs so motors don't go too fast
    GPIO.setup(LS, GPIO.OUT)
    p = GPIO.PWM(LS, 20)
    p.start(0)

    GPIO.setup(LD, GPIO.OUT)

    GPIO.setup(RS, GPIO.OUT)
    a = GPIO.PWM(RS, 20)
    a.start(0)

    GPIO.setup(RD, GPIO.OUT)

    startServos()


# cleanup(). Sets all motors off and sets GPIO to standard values
def cleanup():
    stop()
    stopServos()
    GPIO.cleanup()


# version(). Returns 2. Invalid until after init() has been called
def version():
    return 2  # (version 1 is Pirocon, version 2 is RoboHAT)


# End of General Functions
# ======================================================================


# ======================================================================
# Motor Functions
#
# stop(): Stops both motors
def stop():
    p.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)



# forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
def forward(speed):
    p.ChangeDutyCycle(speed)
    a.ChangeDutyCycle(speed)
    p.ChangeFrequency(speed + 5)
    a.ChangeFrequency(speed + 5)


# reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
def reverse(speed):
    GPIO.output(q, 1)
    GPIO.output(b, 1)
    p.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    p.ChangeFrequency(speed + 5)
    a.ChangeFrequency(speed + 5)


# spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def spinLeft(speed):
    GPIO.output(q, 0)
    GPIO.output(b, 1)
    p.ChangeDutyCycle(speed)
    a.ChangeDutyCycle(speed)
    p.ChangeFrequency(speed + 5)
    a.ChangeFrequency(speed + 5)


# spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def spinRight(speed):
    GPIO.output(q, 1)
    GPIO.output(b, 0)
    p.ChangeDutyCycle(speed)
    a.ChangeDutyCycle(speed)
    p.ChangeFrequency(speed + 5)
    a.ChangeFrequency(speed + 5)


# turnForward(leftSpeed, rightSpeed): Moves forwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnForward(leftSpeed, rightSpeed):
    GPIO.output(q, 1)
    GPIO.output(b, 1)
    p.ChangeDutyCycle(leftSpeed)
    a.ChangeDutyCycle(rightSpeed)
    p.ChangeFrequency(leftSpeed + 5)
    a.ChangeFrequency(rightSpeed + 5)


# turnReverse(leftSpeed, rightSpeed): Moves backwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnReverse(leftSpeed, rightSpeed):
    GPIO.output(q, 0)
    GPIO.output(b, 0)
    p.ChangeDutyCycle(leftSpeed)
    a.ChangeDutyCycle(rightSpeed)
    p.ChangeFrequency(leftSpeed + 5)
    a.ChangeFrequency(rightSpeed + 5)


# End of Motor Functions
# ======================================================================

# ======================================================================
# UltraSonic Functions

# getDistance(). Returns the distance in cm to the nearest reflecting object. 0 == no object
def getDistance():
    GPIO.setup(sonar, GPIO.OUT)
    # Send 10us pulse to trigger
    GPIO.output(sonar, True)
    time.sleep(0.00001)
    GPIO.output(sonar, False)

    start = time.time()
    count = time.time()
    GPIO.setup(sonar, GPIO.IN)
    while GPIO.input(sonar) == 0 and time.time() - count < 0.1:
        start = time.time()

    count = time.time()
    stop = count
    while GPIO.input(sonar) == 1 and time.time() - count < 0.1:
        stop = time.time()

    # Calculate pulse length
    elapsed = stop - start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000
    # That was the distance there and back so halve the value
    distance = distance / 2
    return distance


# End of UltraSonic Functions
# ======================================================================

# ======================================================================
# Servo Functions
# Pirocon/Microcon/RoboHAT use ServoD to control servos


def setServo(Servo, Degrees):
    global ServosActive
    # print "ServosActive:", ServosActive
    # print "Setting servo"
    if ServosActive == False:
        startServos()
    pinServod(Servo, Degrees)  # for now, simply pass on the input values


def stopServos():
    stopServod()


def startServos():
    # print "Starting servod as CPU =", CPU
    startServod()


def startServod():
    global ServosActive
    # print "Starting servod. ServosActive:", ServosActive
    SCRIPTPATH = os.path.split(os.path.realpath(__file__))[0]
    os.system("sudo pkill -f servod")
    initString = "sudo " + SCRIPTPATH + '/servod --pcm --idle-timeout=20000 --p1pins="18,22" > /dev/null'

    os.system(initString)
    ServosActive = True


def pinServod(pin, degrees):
    # print pin, degrees
    pinString = "echo " + str(pin) + "=" + str(50 + ((90 - degrees) * 200 / 180)) + " > /dev/servoblaster"
    os.system(pinString)


def stopServod():
    global ServosActive
    os.system("sudo pkill -f servod")
    ServosActive = False
