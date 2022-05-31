import unittest

from stack import Stack
from stack.stack import StackOverflowError


class TestStack(unittest.TestCase):
    def test_push(self):
        stack = Stack(1)
        stack.push(5)

        self.assertEqual(stack.peek(), 5)

    def test_pop(self):
        stack = Stack(2)
        stack.push(5)
        stack.push(7)

        self.assertEqual(stack.pop(), 7)
        self.assertEqual(stack.pop(), 5)

    def test_is_full_false(self):
        stack = Stack(1)

        self.assertFalse(stack.is_full)

    def test_is_full_true(self):
        stack = Stack(0)

        self.assertTrue(stack.is_full)

    def test_is_empty_false(self):
        stack = Stack(1)
        stack.push(5)

        self.assertFalse(stack.is_empty)

    def test_is_empty_true(self):
        stack = Stack(1)

        self.assertTrue(stack.is_empty)

    def test_stack_size_type_error(self):
        with self.assertRaises(TypeError) as ex:
            Stack('not int')

        self.assertEqual(
            str(ex.exception), 'Stack size must be an integer, not str'
        )

    def test_stack_overflow_error(self):
        with self.assertRaises(StackOverflowError) as ex:
            Stack(0).push(5)

        self.assertEqual(str(ex.exception), 'Stack is full')
