from unittest import TestCase

from tdd.converter import infix_to_postfix


class TestConverter(TestCase):
    def test_operand(self):
        self.assertEqual(infix_to_postfix('1'), '1')

    def test_operation(self):
        self.assertEqual(infix_to_postfix('1*2+3'), '12*3+')
        self.assertEqual(infix_to_postfix('1+2*3'), '123*+')
        self.assertEqual(infix_to_postfix('1+2+3*4'), '12+34*+')

    def test_grouping(self):
        self.assertEqual(infix_to_postfix('(1+2)*3'), '12+3*')
        self.assertEqual(infix_to_postfix('1*(2*3+4*5)+6'), '123*45*+*6+')
        self.assertEqual(infix_to_postfix('(1+2)*3+(4-5)/6'), '12+3*45-6/+')
