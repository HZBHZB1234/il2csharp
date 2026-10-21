"""Per-type parallel emission: planning, batching, and worker deltas.

A single monolithic image (Assembly-CSharp is ~176k bodies in ONE image) used
to be forced serial because `--workers` only split ACROSS images. The pool now
runs over per-image, per-top-type tasks, so one big image uses every core. The
correctness contract is unchanged: every task writes only its own type file,
and the per-assembly tail (`__SharedBodyStubs.cs`/`__Addr.cs`/`.csproj`) is
written once by the parent from the collected union, so the tree is byte-
identical to the serial build. `test_game_parallel_build.py` proves the bytes;
these prove the arithmetic and the decline rules with stubs.
"""
from types import SimpleNamespace as NS

import pytest

import il2cpp.cli as cli
from il2cpp.cli import (_split_balanced, _worker_count, _worker_emit_types)


def _args(**kw):
    base = dict(workers=1, max_methods=None, asm=False, decls_only=False,
                verbose=False, types=None, out='out', quiet=False, bodies=None)
    base.update(kw)
    return NS(**base)


def _images(n):
    return [NS(name='a%d.dll' % i) for i in range(n)]


# ---------------------------------------------------------- batching

def test_split_balanced_is_contiguous_and_covers_everything():
    items = [(i, 't%d' % i) for i in range(10)]
    chunks = _split_balanced(items, 3)
    assert [len(c) for c in chunks] == [3, 3, 3, 1]
    # contiguous and lossless: order preserved, every item present once
    flat = [x for c in chunks for x in c]
    assert flat == items


def test_split_balanced_batch_one_and_empty():
    items = [(i, 't') for i in range(3)]
    assert [len(c) for c in _split_balanced(items, 1)] == [1, 1, 1]
    assert _split_balanced([], 4) == []
    # a batch of 0 or negative is clamped to 1, never an infinite loop
    assert [len(c) for c in _split_balanced(items, 0)] == [1, 1, 1]
    assert [len(c) for c in _split_balanced(items, -5)] == [1, 1, 1]


# --------------------------------------------------- worker count rules

def test_single_image_no_longer_forced_serial():
    # the whole point: one image can now use the per-type pool
    assert _worker_count(_args(workers=8), _images(1)) == (8, None)


def test_max_methods_still_declines_even_for_one_image():
    workers, note = _worker_count(_args(workers=8, max_methods=10), _images(1))
    assert workers == 1 and '--max-methods' in note


def test_bodies_still_declines_even_for_one_image():
    workers, note = _worker_count(_args(workers=8, bodies='b.json'), _images(1))
    assert workers == 1 and '--bodies' in note


# ------------------------------------------------ per-type worker deltas

class _StubEmitter:
    """Minimal stand-in for the per-task Emitter used by _worker_emit_types."""

    def __init__(self):
        self.out_dir = 'out'
        self.lifted = self.failed = self.fallbacks = self.emit_failed = 0
        self.lifter = object()
        self.seen = []
        self.fail_index = None

    def _assembly_dir_name(self, name):
        return name[:-4] if name.lower().endswith('.dll') else name

    def _emit_one_top(self, td, img_name, asm_dir, base):
        if td.index == self.fail_index:   # simulate an emission failure
            raise ValueError('boom')
        self.seen.append((td.index, base, asm_dir))
        self.lifted += 1
        sub = {'%08x' % td.index} if td.index % 2 else set()
        raw = (td.index % 3 == 0)
        return sub, raw


def _install_stub(monkeypatch, images, typedefs, fail_index=None):
    em = _StubEmitter()
    em.fail_index = fail_index
    # _worker_emit_types calls _worker_make_emitter(*_W['emitter_args']); make
    # that install our stub (and its args a harmless tuple), and give it meta.
    monkeypatch.setattr(cli, '_W', {
        'emitter_args': (), 'em': em,
        'meta': NS(images=images, typedefs=typedefs)}, raising=False)
    monkeypatch.setattr(cli, '_worker_make_emitter',
                        lambda *a, **k: cli._W.__setitem__('em', em),
                        raising=False)
    return em


def test_worker_emit_types_reports_deltas_and_union(monkeypatch):
    images = [NS(name='x.dll')]
    typedefs = [NS(index=i) for i in range(6)]
    em = _install_stub(monkeypatch, images, typedefs)
    items = [(i, 'T%d' % i) for i in range(6)]
    r = _worker_emit_types(('x.dll', items))
    assert r['files'] == 6 and r['lifted'] == 6 and r['failed'] == 0
    assert r['error'] is None
    # odd indices contribute a sub VA; raw is any(i%3==0)
    assert r['sub'] == {'%08x' % i for i in range(6) if i % 2}
    assert r['raw'] is True
    # file names come straight from the plan (never re-derived)
    assert [s[1] for s in em.seen] == ['T%d' % i for i in range(6)]


def test_worker_emit_types_reports_an_unknown_image(monkeypatch):
    _install_stub(monkeypatch, [NS(name='x.dll')], [NS(index=0)])
    r = _worker_emit_types(('missing.dll', [(0, 'T0')]))
    assert r['files'] == 0 and 'image not found' in r['error']


def test_worker_emit_types_captures_a_type_failure(monkeypatch):
    _install_stub(monkeypatch, [NS(name='x.dll')],
                  [NS(index=0), NS(index=1)], fail_index=1)
    r = _worker_emit_types(('x.dll', [(0, 'ok'), (1, 'boom')]))
    assert r['files'] == 1                      # the first type went through
    assert 'boom' in r['error'] and 'type 1' in r['error']
