# coding: utf-8
from six.moves import zip_longest


def tabulate(vals):
    # From pfmoore on GitHub:
    # https://github.com/pypa/pip/issues/3651#issuecomment-216932564
    assert len(vals) > 0

    sizes = [0] * max(len(x) for x in vals)
    for row in vals:
        sizes = [max(s, len(str(c))) for s, c in zip_longest(sizes, row)]

    result = []
    for row in vals:
        display = " ".join([str(c).ljust(s) if c is not None else ''
                            for s, c in zip_longest(sizes, row)])
        result.append(display)

    return result, sizes
