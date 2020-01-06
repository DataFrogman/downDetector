import requests
import paramiko

class Challenge(object):

    def __init__(self, host, name):
        self.host = host
        self.name = name

    def solve(self):
        """This is the solver to check if a challenge is up or vandalized.
        IT MUST BE DEFINED.

        Return True if the challenge passes all checks, return False at the first failure
        """

        raise NotImplementedError("{} has not implemented the 'solve' function".format(self.__class__.__name__))

    def redeployment(self):
        """This function is called every time the challenge fails the 'solve' function.
        It redeploys the challenge, assuming that it has been vandalized or broken.
        IT MUST BE DEFINED.
        """

        raise NotImplementedError("{} has not implemented the 'redeployment' function".format(self.__class__.__name__))

""" Sample implementation for a challenge that is just a webpage with the flag on it
class sample(Challenge):
    def __init__(self, host, name, keyfile):
        self.host = host
        self.name = name
        self.flag = "RITSEC{sample}"
        self.port = 8080
        self.key = keyfile

    def solve(self):
        try:
            response = requests.get('http://{}:{}'.format(self.host, self.port))
        except:
            return False
        if self.flag in response.text:
            return True
        else:
            return False

    def redeployment(self):
        k = paramiko.RSAKey.from_private_key_file(self.key)
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, port=22, username="datafrogman", pkey=k)
        stdin, stdout, stderr = ssh.exec_command("cd sample; sudo docker-compose down; sudo docker-compose up -d")
        ssh.close()
"""
