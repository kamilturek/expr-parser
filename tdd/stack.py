from typing import Any


class Stack:
    def __init__(self, size: int):
        if not isinstance(size, int):
            raise TypeError(
                f'Stack size must be an integer, not {size.__class__.__name__}'
            )

        self._size = size
        self._elements: list[Any] = []

    @property
    def is_full(self) -> bool:
        return len(self._elements) == self._size

    @property
    def is_empty(self) -> bool:
        return len(self._elements) == 0

    def push(self, element: Any) -> None:
        if self.is_full:
            raise StackOverflowError('Stack is full')

        self._elements.append(element)

    def peek(self) -> Any:
        return self._elements[-1]

    def pop(self) -> Any:
        return self._elements.pop()


class StackOverflowError(Exception):
    pass
