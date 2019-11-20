Author: DataFrogman

downDetector is a bash script designed to check if challenges are up via autosolving where able otherwise by polling for signs of life.  If the challenge is up it will log that otherwise it will ssh into the box, shut down the docker image(s) and then redeploy (rebuilding where applicable).  The files in the home directory are required to run the autosolve scripts except for downDetector2.sh, that file is used for testing a future build of it so that the current downDetector will still run and check challenges.  When you have the next version working, wait for the next sweep to pass then rm the current downDetector.sh and cp the downDetector2.sh to downDetector.sh

To set up the auto sweeps add the following entry to the crontab 0,5,10,15,20,25,30,35,40,45,50,55 \* \* \* \* ~/downDetector.sh

When a challenge must be brought down for extensive maintenance comment out that challenge's function call so that downDetector will not ruin your box while you are working on it.

=============================================================================================
This is a warning to people on the box not to touch stuff, also set it up with your ssh hosts in the /et/motd file so that black team/ops don't accidentally break it.

WHATEVER YOU DO DO NOT EDIT FILES IN THE HOME DIRECTORY
If you edit any of the files it is very likely that you will break the 
redeployment script and crash all of the challenges
