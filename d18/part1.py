from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Iterable, Iterator, cast


@dataclass
class Node:
    value: tuple[Node, Node] | int

    def __add__(self, other: Node) -> Node:
        return reduce(Node((self, other)))

    def __iadd__(self, other: Node) -> Node:
        return self + other

    def increment(self, value: int) -> None:
        assert isinstance(self.value, int)
        self.value += value


def reduce(node: Node) -> Node:
    while True:
        if explode(node):
            continue
        if split(node):
            continue
        return node




def traverse(node: Node, depth: int = 0) -> Iterator[tuple[Node, int]]:
    """
    >>> node = Node(
    ...     (
    ...         Node((Node(2), Node(0))),
    ...         Node(
    ...             (
    ...                 Node(5),
    ...                 Node(
    ...                     (
    ...                         Node(
    ...                             (
    ...                                 Node(8),
    ...                                 Node(3),
    ...                             )
    ...                         ),
    ...                         Node(4),
    ...                     )
    ...                 ),
    ...             )
    ...         ),
    ...     ),
    ... )
    >>> expected = [
    ...     (Node((Node(2), Node(0))), 1),
    ...     (Node(5), 2),
    ...     (Node((Node(8), Node(3))), 3),
    ...     (Node(4), 3),
    ... ]
    >>> result = list(traverse(node))
    >>> assert result == expected, f"{result} != {expected}"
    """
    match node.value:
        case Node(tuple()) as left, Node(tuple()) as right:
            yield from traverse(left, depth + 1)
            yield from traverse(right, depth + 1)

        case Node(tuple()) as left, Node() as right:
            yield from traverse(left, depth + 1)
            yield right, depth + 1

        case Node() as left, Node(tuple()) as right:
            yield left, depth + 1
            yield from traverse(right, depth + 1)

        case _:
            # Leaf node
            yield node, depth


def explode(root: Node) -> bool:
    """
    >>> import copy
    >>> node = Node(
    ...     (
    ...         Node((Node(2), Node(0))),
    ...         Node(
    ...             (
    ...                 Node(5),
    ...                 Node(
    ...                     (
    ...                         Node(
    ...                             (
    ...                                 Node(8),
    ...                                 Node(3),
    ...                             )
    ...                         ),
    ...                         Node(4),
    ...                     )
    ...                 ),
    ...             )
    ...         ),
    ...     ),
    ... )
    >>> expected = copy.deepcopy(node)
    >>> explode(node)
    False
    >>> assert node == expected, f"{node} != {expected}"


    >>> node = Node(
    ...     (
    ...         Node(
    ...             (
    ...                 Node((Node(2), Node(0))),
    ...                 Node(
    ...                     (
    ...                         Node(5),
    ...                         Node((Node((Node(8), Node(3))), Node(4))),
    ...                     )
    ...                 ),
    ...             ),
    ...         ),
    ...         Node(2),
    ...     )
    ... )
    >>> explode(node)
    True
    >>> expected = Node(
    ...     (
    ...         Node(
    ...             (
    ...                 Node((Node(2), Node(0))),
    ...                 Node((Node(13), Node((Node(0), Node(7))))),
    ...             )
    ...         ),
    ...         Node(2),
    ...     )
    ... )
    >>> assert node == expected, f"{node} != {expected}"
    """
    predecessor: Node | None = None
    right_value: int | None = None
    for node, depth in traverse(root):
        if right_value is not None:
            match node.value:
                case Node() as left, _:
                    left.increment(right_value)

                case _:
                    node.increment(right_value)

            return True

        match node.value:
            case Node(int() as l), Node(int() as r) if depth >= 4:
                if predecessor is not None:
                    predecessor.increment(l)
                node.value = 0
                right_value = r

        match node.value:
            case _, right:
                predecessor = right

            case _:
                predecessor = node

    return right_value is not None


def split(root: Node) -> bool:
    """
    >>> node = Node(11)
    >>> split(node)
    True
    >>> assert node == Node((Node(5), Node(6)))

    >>> node = Node((Node(5), Node(6)))
    >>> split(node)
    False
    >>> assert node == Node((Node(5), Node(6)))
    """
    for node, _ in traverse(root):
        match node.value:
            case Node(int() as value) as left, _ if value >= 10:
                left.value = (Node(value // 2), Node(value - value // 2))
                return True
            case _, Node(int() as value) as right if value >= 10:
                right.value = (Node(value // 2), Node(value - value // 2))
                return True
            case int() as value if value >= 10:
                node.value = (Node(value // 2), Node(value - value // 2))
                return True

    return False


def magnitude(node: Node) -> int:
    """
    >>> magnitude(parse_one("[[1,2],[[3,4],5]]"))
    143
    """

    match node.value:
        case int() as v:
            return v
        case Node() as left, Node() as right:
            return 3 * magnitude(left) + 2 * magnitude(right)
        case _:
            assert False



def read() -> Iterator[str]:
    with open("d18/input.txt") as f:
        for line in f:
            yield line.strip()


def parse_one(line: str) -> Node:
    return _parse_literal(ast.literal_eval(line))


def parse(lines: Iterable[str]) -> Iterator[Node]:
    """
    >>> [result] = list(parse(["[[2,0],[5,[[8,3],4]]]"]))
    >>> expected = Node(
    ...     (
    ...         Node((Node(2), Node(0))),
    ...         Node(
    ...             (
    ...                 Node(5),
    ...                 Node(
    ...                     (
    ...                         Node(
    ...                             (
    ...                                 Node(8),
    ...                                 Node(3),
    ...                             )
    ...                         ),
    ...                         Node(4),
    ...                     )
    ...                 ),
    ...             )
    ...         ),
    ...     ),
    ... )
    >>> assert result == expected, f"{result} != {expected}"
    """
    for line in lines:
        yield parse_one(line)


def _parse_literal(literal: int | list) -> Node:
    if isinstance(literal, int):
        return Node(literal)

    return Node(
        cast(
            tuple[Node, Node],
            tuple(_parse_literal(value) for value in literal),
        )
    )


if __name__ == "__main__":
    nodes = parse(read())
    print(magnitude(sum(nodes, start=next(nodes))))
