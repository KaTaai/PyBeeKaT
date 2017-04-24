import random
class Dice(object):
    
    def __init__(self,seed=None):
        self.rnd = random.Random()
        self.rnd.seed(seed)

    
    def uniform(self, a, b):
        return self.rnd.uniform(a,b)

    
    def uniformInt(self, a, b):
        return self.rnd.randint(a, b)