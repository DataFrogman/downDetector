import sys
import logging
import paramiko
import argparse
import multiprocessing as mp
from challenges import *

class Error(Exception):
    pass

class InvalidChallengeError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

#Function to check if a challenge is up using the solve function and redeploy if it is not
def check(challenge):
    log.debug("Checking challenge {}".format(challenge.__class__.__name__))
    if challenge.solve():
        log.debug("{} is up".format(challenge.__class__.__name__))
    else:
        log.debug("{} is down".format(challenge.__class__.__name__))
        log.debug("Redeploying {}".format(challenge.__class__.__name__))
        challenge.redeployment()
        log.debug("Redeployed {}".format(challenge.__class__.__name__))
        log.debug("Verifying redeployment of {}".format(challenge.__class__.__name__))
        if challenge.solve():
            log.debug("{} sucessfully redeployed".format(challenge.__class__.__name__))
        else:
            log.debug("{} failed to redeploy".format(challenge.__class__.__name__))

if __name__ == "__main__":

    #Set up the parser
    parser = argparse.ArgumentParser(description="Automatically verify and redeploy implemented challenges")
    parser.add_argument("-l", "--list", action="store_true", help="List the challenges currently implemented")
    parser.add_argument("-t", "--target", nargs='+', help="Target challenges to test")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-f", "--file", help="Log file", default="./downDetector.log")
    parser.add_argument("-p", "--processes", help="Number of processes to use, default=5", default=5, type=int)
    args = parser.parse_args()
    
    # Example implementation of the 'sample' challenge
    #sample = sample('192.168.76.128', 'sample', 'test.pem')
    #challengesList = [sample]
    challengesList = []
    
    #Set up the logger
    logfile = args.file
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s", 
                              datefmt="%Y-%m-%d - %H:%M:%S")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    
    #Begin handling the args
    if args.verbose:
        log.addHandler(ch)
    if args.list:
        temp = "Challenges Implemented: "
        if len(challengesList) == 0:
            print("No challenges implemented")
        else:
            for entry in challengesList:
                temp = temp + entry.__class__.__name__ + ", "
            print(temp[0:-2])
    elif args.target is not None:
        for option in args.target:
            if len(challengesList) == 0:
                log.debug("No challenges")
                sys.exit()
            for i in challengesList:
                if i.__class__.__name__ == option:
                    check(i)
                else:
                    raise InvalidChallengeError("{} is not a valid challenge".format(option))
    else:
        if len(challengesList) == 0:
            log.debug("No challenges")
            sys.exit()
        pool = mp.Pool(processes=args.processes)
        results = [pool.apply(check, args=(x,)) for x in challengesList]

