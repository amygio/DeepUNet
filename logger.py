import time
import sys
import os
#import logging

#Class to create log files

class Logger(object):

    def __init__(self):
        #Check if the directory 'log' exists
        if not os.path.isdir("./log"):
            os.mkdir("./log")
        #Make the file named with the current time
        self.currentDate = time.strftime("%Y-%m-%d-%H-%M-%S")
        #Create the file
        open('./log/' + self.currentDate + ".log", "a").close()

        #copy all the output flow to the terminal
        self.terminal = sys.stdout
        #open the log file created before
        self.log = open('./log/' + self.currentDate + ".log", "a")

        #define the function to write on the log file
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

        #define the function to flush the flow, it is for python3
    def flush(self):
        pass
        
        """
        #set the log level and the message format
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        logger = logging.getLogger()

        #Set the format for the output messages
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

        #Intercept the standard output
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)

        #Indicate the file where to write the log messages
        file_handler = logging.FileHandler('./log/' + self.currentDate + ".log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        #Indicate where to write the log messages
        logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)
        """