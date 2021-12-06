from typing import Iterable, Iterator


def read() -> Iterator[str]:
    with open("d3/input.txt") as f:
        for line in f:
            yield line.strip()


def get_scores(numbers: Iterable[str]) -> list[int]:
    """Get the score for each digit.

    For each "1" add 1 for each "0" takeaway 1
    """

    total = None
    for num in numbers:
        if total is None:
            total = [0 for _ in range(len(num))]
        for i, digit in enumerate(num):
            if digit == "0":
                total[i] -= 1
            else:
                total[i] += 1
    assert total is not None
    return total


if __name__ == "__main__":
    scores = get_scores(read())
    print(
        int("".join("0" if i < 0 else "1" for i in scores), base=2)
        * int("".join("1" if i < 0 else "0" for i in scores), base=2)
    )
