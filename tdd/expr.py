from operator import add, floordiv, mul, sub
from typing import Callable, Iterable

from .stack import Stack


class OperatorMeta(type):
    _OPERATORS: Iterable

    def __contains__(self, obj: object) -> bool:
        return obj in self._OPERATORS


class Operator(metaclass=OperatorMeta):
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    OPENING_PAREN = '('
    CLOSING_PAREN = ')'

    _OPERATORS = [
        PLUS,
        MINUS,
        TIMES,
        DIVIDE,
        OPENING_PAREN,
        CLOSING_PAREN,
    ]

    _PRECEDENCES = {
        TIMES: 20,
        DIVIDE: 20,
        PLUS: 10,
        MINUS: 10,
        OPENING_PAREN: 0,
        CLOSING_PAREN: 0,
    }

    _OPERATIONS = {
        PLUS: add,
        MINUS: sub,
        TIMES: mul,
        DIVIDE: floordiv,
    }

    @classmethod
    def get_precedence(cls, operator: str) -> int:
        return cls._PRECEDENCES[operator]

    @classmethod
    def get_operation(cls, operator: str) -> Callable[[int, int], int]:
        return cls._OPERATIONS[operator]


def infix_to_postfix(infix: str) -> str:
    stack = Stack(len(infix))
    postfix = ''

    for char in infix:
        if char.isdigit():
            postfix += char
            continue

        if char not in Operator:
            continue

        if char == '(':
            stack.push(char)
            continue

        if char == ')':
            while stack.peek() != '(':
                postfix += stack.pop()
            stack.pop()
            continue

        if stack.is_empty:
            stack.push(char)
        elif Operator.get_precedence(char) > Operator.get_precedence(stack.peek()):
            stack.push(char)
        else:
            while not stack.is_empty and Operator.get_precedence(
                char
            ) <= Operator.get_precedence(stack.peek()):
                postfix += stack.pop()
            stack.push(char)

    while not stack.is_empty:
        postfix += stack.pop()

    return postfix


def evaluate_postfix(postfix: str) -> int:
    stack = Stack(len(postfix))
    result = 0

    for char in postfix:
        if char.isdigit():
            stack.push(int(char))
        elif char in Operator:
            b = stack.pop()
            a = stack.pop()
            stack.push(Operator.get_operation(char)(a, b))

    while not stack.is_empty:
        result += stack.pop()

    return result


def evaluate_infix(infix: str) -> int:
    return evaluate_postfix(infix_to_postfix(infix))
