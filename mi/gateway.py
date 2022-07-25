# -*- coding: utf-8 -*-
"""
@author: Riccardo Omiccioli
"""

import socket as skt
import time
import re
import logging

from ThreadedProgram import ThreadedProgram

# Number of devices
device_number = 4

# Dictionary used to store all devices measures where IP addresses of the devices are the keys
devices_measures = {}

def receive():
    # Create UDP socket
    gateway_UDP_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
    gateway_UDP_socket.bind(("localhost", 50000))
    while True:
        if tp.stop_threads:
            break
        if tp.threads_active:
            # Wait for data on UDP socket
            data, address = gateway_UDP_socket.recvfrom(4096)
            data = data.decode("utf8")
            # Using regex to extract fake sender IP
            address = re.findall("^[\d.]*", data)[0]
            logging.debug("Received {} bytes from {}".format(len(data), address))
            # logging.debug("{}".format(data)) # Prints data received
            # Using regex to extract data (which is enclosed inside [])
            measures = re.findall("\[(.*?)\]", data)[0]
            with tp.lock:
                # With mutex add device measures from one device in the dictionary
                devices_measures[address] = measures

def send():
    while True:
        if tp.stop_threads:
            break
        if tp.threads_active:
            with tp.lock:
                # If measures from all device_number devices are received
                if len(devices_measures) == device_number:
                    # logging.debug("{}".format(devices_measures)) # Prints all measures
                    try:
                        # Create TCP socket
                        gateway_TCP_socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
                        gateway_TCP_socket.bind(("localhost", 60000))
                        gateway_TCP_socket.connect(("localhost", 60001))
                        # Getting time before sending then sending and then take time again
                        start_send = time.time()
                        gateway_TCP_socket.send(str(devices_measures).encode())                        
                        stop_send = time.time()
                        # Printing send time
                        logging.debug("Sent data in: {:.3f}µs".format((stop_send - start_send) * 1000000))
                        # Wait for server response
                        response = gateway_TCP_socket.recv(1024)
                        # Printing server response
                        logging.debug("Response from server: {}".format(response.decode("utf8")))
                    except Exception as e:
                        logging.debug("{}".format(e))   
                    finally:
                        gateway_TCP_socket.close()
                        # Clear measures dictionary to receive new measures
                        devices_measures.clear()
        
tp = ThreadedProgram()
# Creating and starting gateway receiver and sender threads
tp.create_thread("UDP-Receiver", receive)
tp.create_thread("TCP-Sender", send)
# Starting terminal menu on main_thread
tp.start_UI()
