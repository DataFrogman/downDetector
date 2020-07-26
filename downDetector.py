import sys
import logging
import paramiko
import argparse
import multiprocessing as mp
from challenges import *
from cmd import Cmd

challengesList = []
timer = 300
threads = 5

class Error(Exception):
    pass

class InvalidChallengeError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class IllegalInputError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

#Function builder for interactive shell
class myPrompt(Cmd):
    prompt = 'dD> '
    intro = "Welcome to downDetector! Type help to list all commands."
    #Shell commands
    
    #Exits the program
    def do_exit(self, inp):
        print("Exiting")
        return True

    #Lists implemented challenges
    def do_list(self, inp):
        temp = "Challenges Implemented: "
        if len(challengesList) == 0:
            print("No challenges implemented")
        else:
            for entry in challengesList:
                temp = temp + entry.__class__.__name__ + ", "
            print(temp[0:-2])
    
    #Checks a target challenge or challenges
    def do_target(self, inp):
        inp = inp.split()
        for option in inp:
            if len(challengesList) == 0:
                log.debug("No challenges")
                print("No challenges implemented!")
            for i in challengesList:
                if i.__class__.__name__ == option:
                    check(i)
                else:
                    print(i + " is not a valid challenge!")
                    #raise InvalidChallengeError("{} is not a valid challenge".format(option))

    #Sets the default time between check cycles
    def do_timer(self, inp):
        try:
            int(inp)
        except ValueError:
            print("Not a valid input, please enter only integers greater than 0")
        if (int(inp) < 1):
            print("Not a valid input, please enter only integers greater than 0")
        timer = int(inp)
        print("Time between check cycles set to " + inp + " seconds.")

    #Sets number of threads to use
    def do_threads(self, inp):
        try:
            int(inp)
        except ValueError:
            print("Not a valid input, please enter only integers greater than 0")
        if (int(inp) < 1):
            print("Not a valid input, please enter only integers greater than 0")
        threads = int(inp)
        print("Number of threads set to " + inp)

    #Runs all checks
    def do_run(self):
        if len(challengesList) == 0:
            log.debug("No challenges")
            print("No challenges implemented.")
        pool = mp.Pool(processes=threads)
        results = [pool.apply(check, args=(x,)) for x in challengesList]

    #Command help sections
    def help_exit(self):
        print("Exits the program")

    def help_list(self):
        print("Prints the implemented challenges")

    def help_target(self):
        print("Checks the targeted challenges in order.")
        print("Syntax: target [challenge1] [challenge2] [challenge3]")

    def help_timer(self):
        print("Sets the amount of time between check cycles in seconds, default is 300.")
        print("Syntax: timer 300")

    def help_threads(self):
        print("Sets the number of threads to use during checks, default is 5.")
        print("Syntax: threads 5")

    def help_run(self):
        print("Checks all implemented challenges.")
    
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
    ''' 
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
        if args.processes < 1:
            raise IllegalInputError("Number of processes must be greater than or equal to one")
        pool = mp.Pool(processes=args.processes)
        results = [pool.apply(check, args=(x,)) for x in challengesList]
    '''
    myPrompt().cmdloop()
