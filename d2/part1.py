from typing import Iterable, Iterator, cast

import parse

instruction_parser = parse.compile("{command:w} {value:d}")


def read() -> Iterator[str]:
    with open("d2/input.txt") as f:
        for line in f:
            yield line.strip()


def parse_instruction(instruction) -> tuple[str, int]:
    result = instruction_parser.parse(instruction)
    assert result is not None
    result = cast(parse.Result, result)
    return result["command"], result["value"]


def evaluate(instructions: Iterable[tuple[str, int]]):
    position = 0
    depth = 0
    for command, value in instructions:
        match command:
            case "forward":
                position += value
            case "up":
                depth -= value
            case "down":
                depth += value
    return position, depth


if __name__ == "__main__":
    instructions = (parse_instruction(instruction) for instruction in read())
    position, depth = evaluate(instructions)
    print(position * depth)
