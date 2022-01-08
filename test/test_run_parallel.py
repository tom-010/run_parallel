from unittest import TestCase
from run_parallel.run_parallel import run_parallel, is_iterable, _run_in_parallel
import time 


class TestRunParallel(TestCase):
    
    # def test_pass_empty_list(self):
    #     self.assertEqual([], list(run_parallel([])))

    
    # def test_callable_classes(self):
    #     self.assertEqual([1, 2], list(run_parallel([
    #         self.CallableClass(1),
    #         self.CallableClass(2)
    #     ])))

    # def test_pass_generator(self):
    #     generator = map(self.CallableClass, [1,2])
    #     self.assertEqual([1, 2], list(run_parallel(generator)))

    def test_partially_invalid_input(self):
        # the idea: everything is a function, but if it is not callable
        # it is a constant function, that always returns itself

        for invalid_input in [None, 0, 1.1, 1, [], {}]:
            partally_invalid_input = [
                self.CallableClass(1),
                invalid_input,
                self.CallableClass(2)
            ]
            self.assertEqual([1, invalid_input, 2], list(run_parallel(partally_invalid_input)), partally_invalid_input)

    def test_wired_but_valid_input(self):
        for wired_input, expected in [(set, set())]:
            self.assertEqual([expected], list(run_parallel([wired_input])), wired_input)

    def test_easy_interface(self):
        self.assertEqual([1, 2], list(run_parallel(
            self.CallableClass(1),
            self.CallableClass(2)
        )))

    def test_passing_no_args(self):
        self.assertEqual([], list(run_parallel()))
    
    def test_passing_multiple_iterables(self):
        self.assertEqual([1, 2, 3, 4], list(run_parallel([
            self.CallableClass(1),
            self.CallableClass(2)
        ], [
            self.CallableClass(3),
            self.CallableClass(4)
        ])))

    def test_some_passed_iterables_are_none(self):
        self.assertEqual([1, 2, None, 1, set(), 3, 4], list(run_parallel([
            self.CallableClass(1),
            self.CallableClass(2)
        ],
        None, 
        1,
        set, 
        [
            self.CallableClass(3),
            self.CallableClass(4)
        ])))

    def test_passing_multiple_iterables_contain_invalid_inputs(self):
        self.assertEqual([1, 1, 3, None], list(run_parallel([
            self.CallableClass(1),
            1
        ], [
            self.CallableClass(3),
            None
        ])))

    def test_single_callable(self):
        self.assertEqual(1, run_parallel(self.CallableClass(1)))

    def test_single_callable_is_invalid_input(self):
        for invalid_input in [1, 1.1, None]:
            self.assertEqual(invalid_input, run_parallel(invalid_input))

    def test_single_callable_as_list(self):
        self.assertEqual([1], list(run_parallel([
            self.CallableClass(1)
        ])))

    class CallableClass:
        def __init__(self, res):
            self.res = res
        def __call__(self):
            return self.res


class TestIsIterable(TestCase):

    def test_true(self):
        positive_examples = [
            'abc',
            ['a'],
            [],
            {'a': 1},
            set([1, 2]),
            self.ClassWithGetItem(),
            self.ClassWithIter(),
            {}
        ]
        for positive_example in positive_examples:
            self.assertTrue(is_iterable(positive_example))

    def test_false(self):
        negative_examples = [
            self.BlankClass(),
            lambda x: x,
            1, 1.1, -1,
            None,
            self.ClassWithGetItem, # note type, not obj
            self.ClassWithIter, # note type, not obj
            list,
            set
        ]
        for negative_example in negative_examples:
            self.assertFalse(is_iterable(negative_example))

    class ClassWithGetItem:
        def __getitem__(self):
            return 1

    class ClassWithIter:
        def __iter__(self):
            return 1

    class BlankClass:
        pass

class SleepingJob:

    def __init__(self, seconds):
        self.seconds = seconds

    def __call__(self):
        time.sleep(self.seconds)
        return time.time() # report back the wakeup time


class TestDoNotStartInBatches(TestCase):

    def test_one_long_running_job(self):
        jobs = [
            SleepingJob(1),
            SleepingJob(0.1),
            SleepingJob(0.1),
            SleepingJob(0.1),
            SleepingJob(0.1),
        ]
        res = list(run_parallel(jobs, cores=2))
        
        first_job_end_time = res[0]
        
        # every job except the first should have been finished befoe
        # the first job
        for idx, other_job in enumerate(res[1:]):
            offset = other_job - first_job_end_time
            self.assertTrue(other_job < first_job_end_time, f'The job {idx} should have been completed BEFORE the first job. But it completed {offset*1000} milliseconds later')
