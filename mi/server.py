# -*- coding: utf-8 -*-
"""
@author: Riccardo Omiccioli
"""

import socket as skt
import logging
import datetime
import ast

from ThreadedProgram import ThreadedProgram

def receive():
    # Create server TCP socket
    server_socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
    server_socket.bind(('localhost', 60001))
    # Queue up to 1 connect request
    server_socket.listen(1)
    # Setting timeout to make the socket semi-blocking
    server_socket.settimeout(1)
    while True:
        if tp.stop_threads:
            break
        if tp.threads_active:
            try:
                # Accept TCP connection and create connection socket
                connection_socket, client_address = server_socket.accept()
                try:
                    data = connection_socket.recv(16384)
                    data = data.decode("utf8")
                    # logging.debug("Received: {} bytes -> {}".format(len(data), data)) # Prints data received
                    if data:
                        # Converts data from string to dictionary
                        data = ast.literal_eval(data)
                        # For each key in dictrionary which is a device IP
                        for key in list(data.keys()):
                            # Converts from measurements string to list of measures
                            measures = ast.literal_eval(data[key])
                            for measure in measures:
                                # Splits the "epoch-temperature-humidity" string
                                measure_time, measure_temperature, measure_humidity = measure.split("-")
                                # Converting from epoch to (Y)ear (m)onth (d)ay (H)ours (M)inutes (S)econds 
                                measure_time = datetime.datetime.fromtimestamp(int(measure_time)).strftime('%Y-%m-%d %H:%M:%S')
                                # Prints data as requested
                                logging.debug("{}-{}-{}-{}".format(key, measure_time, measure_temperature, measure_humidity))
                    else:
                        break
                    logging.debug("Sending response")
                    connection_socket.send("OK".encode())
                finally:
                    connection_socket.close()
            # Continue execution if a socket timeout occours
            except skt.timeout:
                pass
        
tp = ThreadedProgram()
# Creating and starting server receive thread
tp.create_thread("TCP", receive)
# Starting terminal menu on main_thread
tp.start_UI()
