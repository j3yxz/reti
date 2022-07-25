# -*- coding: utf-8 -*-
"""
@author: Riccardo Omiccioli
"""

import socket as skt
import random
import threading
import time
import logging
import re

from ThreadedProgram import ThreadedProgram

# Variable used to alterate parametes when testing the application
debug = True
# Sets day duration (in seconds) to 20 if debug mode is true or to the actual value of 86400 seconds per day
day_duration = 10 if debug else 86400

# Number of devices
device_number = 4
# Starting from average_temperature the program then randomly adds or subtracts a value with modulus delta_temperature to simulate measures
average_temperature = 17
delta_temperature = 5
# Starting from average_humidity the program then randomly adds or subtracts a value with modulus delta_humidity to simulate measures
average_humidity = 50
delta_humidity = 10

gateway_address = ('localhost', 50000)


def device():
    logging.debug("ThreadID_" + str(threading.get_ident()) + " Started")
    thread_name = threading.currentThread().getName()
    # Creating a fake IP address starting from 192.168.1.2
    ip_address = "192.168.1.{}".format(int(re.findall("[\d]*.$", thread_name)[0]) + 1)
    # List used to store device measures to be sent
    measures = []
    # Adding randomness to the start time of the devices so that they don't start at the same moment
    #time.sleep(random.randint(5, 10))
    # Getting the current time to send measures after day_duration from current time
    start_time = time.time()
    while True:
        if tp.stop_threads:
            break
        if tp.threads_active:
            # If debug mode is true wait a random time else wait for 30 minutes
            time.sleep(random.randint(1, 5) if debug else 1800)
            current_time = int(time.time())
            measure  = str(current_time) + "-"
            measure += str(average_temperature + random.randrange(-delta_temperature, delta_temperature)) + "-"
            measure += str(average_humidity + random.randrange(-delta_humidity, delta_humidity))
            # After creating measure string adds it to the list of measures to be sent
            measures.append(measure)
            logging.debug("Measure added: " + measure)
            # If the day_duration is elapsed send all measures
            if current_time - start_time >= day_duration:
                start_time = current_time
                # Prepare message with fake IP followed by all measures
                message = "{} {}".format(ip_address, measures)
                logging.debug("Sending measure")
                socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
                try:
                    # Getting time before sending then sending and then take time again
                    start_send = time.time()
                    socket.sendto(message.encode(), gateway_address)
                    stop_send = time.time()
                    logging.debug("Sent data in: {:.3f}µs".format((stop_send - start_send) * 1000000))
                except Exception as e:
                    logging.debug(str(e))
                finally:
                    socket.close()
                # Clear list of measures to be sent
                measures.clear()

tp = ThreadedProgram()
# Creating and starting devices threads
for i in range(device_number):
    tp.create_thread("Device-{}".format(i+1), device)
# Starting terminal menu on main_thread
tp.start_UI()
