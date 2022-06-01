from unittest import TestCase

from tdd.expr import evaluate_infix, evaluate_postfix, infix_to_postfix


class TestInfixToPostfix(TestCase):
    def test_converts_single_operand(self):
        self.assertEqual(infix_to_postfix('1'), '1')

    def test_converts_operations(self):
        self.assertEqual(infix_to_postfix('1*2+3'), '12*3+')
        self.assertEqual(infix_to_postfix('1+2*3'), '123*+')
        self.assertEqual(infix_to_postfix('1+2+3*4'), '12+34*+')

    def test_converts_operations_with_groupings(self):
        self.assertEqual(infix_to_postfix('(1+2)*3'), '12+3*')
        self.assertEqual(infix_to_postfix('1*(2*3+4*5)+6'), '123*45*+*6+')
        self.assertEqual(infix_to_postfix('(1+2)*3+(4-5)/6'), '12+3*45-6/+')


class TestEvaluatePostfix(TestCase):
    def test_evaluates_single_operand(self):
        self.assertEqual(evaluate_postfix('1'), 1)

    def test_evaluates_operations(self):
        self.assertEqual(evaluate_postfix('12*3+'), 5)
        self.assertEqual(evaluate_postfix('123*+'), 7)
        self.assertEqual(evaluate_postfix('12+34*+'), 15)

    def test_evaluates_operations_with_groupings(self):
        self.assertEqual(evaluate_postfix('12+3*'), 9)
        self.assertEqual(evaluate_postfix('123*45*+*6+'), 32)
        self.assertEqual(evaluate_postfix('12+3*45-6/+'), 8)


class TestEvaluateInfix(TestCase):
    def test_evaluates_single_operand(self):
        self.assertEqual(evaluate_infix('1'), 1)

    def test_evaluates_operations(self):
        self.assertEqual(evaluate_infix('1*2+3'), 5)
        self.assertEqual(evaluate_infix('1+2*3'), 7)
        self.assertEqual(evaluate_infix('1+2+3*4'), 15)

    def test_evaluates_operations_with_groupings(self):
        self.assertEqual(evaluate_infix('(1+2)*3'), 9)
        self.assertEqual(evaluate_infix('1*(2*3+4*5)+6'), 32)
        self.assertEqual(evaluate_infix('(1+2)*3+(4-5)/6'), 8)
