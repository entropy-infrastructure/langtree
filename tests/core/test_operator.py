import unittest
from langtree.core import Operator
from langtree.operators import chainable


class TestOperator(unittest.TestCase):

    def test_default_behavior(self):
        operator = Operator()
        result = operator(foo='bar')
        self.assertEqual(result, {'foo': 'bar'})

    def test_custom_call(self):
        custom_call = lambda **kwargs: {'a': kwargs.get('a', 0) * 2}
        operator = Operator(call=custom_call)
        self.assertEqual(operator(a=5), {'a': 10})

    def test_custom_parse(self):
        custom_parse = lambda output: {k: -v for k, v in output.items()}
        operator = Operator(parse=custom_parse)
        self.assertEqual(operator(a=5), {'a': -5})

    def test_freeze_call(self):
        operator = Operator()
        operator.freeze_call(foo='frozen')
        self.assertEqual(operator(1, 2, 3), {'foo': 'frozen'})

    def test_freeze_parse(self):
        custom_parse = lambda output, multiply=1: {k: v * multiply for k, v in output.items()}
        operator = Operator(parse=custom_parse)
        operator.freeze_parse(multiply=10)
        self.assertEqual(operator(a=5), {'a': 50})

    def test_chainable_decorator(self):
        @chainable
        def custom_call(**kwargs):
            return {'result': kwargs.get('value', 0) + 10}

        chained_call = custom_call(value=5)
        operator = Operator(call=chained_call)
        self.assertEqual(operator(), {'result': 15})

    def test_none_parse(self):
        operator = Operator(parse=None)
        result = operator(foo='bar')
        self.assertEqual(result, {'foo': 'bar'})


if __name__ == '__main__':
    unittest.main()
