# downDetector
automated challenge downtime detection and recovery tool, designed to recover CTF challenges hosted via Docker

## About
`downDetector` executes challenge objects to check if a CTF challenge is currently solvable and then redeploys the challenge if it is not
solvable.  It logs the checks and redeployment to a local file, by default downDetector.log, that is able to be customized and it uses
multithreading to speed up the checking and redeployment of challenges.  This started as a Bash script paired with cron to check and 
redeploy every 5 minutes, it was unfortunately not very modular or reusable for future competitions.  I then decided to rewrite it in 
python for use in future competitions, however it still needs to be paired with cron for automatic detection.

## Installation
To install downDetector follow these steps.

__Install the Requirements:__
```
pip3 install -r requirements.txt
```

__Customize for Challenges__:
To use in a competition you must build challenge objects in the challenges.py file.  A sample challenge is provided.
A challenge object requires a name, a host, a `solve` function, and a `redeployment` function.  All challenge objects should be initialized
in the downDetector.py file and then added to the challengesList list.

The `solve` function must return True or False, if the challenge is successfully solved and does not need to be redeployed the `solve` 
function must return True.  If at any point the challenge is unable to be solved or it shows vandalism the `solve` function should return 
False.  When the `solve` function returns False it triggers the `redeployment` function.

The `redeployment` function should use paramiko to ssh into the host of the challenge, bring down the docker instance or other host method,
and then redeploy it.

Best practices are require your challenge authors to submit their challenges with a `solve` function already made.  Since the 
`redeployment` function is very hosting solution dependent it should be made by the Competition Architect or competition Black Team.

## Usage
downDetector is host solution agnostic, the specific implementation of `solve` and `redeployment` should be tailored to your challenges
and hosting solution.

downDetector has multiple options, see below:

| Option | Description |
|-----------------|------------------------------------------------------------|
| -h | Help, displays the possible arguments |
| -v, --verbose | Turns on terminal display of log statements, useful in combination with -t |
| -t, --target | Used to specify challenges to test, supports multiple or an individual challenge |
| -l, --list | Lists the names of every initialized challenge |
| -f, --file | Used to specify the log file, defaults to downDetector.log |
| -p, --processes | Specifies the number of processes to use, defaults to 5 |

If the options -h, -t, or -l are not specified it will run through all initialized challenges.

## Acknowledgments

* Great thanks to micahjmartin for the help with getting started.
