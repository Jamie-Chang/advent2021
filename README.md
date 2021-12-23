# advent2021
Advent of code solutions 2021 https://adventofcode.com

## Prerequisites
- Requires Python 3.10 or above.
- See [requirements.txt file](./requirements.txt)

### Parse
[parse](https://pypi.org/project/parse/) is a fantastic library that saves a lot of time. The idea is to use format strings that are commonly used in day-to-day coding as opposed to regexes.

## Development
### Setup Virtual Environment
This is only required for the first time setting up the `venv`.
```
$ python3.10 -m venv .venv
```

### Activate Virtual Environment
Do this before trying to execute the code.

```
$ . .venv/bin/activate
```

### Running a File
```
(.venv)$ python d1/part1.py
```

### Running Doctests
For convenience, tests are written in docstrings and can be run using doctests.
```
(.venv)$ python -m doctest d1/part1.py
```