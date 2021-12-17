run_parallel
============

Pass an array or generator of callables and `run_parallel`
will run them as fast as possible.

Lambdas are not supported yet.

## Example

As computations are often a little bit complex, classes make 
sense often. Override the `__call__` method:

```python

class ExensiveComputation:

    def __init__(self, arg):
        self.arg = arg

    def __call__(self):
        res = self._step1(self.arg)
        res = self._step2(res)
        return res

    def _step1(self, arg):
        # expensive stuff here
        return res

    def _step2(self, arg):
        # expensive stuff here
        return res


computations = [ExensiveComputation(1), ExensiveComputation(2), ExensiveComputation(3)]
res1, res2, res3 = run_parallel(computations)

```

