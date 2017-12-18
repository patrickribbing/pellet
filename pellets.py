#!/usr/bin/python3
# Read distance from a HC-SR04 distance sensor
# Write to file
# Use a LED to indicate a low distance, otherwise OK

import RPi.GPIO as GPIO
import time
import datetime

# GPIO pin for trigger
TRIG_PIN = 4
# GPIO pin for echo
ECHO_PIN = 17
# GPIO pin for LED
LED_PIN = 18
# file to write to
SINGLE_DISTANCE_FILE = "/var/www/html/distance.data"
# warning distance (mm)
WARNING_DISTANCE = 250
# Add this value (mm) to distance
DISTANCE_OFFSET = 70
# size of cabin (mm)
CABIN_SIZE = 870

distance_stack = list()

def init_system():
    #print ("Initialize system...")
    GPIO.setmode(GPIO.BCM)
    # setup pins
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.setup(LED_PIN, GPIO.OUT)
    # turn on LED
    GPIO.output(LED_PIN, GPIO.HIGH)
    # setup sensor
    GPIO.output(TRIG_PIN, False)
    time.sleep(2)
    # turn off LED
    GPIO.output(LED_PIN, GPIO.LOW)

# get distance in mm
def read_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    read_distance = pulse_duration * 171500
    read_distance += DISTANCE_OFFSET
    read_distance = int(round(read_distance))
    return read_distance

# flash LED if low level
def led_handler(distance):
    if distance < WARNING_DISTANCE:
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)

# write value to file
def write_to_file(distance):
    text_file = open(SINGLE_DISTANCE_FILE, "w")
    text_file.write(str(distance))
    text_file.close()
    return;

# calculate a floating average of distance,
# use current and four old values
def floating_avg_distance(distance):
    distance_stack.append(distance)
    if len(distance_stack) > 5:
        distance_stack.pop(0)

    sum = 0
    for item in distance_stack:
        sum += item

    avg = sum / len(distance_stack)
    return int(round(avg))

init_system()

last_distance = -1

while True:
    try:
        time.sleep(10)
        distance = read_distance()
        orig_value = distance
        # check measured distance
        if distance - DISTANCE_OFFSET < 40:
            continue
        if last_distance != -1:
            diff = abs(last_distance - distance) / last_distance
            if diff > 0.1:
                # Too much difference between this and last measurement
                if last_distance > distance:
                    distance = last_distance * 0.9
                else:
                    distance = last_distance * 1.1
        last_distance = distance

        left_in_cabin = CABIN_SIZE - distance
        if left_in_cabin > 0:
            avg = floating_avg_distance(left_in_cabin)
            write_to_file(avg)
            led_handler(avg)
    except Exception:
        pass

# will never come to this point...
GPIO.cleanup()
