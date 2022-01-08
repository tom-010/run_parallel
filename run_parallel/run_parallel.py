
import multiprocessing
import itertools
from itertools import islice
from queue import Queue
 

def run_parallel(*args, cores=None):
    """
    Takes a list of callables and runs them as fast as possible
    on the system CPU.
    If the list is not iterable, the function returns an empty 
    list.

    You can either call it:
    * run_parallel(Callable, Callable, Callable)
    * run_parallel([Callable, Callable, Callable])
    * run_parallel(generator)
    * run_parallel([Callable, Callable], [Callable, Callable])
    * run_parallel([Callable, Callable], generator)


    If there is a callable that cann not be called, it is regarded
    as constant function, that always returns itself. For example 
    the not callable object 1 will always return 1, or the type 
    (not object of) set will always return itself. 
    """
    if len(args) == 0:
        return []
    elif len(args) == 1:
        callables = args[0]
        if not is_iterable(args[0]):
            if callable(args[0]):
                return args[0]()
            else:
                return args[0]
    else:
        callables = _collapse_args(args)

    if not is_iterable(callables):
        return []

    if not cores:
        cores = multiprocessing.cpu_count()
    return _run_in_parallel(callables, cores)


class Worker:

    def __init__(self, job_queue, result_queue):
        self.job_queue = job_queue
        self.result_queue = result_queue
        self.processes = []

    def work(self):
        processes = []
        while True:
            try:
                job_number, job = self.job_queue.get_nowait()
            except Exception:
                return # done
            
            process = multiprocessing.Process(target=_queue_worker, args=(job, job_number, self.result_queue))
            process.daemon = True
            process.start()
            self.processes.append(process)

    def join(self):
        for process in self.processes:
            process.join()



def _run_in_parallel(fns, cores):
   with multiprocessing.Pool(cores) as pool:
        results = [pool.apply_async(_worker, (fn,)) for fn in fns]
        for res in results:
            yield res.get()

def _worker(job):
    if callable(job):
        return job()
    else:
        return job


def _queue_worker(job, job_number, output):
    if callable(job):
        output.put((job_number, job()))
    else:
        output.put((job_number, job))


def _partition(iterable, n):
    it = iter(iterable)
    return iter(lambda: tuple(islice(it, n)), ())

# for ret in _run_in_parallel([lambda: 1, lambda: 2, lambda: 3], 2):
#     print(ret)

def _collapse_args(args):
    callables = []
    for arg in args:
        if is_iterable(arg):
            for c in arg:
                callables.append(c)
        else:
            callables.append(arg)
    return callables


def is_iterable(obj):
    """
    This function checks if a given object is iterable without raising 
    errors. 
    Try to use iter(obj) would be preferable, but we don't know how 
    expensive this function is as the user can pass arbitary generators.
    """
    has_required_methods = hasattr(obj, '__iter__') or hasattr(obj, '__getitem__')
    return has_required_methods and not isinstance(obj, type)