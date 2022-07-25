# -*- coding: utf-8 -*-
"""
@author: Riccardo Omiccioli
"""

import threading
import time
import logging
import sys
import os

class ThreadedProgram():

    def __init__(self):
        # List of threads managed by this class
        self.threads = []
        # Lock variable used for threads mutual exlusion (mutex)
        self.lock = threading.Lock()  
        # Variable used to exit the infinite while loop inside threads
        self.stop_threads = False
        # Variable used to pause threads execution
        self.threads_active = True
        # Menu string used in terminal UI
        self.menu_string  = "################################################################################\n"
        self.menu_string += "# 1) Close program                                                             #\n"
        self.menu_string += "# 2) Activate/Deactivate threads                                               #\n"
        self.menu_string += "################################################################################\n"
        # Logging setup
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("(%(threadName)-5s) %(message)s")
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

    def join_all(self):
        # Stopping threads infinite while loop
        self.stop_threads = True
        # Joining all threads in threads list
        for t in self.threads:
            logging.debug("Joining %s", t.getName())
            t.join()
            logging.debug("Join complete  %s", t.getName())
    
    # Simple thread target method as an example
    def thread(self):
        logging.debug("ThreadID_{} Started".format(threading.get_ident()))
        while True:
            # If all threads are stopped exit from infinite while loop
            if self.stop_threads:
                break
            # If the threads are running (if they are not active do nothing)
            if self.threads_active:
                # Code that the thread executes
                logging.debug("active")
                time.sleep(1)
                
    def create_thread(self, name, function):
        # Create thread
        thread = threading.Thread(name="Thread-{}".format(name), target=function)
        # Add thread to treads list
        self.threads.append(thread)
        # Starts the thread
        thread.start()
        
    def start_UI(self):
        # Main thread
        main_thread = threading.main_thread()
        for thread in threading.enumerate():
            # If the main_thread is found continue execution of code below
            if thread is main_thread:
                continue
            while True:
                # Print menu string and wait for user input (main_thread is blocked but other threads execution continues)
                user_input = int(input(self.menu_string + '> '))
                if user_input == 1:
                    self.join_all()
                    time.sleep(1)
                    # Sigkill to restart python kernell and reset cache
                    os.kill(os.getpid(), 9)
                elif user_input == 2:
                    self.threads_active = not self.threads_active
                    logging.debug("Threads active: {}".format(self.threads_active))
                else:
                    logging.debug("Incorrect command, try again")   
            