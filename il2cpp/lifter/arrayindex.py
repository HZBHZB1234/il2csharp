"""Conservative conversion from a native byte index to managed element units."""
import ast
from functools import lru_cache

from il2cpp.text import _term_up, strip_outer


@lru_cache(maxsize=4096)
def array_index_units(text, scale, stride):
    """Strip only outer positive constant multiplies/short left shifts.

    No division is emitted and no sums are distributed: the surviving text
    is copied unchanged. An unsupported C# expression or an unproved multiple
    declines. The small syntax/bounds limits also bound work on corrupt input.
    This models the already decoded address, not general C# shift semantics.
    """
    if not isinstance(text, str) or len(text) > 512 \
            or type(scale) is not int or scale not in (1, 2, 4, 8) \
            or type(stride) is not int or not 0 < stride < 0x100000:
        return None
    text = strip_outer(text)
    try:
        node = ast.parse(text, mode='eval').body
    except (SyntaxError, ValueError, TypeError, RecursionError):
        return None
    factor = scale
    while isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Mult, ast.LShift)):
        right = node.right
        if not isinstance(right, ast.Constant) or type(right.value) is not int:
            break
        value = right.value
        if isinstance(node.op, ast.LShift):
            # Larger shifts have width-dependent masking in C#; do not
            # reinterpret a shift-by-32 of an int as multiplication by 2^32.
            if not 0 <= value < 31:
                return None
            factor <<= value
        else:
            if value <= 0:
                return None
            factor *= value
        if factor > 0x7fffffff:
            return None
        node = node.left
    if factor % stride:
        return None
    unit = ast.get_source_segment(text, node)
    if not unit:
        return None
    factor //= stride
    return unit if factor == 1 else _term_up(unit, mul=True) + ' * ' + str(factor)
