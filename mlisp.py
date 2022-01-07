from operators import *
from typing import Callable
import re
import argparse


class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        super().__init__()
        self.update(zip(params, args))
        self.outer = outer

    def __getitem__(self, key):
        if key in self: return super().__getitem__(key)
        return self.outer[key] if self.outer else None


class Lambda(Callable):
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args):
        # return another lambda if partially evaluated
        if len(args) < len(self.params):
            return Lambda(self.params[len(args):], self.body, Env(self.params[:len(args)], args, self.env))

        # evaluate the whole lambda
        lambda_env = Env(self.params, args, self.env)
        eval_res = None

        # there might be multiple statements in the body
        for stmt in self.body:
            eval_res = eval(stmt, lambda_env)
        return eval_res


Symbol = str
Number = int
List = list
Exp = (Symbol, Number, List)
Arg = (bool, int, Lambda)

LETTER_REGEX = "[a-z]"
DIGIT_REGEX = "[0-9]"
SYMBOL_REGEX = f"{LETTER_REGEX}({LETTER_REGEX}|{DIGIT_REGEX}|-)*"
RESERVED_WORDS = ["mod", "and", "or", "not", "define", "fun", "if"]


def default_env() -> Env:
    env = Env()
    env.update({
        "+": add,
        "-": sub,
        "*": mul,
        "/": div,
        "<": lt,
        ">": gt,
        "=": eq,
        "mod": mod,
        "print-num": print_num,

        "and": and_,
        "or": or_,
        "not": not_,
        "print-bool": print_bool,
        "#t": True,
        "#f": False,
    })
    return env


def find_symbol(exp: Exp, env: Env):
    if isinstance(exp, Number): return exp
    if env[exp] is None:
        raise SyntaxError(f"unknown symbol '{exp}'")
    return env[exp]


def eval_if(args, env: Env):
    predicate, consequence, alternative = args
    bool_exp = eval(predicate, env)
    if not type(bool_exp) is bool:
        raise TypeError("if: predicate must be a boolean expression")
    res = consequence if eval(predicate, env) else alternative
    return eval(res, env)


def eval_define(args, env: Env):
    symbol, exp = args
    if symbol in RESERVED_WORDS:
        raise SyntaxError(f"reserved word '{symbol}' in define statement")
    if not re.fullmatch(SYMBOL_REGEX, symbol):
        raise SyntaxError(f"unexpected symbol '{symbol}', id must be in lowercase letters or digits")
    env[symbol] = eval(exp, env)


def eval_lambda(args, env: Env):
    params, *body = args
    return Lambda(params, body, env)


def eval(x: Exp, env: Env):
    if isinstance(x, Symbol) or isinstance(x, Number):
        return find_symbol(x, env)

    # x is an unevaluated expression, unwrap the expression
    op, *args = x

    if isinstance(op, Number): return op  # unwrap number

    # keyword functions
    if op == "if":
        return eval_if(args, env)
    elif op == "define":
        return eval_define(args, env)
    elif op == 'lambda' or op == 'fun':
        return eval_lambda(args, env)

    # function calls
    func = eval(op, env)
    if not isinstance(func, Callable):
        raise SyntaxError(f"operator not found: '{op}'")
    func_args = [eval(arg, env) for arg in args]
    for param, evaluated in zip(args, func_args):
        if not isinstance(evaluated, Arg):
            raise SyntaxError(f"unexpected '{param}'")
    return func(*func_args)


def tokenize(input_str: str) -> List:
    return input_str.replace("(", " ( ").replace(")", " ) ").split()


def read_exp(tokens: List) -> Exp:
    if len(tokens) == 0: raise SyntaxError("unexpected EOF")
    token = tokens.pop(0)
    if token == '(':
        exp = []
        while len(tokens) > 0 and tokens[0] != ')':
            exp.append(read_exp(tokens))
        if len(tokens) == 0: raise SyntaxError("unclosed bracket '('")
        tokens.pop(0)
        return exp
    elif token == ')':
        raise SyntaxError("unexpected ')'")
    else:
        return parse_literal(token)


def parse_program(input_str: str, verbose=False) -> Exp:
    if verbose: print("Tokenized result:", tokenize(input_str))
    return read_exp(tokenize(input_str))


def parse_literal(token: str):
    try: return Number(token)
    except ValueError: return Symbol(token)


def read_input():
    input_lines = []
    while True:
        try:
            line = input()
            if line == "end":
                break
            elif line:
                input_lines.append(line)
        except EOFError:
            break

    return "".join(input_lines)


def run_interpreter(input_str: str, verbose=False):
    program = parse_program(f"({input_str})", verbose)
    if verbose: print("Parsed program:", program)

    env = default_env()
    for statement in program:
        eval(statement, env)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-debug", dest="verbose", action="store_const", const=True, default=False, help="Debug mode")

    args = parser.parse_args()
    verbose = args.verbose

    input_str = read_input()
    if verbose: print("Input string:", input_str)
    run_interpreter(input_str, verbose)


if __name__ == "__main__":
    main()
