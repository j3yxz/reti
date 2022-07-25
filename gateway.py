# -*- coding: utf-8 -*-
"""
@author:Alexandru Bragari
"""

import socket
import time
import logging
import logging_utility

n_device = 4

device_measures = {}

gateway_UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
gateway_UDP_socket.bind(("localhost", 56789))
while True:
    # aspetta i dati sul socket udp
    data, address = gateway_UDP_socket.recvfrom(4096)
    data = data.decode("utf8")
    # data = 192.168.1.1#10,20,30#40,50,60#10000,100001
    data_split = data.split('#')

    address = data_split[0]
    logging.debug("Ricevuto dati da {}".format(address))
    # logging.debug("Data[1] {} Data[2] {} Data[3] {}".format(data[1] , data[2], data[3]))

    device_measures[address] = data
    if len(device_measures) == n_device:
        # bisogna mandare i dati al server e pulire il vettore device_measures

        try:
            # creo socket tcp
            gateway_TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # il bind non è necessario
            gateway_TCP_socket.bind(("localhost", 61110))
            gateway_TCP_socket.connect(("localhost", 61111))

            start = time.time()
            gateway_TCP_socket.send(str(device_measures).encode())
            stop = time.time()

            logging.debug("time to send: {:.6f} µs".format((stop - start) * 1000000))
            # aspetto la risposta del cloud
            response = gateway_TCP_socket.recv(1024)

            logging.debug("Cloud response: {}".format(response.decode("utf8")))
        except Exception as Error:
            logging.debug("{}".format(Error))
        finally:
            gateway_TCP_socket.close()
        device_measures.clear()