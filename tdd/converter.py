from .stack import Stack

OPERATORS = {
    '*': 20,
    '/': 20,
    '+': 10,
    '-': 10,
    '(': 0,
    ')': 0,
}


def _get_precedence(operator: str) -> int:
    return OPERATORS[operator]


def infix_to_postfix(infix: str) -> str:
    stack = Stack(len(infix))
    postfix = ''

    for char in infix:
        if char.isdigit():
            postfix += char
            continue

        if char not in OPERATORS:
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
        elif _get_precedence(char) > _get_precedence(stack.peek()):
            stack.push(char)
        else:
            while not stack.is_empty and _get_precedence(
                char
            ) <= _get_precedence(stack.peek()):
                postfix += stack.pop()
            stack.push(char)

    while not stack.is_empty:
        postfix += stack.pop()

    return postfix
