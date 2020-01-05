import sys
import logging
import paramiko
import argparse
from challenges import *

class Error(Exception):
    pass

class InvalidChallengeError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

#Function to check if a challenge is up using the solve function and redeploy if it is not
def check(challenge):
    logging.info("Checking challenge {}".format(challenge.__class__.__name__))
    if challenge.solve():
        logging.info("{} is up".format(challenge.__class__.__name__))
    else:
        logging.info("{} is down".format(challenge.__class__.__name__))
        logging.info("Redeploying {}".format(challenge.__class__.__name__))
        challenge.redeployment()
        logging.info("Redeployed {}".format(challenge.__class__.__name__))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically verify and redeploy implemented challenges")
    parser.add_argument("-l", "--list", action="store_true", help="List the challenges currently implemented")
    parser.add_argument("-t", "--target", nargs='+', help="Target challenges to test")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-f", "--file", help="Log file", default="./downDetector.log") 
    args = parser.parse_args()

    challengesList = []
    logfile = args.file
    logging.basicConfig(filename=logfile, filemode="w", level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    if args.verbose:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.getLogger("").addHandler(console)
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
                logging.info("No challenges")
                sys.exit()
            for i in challengesList:
                if i.__class__.__name__ == option:
                    check(i)
                else:
                    raise InvalidChallengeError("{} is not a valid challenge".format(option))
    else:
        if len(challengesList) == 0:
            logging.info("No challenges")
            sys.exit()
        for entry in challengesList:
            check(entry)

