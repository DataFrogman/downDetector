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

"""
Place Challenge classes here
"""
