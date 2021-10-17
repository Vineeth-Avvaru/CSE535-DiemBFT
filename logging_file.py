import logging

class LogStuff:
    def __init__(self):
        pass

    def log_to_file(s, nodeID):
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',filename='logFile.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
        logging.info("Node:" + str(nodeID) + " : " + s )
        pass
