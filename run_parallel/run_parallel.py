
import multiprocessing
 

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