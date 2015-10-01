strategies_per_type = {}


class GiveUp(Exception):
    pass


def shrink(validator, input):
    """
    # basic example
    >>> validator = lambda x: 1 == x[-1]
    >>> shrink(validator, {'x': [1, 2, 3]})
    (True, {'x': [1]})

    # It should return input as is for unknown structures
    >>> validator = lambda x: 1 == x[-1]
    >>> shrink(validator, {'x': None})
    (False, {'x': None})
    """
    simplified_input = input.copy()
    for var, value in input.items():
        strategy = strategies_per_type.get(type(value))
        if not strategy:
            continue
        simplified = strategy(value)
        while not validator(simplified):
            try:
                simplified = strategy(simplified)
            except GiveUp:
                break
        simplified_input[var] = simplified
        return True, simplified_input
    return False, simplified_input


def strategy_for(t_var):

    def wrap(fn):
        strategies_per_type[t_var] = fn
        return fn

    return wrap


@strategy_for(list)
def reduce_to_singleton(x):
    """
    >>> reduce_to_singleton([1, 2])
    [1]
    """
    if not x:
        raise GiveUp('Singleton list')
    return x[:-1]
