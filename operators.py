from functools import wraps, reduce
import operator


def type_check(check_type: type):
    def wrapper(proceed: callable):
        @wraps(proceed)
        def checker(*args):
            for idx, arg in enumerate(args):
                if not type(arg) is check_type:
                    raise TypeError(f"{proceed.__name__}(): invalid type for argument {idx},"
                                    f" expected {check_type.__name__}, but found {type(arg).__name__}")
            return proceed(*args)

        return checker

    return wrapper


def argcount_check(rule: str):
    def wrapper(proceed: callable):
        @wraps(proceed)
        def checker(*args):
            allow_more = rule[-1] == '+'
            arg_count = int(rule[:-1]) if allow_more else int(rule)
            if (not allow_more and len(args) != arg_count) or (allow_more and len(args) < arg_count):
                raise SyntaxError(f"{proceed.__name__}(): expected {rule} arguments, got {len(args)}")
            return proceed(*args)

        return checker

    return wrapper


@argcount_check("1")
@type_check(bool)
def print_bool(x):
    print("#t" if x else "#f")


@argcount_check("1")
@type_check(int)
def print_num(x):
    print(x)


@argcount_check("2+")
@type_check(int)
def add(*args):
    return reduce(operator.add, args)


@argcount_check("2")
@type_check(int)
def sub(*args):
    return operator.sub(*args)


@argcount_check("2+")
@type_check(int)
def mul(*args):
    return reduce(operator.mul, args)


@argcount_check("2")
@type_check(int)
def div(*args):
    return operator.floordiv(*args)


@argcount_check("2")
@type_check(int)
def mod(*args):
    return operator.mod(*args)


@argcount_check("2")
@type_check(int)
def lt(*args):
    return operator.lt(*args)


@argcount_check("2")
@type_check(int)
def gt(*args):
    return operator.gt(*args)


@argcount_check("2+")
@type_check(int)
def eq(*args):
    return args.count(args[0]) == len(args)


@argcount_check("2+")
@type_check(bool)
def and_(*args):
    return reduce(operator.and_, args)


@argcount_check("2+")
@type_check(bool)
def or_(*args):
    return reduce(operator.or_, args)


@argcount_check("1")
@type_check(bool)
def not_(*args):
    return operator.not_(*args)
