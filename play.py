from run_parallel.run_parallel import run_parallel
import math

class Simulation:

    def __init__(self, n):
        self.n = n

    def __call__(self):
        return self.n

for res in run_parallel([Simulation(i) for i in range(100)]):
    print(res)
