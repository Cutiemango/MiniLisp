# MiniLisp
## Development Environment and Tools
- Ubuntu 18.04 on Windows 10 WSL
- Python 3.8.10
- Python library
  - `argparse` for program flags
  - `functools` for operators
  - `typing` for type checking
  - `re` for syntax checking

## How to Use
Run the script by `python3 mlisp.py`, then you can enter your `Lisp` program.

You can keep entering your testcases, the interpreter will continue reading until an `end` token has been received.

After receiving the `end` token, the interpreter will output the result of your input.

## Testcases
Sample testcases (`.in` files) are located at `/testcase/test_data`.

By running `python3 checker.py`, the checker will automatically run through all the testcases and `diff` them. (**Linux** required!)

You can generate ground truth (TA's answer) by running `python3 gen_ans.py`.

## Debugging
You can see the interpreter logging message (helpful for debugging) by enabling the `-debug` flag.

(namely, run the script by `python3 mlisp.py -debug`)