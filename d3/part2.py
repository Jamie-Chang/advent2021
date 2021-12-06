from typing import Iterable, Iterator


def read() -> Iterator[str]:
    with open("d3/input.txt") as f:
        for line in f:
            yield line.strip()


def get_bit(numbers: list[str], position: int) -> Iterator[int]:
    for num in numbers:
        yield int(num[position])


def get_score(bits: Iterable[int]) -> int:
    """Get the score.

    For each "1" add 1 for each "0" takeaway 1
    """
    return sum(-1 if bit == 0 else 1 for bit in bits)


def oxygen_generator_rating(numbers: list[str], digits: int) -> str:
    for i in range(digits):
        keep = "1" if get_score(get_bit(numbers, i)) >= 0 else "0"
        numbers = [num for num in numbers if num[i] == keep]
        if len(numbers) == 1:
            return numbers[0]
    assert False


def CO2_scrubber_rating(numbers: list[str], digits: int) -> str:
    for i in range(digits):
        keep = "0" if get_score(get_bit(numbers, i)) >= 0 else "1"
        numbers = [num for num in numbers if num[i] == keep]
        if len(numbers) == 1:
            return numbers[0]
    assert False


if __name__ == "__main__":
    numbers = list(read())
    digits = len(numbers[0])
    print(
        int(oxygen_generator_rating(numbers, digits), base=2)
        * int(CO2_scrubber_rating(numbers, digits), base=2)
    )
