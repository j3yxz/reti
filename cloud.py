# -*- coding: utf-8 -*-
"""
@author:Alexandru Bragari
"""

import socket
import ast
import logging
import sys
import logging_utility

device_measures = {}

# creo il socket per ricevere informazioni dal gateway
cloud_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cloud_socket.bind(('localhost', 61111))
cloud_socket.listen(1)
# per liberare il socket in caso di problemi
cloud_socket.settimeout(1)

while True:
    try:
        # accetta connessione tcp
        connection_socket, client_address = cloud_socket.accept()
        try:
            data = connection_socket.recv(32768)
            data = data.decode("utf8")
            if data:
                # converto i dati ricevuti in dizionario
                decoded_data = ast.literal_eval(data)

                for key in list(decoded_data.keys()):
                    # ora che ho la lista posso riorganizzarla per stampare output richiesto dalle specifiche
                    data_values = decoded_data[key]
                    ip, temp, humidity, times = data_values.split('#')
                    temp_all = temp.split(',')
                    humidity_all = humidity.split(',')
                    times_all = times.split(',')
                    for i in range(len(temp_all)):
                        logging.debug("{}-{}-{}-{}".format(str(ip), str(times_all[i]), str(temp_all[i]), str(humidity_all[i])))
            else:
                break
            logging.debug("ok response")
            connection_socket.send("200".encode())
        finally:
            connection_socket.close()
    # se succede un errore del timeout ricomincia il ciclo e riprova
    except socket.timeout:
        pass