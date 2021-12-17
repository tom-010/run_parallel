from run_parallel.run_parallel import run_parallel
import math

class Simulation:

    def __init__(self, n):
        self.n = n

    def __call__(self):
        res = 0
        for i in range(self.n):
            res += math.sin(i * self.n)
        return res / self.n

for res in run_parallel([Simulation(1000000+i) for i in range(100)]):
    print(res)
