import logging

class LogStuff:
    def __init__(self):
        pass

    def log_to_file_node(s, nodeID):
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',filename='../logs/logFile.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
        logging.info("Node:" + str(nodeID) + " : " + s )
        pass
    
    def log_to_file(s, level="INFO"):
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',filename='../logs/logFile.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
        if level == "ERROR":
            logging.error(s)
        else:
            logging.info(s)
        pass

    def log_to_file_param(s, p):
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',filename='../logs/logFile.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
        logging.info(s + " : " + str(p))
