
import multiprocessing
import itertools
 

 

def run_parallel(*args):
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

    return _run_in_parallel(callables, multiprocessing.cpu_count())


def _run_in_parallel(fns, cores):
    for chunk in _partition(fns, cores):
        manager = multiprocessing.Manager()
        output = manager.dict()
        processes = []
        for idx, fn in enumerate(chunk):
            process = multiprocessing.Process(target=_worker, args=(fn, idx, output))
            process.start()
            processes.append(process)
        for process in processes:
            process.join()
        for i in range(len(chunk)):
            yield output[i]

def _worker(job, idx, output):
    output[idx] = job()

def _partition(l, size):
    for i in range(0, len(l), size):
        yield list(itertools.islice(l, i, i + size))

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

def _fn_for_map(fn):
    return fn() if callable(fn) else fn

def is_iterable(obj):
    """
    This function checks if a given object is iterable without raising 
    errors. 
    Try to use iter(obj) would be preferable, but we don't know how 
    expensive this function is as the user can pass arbitary generators.
    """
    has_required_methods = hasattr(obj, '__iter__') or hasattr(obj, '__getitem__')
    return has_required_methods and not isinstance(obj, type)