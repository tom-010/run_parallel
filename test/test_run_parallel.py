from unittest import TestCase
from run_parallel.run_parallel import run_parallel, is_iterable

class TestRunParallel(TestCase):
    
    def test_pass_empty_list(self):
        self.assertEqual([], run_parallel([]))

    def test_callable_classes(self):
        self.assertEqual([1, 2], run_parallel([
            self.CallableClass(1),
            self.CallableClass(2)
        ]))

    def test_pass_generator(self):
        generator = map(self.CallableClass, [1,2])
        self.assertEqual([1, 2], run_parallel(generator))

    def test_invalid_input(self):
        for invalid_input in [None, 0, 1.1, 1, set, [], {}]:
            self.assertEqual([], run_parallel(invalid_input), invalid_input)

    def test_partially_invalid_input(self):
        # the idea: everything is a function, but if it is not callable
        # it is a constant function, that always returns itself

        for invalid_input in [None, 0, 1.1, 1, [], {}]:
            partally_invalid_input = [
                self.CallableClass(1),
                invalid_input,
                self.CallableClass(2)
            ]
            self.assertEqual([1, invalid_input, 2], run_parallel(partally_invalid_input), partally_invalid_input)

    def test_wired_but_valid_input(self):
        for wired_input, expected in [(set, set())]:
            self.assertEqual([expected], run_parallel([wired_input]), wired_input)

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