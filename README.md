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

## Results
### Personal Stats:
```
      --------Part 1--------   --------Part 2--------
Day       Time   Rank  Score       Time   Rank  Score
 25   04:46:20   5181      0   04:50:40   3452      0
 24   08:23:06   3039      0   09:09:19   3121      0
 23   15:34:57   8145      0   16:23:22   5393      0
 22   10:55:50  12083      0   12:25:28   5960      0
 21   08:19:52  13367      0   15:27:34  11010      0
 20   12:29:52  11680      0   12:41:20  11402      0
 19   12:26:53   5118      0   12:49:24   4967      0
 18   14:27:24   9545      0   14:38:19   9339      0
 17   07:20:43  13192      0   09:42:58  13601      0
 16   06:17:39   9177      0   08:06:45   9311      0
 15   04:19:18  10530      0   07:06:30  10527      0
 14   03:37:33  16018      0   04:10:24  10014      0
 13   04:04:48  14611      0   04:12:27  13702      0
 12   03:49:26  10494      0   04:15:03   9640      0
 11   00:30:00   2534      0   00:34:14   2537      0
 10   03:41:05  18588      0   03:52:52  16875      0
  9   03:15:13  18596      0   03:56:50  13471      0
  8   03:46:36  22848      0   04:34:51  12434      0
  7   01:50:47  16443      0   02:01:48  15557      0
  6   03:52:48  23815      0   04:18:10  18621      0
  5   07:19:14  26775      0   07:59:53  24915      0
  4   08:26:56  27811      0   08:37:33  25071      0
  3   10:04:19  62256      0   10:35:33  42214      0
  2   05:15:48  45203      0   05:18:02  41902      0
  1   10:04:54  56532      0   10:16:46  49244      0
```

