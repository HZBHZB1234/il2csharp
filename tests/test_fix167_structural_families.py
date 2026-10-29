"""Fix 167: two structural bugs behind the last parse-error files.

Both were found by re-emitting the game-only tree's 28 parse-error files
and bisecting the pass that changed the line.

A. `_elseif_flatten.negate` peeled `!(` ... `)` by slicing `cond[2:-1]`
   whenever the text merely STARTED with `!(`. For `!(A) | (B)` that
   cut from the `!` to the LAST `)`, leaving the stray tail `A) | (B`,
   which rendered an unparseable `if (A) | (B)` head
   (RpgArtifactEffect_KillSpawnBlackFluid.ProcessBursting).

B. `_seh_emit_clause` appended `}` + the clause at the END of the buffer
   for a late close. A HOISTED region reaches its close on the teardown
   `return`, by which time the try frame was popped and -- because
   `_seh_close_top_try` skips hoisted regions -- the try's own `}` was
   never written. The `}` already in the buffer belonged to the
   ENCLOSING block, so the finally landed after it:
   `try { ... goto L; } } finally { }`. The fix inserts the missing `}`
   plus the clause BEFORE the brace that balances the try's `{`.
"""
import pytest

from il2cpp.dec import Decompiler


_DEC = None


def _dec():
    global _DEC
    if _DEC is None:
        _DEC = Decompiler.__new__(Decompiler)
    return _DEC


# -- A: the negate slice ---------------------------------------------------

def _elseif_case(cond):
    return ['if (%s)' % cond, '{', '    x();', '}', 'else',
            '{', '    if (C)', '{', '        y();', '}', '}']


def test_elseif_flatten_keeps_a_pipe_condition_intact():
    """`!(A) | (B)` is not `!(...)`; the old slice left `A) | (B`."""
    dec = _dec()
    out = dec._elseif_flatten(_elseif_case('!(A) | (B)'))
    assert out[0] == 'if (!(A) | (B))', out
    assert out[4] == 'else if (C)', out


def test_elseif_flatten_still_negates_a_simple_comparison():
    dec = _dec()
    out = dec._elseif_flatten(_elseif_case('!(A == B)'))
    assert out[0] == 'if (!(A == B))', out


def test_elseif_flatten_plain_condition_unchanged():
    dec = _dec()
    out = dec._elseif_flatten(_elseif_case('A'))
    assert out[0] == 'if (A)', out


# -- B: the SEH brace splice ----------------------------------------------

def _seh_host():
    """A Decompiler with only what the splice path touches."""
    dec = _dec()
    dec._bstack = []
    dec._seh_regions = []
    return dec


def test_matching_brace_finds_the_balancing_close():
    dec = _seh_host()
    out = ['try', '{', '  a();', '  if (x)', '  {', '    b();', '  }', '}',
           'after;']
    assert dec._seh_matching_brace(out, 0) == 7


def test_matching_brace_is_literal_aware():
    """A `"{"` inside a string must not shift the depth."""
    dec = _seh_host()
    out = ['try', '{', '  s = "{{{";', '}', 'after;']
    assert dec._seh_matching_brace(out, 0) == 3


def test_matching_brace_declines_when_not_a_try():
    dec = _seh_host()
    assert dec._seh_matching_brace(['if (x)', '{', '}'], 0) is None
    assert dec._seh_matching_brace(['try', '{', 'a();'], 0) is None
    assert dec._seh_matching_brace([], 0) is None


def test_matching_brace_ignores_a_line_comment():
    dec = _seh_host()
    out = ['try', '{', '  a(); // {', '}']
    assert dec._seh_matching_brace(out, 0) == 3
