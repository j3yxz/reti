# -*- coding: utf-8 -*-
"""
@author:Alexandru Bragari
"""

import socket
import random
import threading
import time
import datetime
import logging
import logging_utility

gt_adr = ("127.0.0.1", 56789)

# per testarlo ho messo 20 secondi anziché 24 ore
day_duration = 20

n_device = 4

min_temp = -50
min_humidity = 0

max_temp = 40
max_humidity = 100


def device_thread():
    th_time = time.time()
    temp = []
    humidity = []
    time_list = []
    while(True):
        temp.append(random.randint(min_temp, max_temp))
        humidity.append(random.randint(min_humidity, max_humidity))
        time_list.append(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
        if time.time() - th_time >= day_duration:
            # qua vengono mandate le misure con una send
            device_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # prendo il tempo di inizio fine e mando il messaggio opportunamente codificato in stringa
                #datetime.datetime.fromtimestamp(int(measure_time)).strftime('%Y-%m-%d %H:%M:%S')
                message = str(threading.currentThread().getName()) + "#" + ','.join(map(str, temp)) + "#" + ','.join(map(str, humidity)) + "#" + ','.join(map(str, time_list))
                logging.debug("messaggio: " + message)
                start = time.time()
                device_socket.sendto(message.encode(), gt_adr)
                stop = time.time()
                logging.debug("Tempo invio dati {:.6f}µs".format((stop - start) * 1000000))
            except Exception as error:
                logging.debug("Exception: " + str(error))
            finally:
                device_socket.close()
            th_time = time.time()
            temp.clear()
            humidity.clear()
            time_list.clear()
        time.sleep(random.randint(0, 5))

for i in range(n_device):
    thread = threading.Thread(name=(f"192.168.1.%i" % (i+10)), target=device_thread)
    thread.start()
