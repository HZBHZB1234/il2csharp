from il2cpp.prelude import *  # noqa: F401,F403
from il2cpp.arm64 import is_arm64_binary
from il2cpp.binary import ELF, load_binary
from il2cpp.emitter import Emitter
from il2cpp.headers import HeaderEmitter
from il2cpp.metadata import Metadata
from il2cpp.runtime.core import Il2Cpp

def find_game_files(path=None, *, metadata=None, binary=None):
    """Discover one unambiguous pair; explicit files always take priority.

    Directory targets are a boundary: never pair them with a parent game's
    binary. Direct metadata files may use the standard Unity ancestor layout.
    Discovery reads directories only and never executes the native binary.
    """
    def explicit(value, label):
        if value is None:
            return None
        value = os.path.abspath(os.fspath(value))
        if not os.path.isfile(value):
            raise ValueError('%s file does not exist: %s' % (label, value))
        return value

    def pick(paths, label, flag):
        paths = sorted(set(paths))
        if len(paths) > 1:
            raise ValueError('multiple %s files found; select one with %s: %s' % (
                label, flag, ', '.join(paths)))
        return paths[0] if paths else None

    def scan(root, names):
        found = []
        for directory, dirs, files in os.walk(root):
            dirs.sort()
            for name in sorted(files):
                if name.casefold() in names:
                    found.append(os.path.join(directory, name))
        return found

    gmd, bp = explicit(metadata, 'metadata'), explicit(binary, 'binary')
    root = None
    if path is not None:
        target = os.path.abspath(os.fspath(path))
        if os.path.isdir(target):
            root = target
        elif os.path.isfile(target):
            if os.path.basename(target).casefold() == 'global-metadata.dat' or target == gmd:
                gmd = gmd or target
            else:
                bp = bp or target
        elif not (gmd or bp):
            return None, None
    if gmd and bp:
        return gmd, bp
    if root is None:
        root = os.path.dirname(bp or gmd) if bp or gmd else None
        if root and gmd and not bp:
            # .../<Game>_Data/il2cpp_data/Metadata/global-metadata.dat
            parent = os.path.dirname(root)
            data_dir = os.path.dirname(parent)
            if os.path.basename(root).casefold() == 'metadata' and \
                    os.path.basename(parent).casefold() == 'il2cpp_data' and \
                    os.path.basename(data_dir).casefold().endswith('_data'):
                root = os.path.dirname(data_dir)
    if root is None:
        return gmd, bp
    if gmd is None:
        gmd = pick(scan(root, {'global-metadata.dat'}), 'metadata', '--metadata')
    if bp is None:
        bp = pick(scan(root, {'gameassembly.dll', 'libil2cpp.so'}), 'binary', '--binary')
    return gmd, bp


# -- assembly emission ---------------------------------------------------

_W = {}


def _load_runtime(gmd, bp, verbose):
    """Read metadata + binary and resolve every method's native address.

    Mirrors the phase `main` runs before the image loop, factored out
    because a parallel build repeats it once per worker process. It keeps
    that phase whole: a worker that loaded less than the serial build would
    silently emit fewer bodies.
    """
    meta = Metadata(gmd)
    bin_ = load_binary(bp)
    if bin_ is None:
        raise ValueError('unsupported binary format')
    il = Il2Cpp(meta, bin_)
    il.verbose = verbose
    il.assign_images()
    try:
        il.find_registrations()
    except RuntimeError:
        # The Android loader assumes a different registration struct shape
        # and lands on a silently wrong registration for a PE; same gate as
        # `main`.
        if not isinstance(bin_, ELF):
            raise
        il.find_registrations_android()
    il.load_function_bounds()
    il.resolve_method_addrs()
    il._mod_ptr_cache.clear()  # free raw pointer arrays
    return meta, il


def _worker_init_runtime(gmd, bp, verbose):
    """Load metadata+binary once per worker process (the ~10-40s phase).

    Kept separate from the Emitter so a worker handling many small per-type
    tasks does not reload the runtime per task."""
    meta, il = _load_runtime(gmd, bp, verbose)
    _W['meta'], _W['il'] = meta, il


def _worker_make_emitter(out_dir, asm_comments, with_bodies, max_methods,
                         verbose, type_filter, publicize=False, raw_addr=False):
    """Build one Emitter over the already-loaded runtime; reused per task."""
    _W['em'] = Emitter(_W['il'], out_dir, asm_comments=asm_comments,
                       with_bodies=with_bodies, max_methods=max_methods,
                       verbose=verbose, type_filter=type_filter,
                       publicize=publicize, raw_addr=raw_addr)


def _worker_init(gmd, bp, out_dir, asm_comments, with_bodies, max_methods,
                 verbose, type_filter, publicize=False, raw_addr=False):
    """One runtime and one Emitter per worker process, reused for every
    image that process is handed (the load costs ~4-40s, an image ~12s)."""
    _worker_init_runtime(gmd, bp, verbose)
    _worker_make_emitter(out_dir, asm_comments, with_bodies, max_methods,
                         verbose, type_filter, publicize, raw_addr)


def _per_type_init(gmd, bp, out_dir, asm_comments, with_bodies, max_methods,
                   verbose, type_filter, publicize=False, raw_addr=False):
    """Pool initializer for the per-type pool: load the runtime ONCE, then
    mint a fresh Emitter per task inside `_worker_emit_types` (state isolation
    between tasks, single runtime load, same bytes as a serial build)."""
    _worker_init_runtime(gmd, bp, verbose)
    _W['emitter_args'] = (out_dir, asm_comments, with_bodies, max_methods,
                          verbose, type_filter, publicize, raw_addr)


def _worker_emit(image_name):
    """Emit one image (all its type files + per-assembly tail) and report
    per-image deltas.

    Deltas, not totals: the parent's running totals are then the serial
    ones, so `--workers N` prints the same log as `--workers 1`.
    """
    em, meta = _W['em'], _W['meta']
    img = next((i for i in meta.images if i.name == image_name), None)
    if img is None:
        return {'files': 0, 'lifted': 0, 'failed': 0, 'fallbacks': 0,
                'emit_failed': 0, 'lifter': em.lifter is not None,
                'error': 'image not found in metadata'}
    before = (em.lifted, em.failed, em.fallbacks, em.emit_failed)
    error = None
    try:
        files = em.write_assembly_split(img)
    except Exception as ex:
        files, error = 0, '%s: %s' % (type(ex).__name__, ex)
    after = (em.lifted, em.failed, em.fallbacks, em.emit_failed)
    return {'files': files, 'lifted': after[0] - before[0],
            'failed': after[1] - before[1],
            'fallbacks': after[2] - before[2],
            'emit_failed': after[3] - before[3],
            'lifter': em.lifter is not None, 'error': error}


def _worker_emit_types(payload):
    """Emit a batch of top-level types of one image; report deltas.

    `payload = (image_name, [(ti, base), ...])`: `ti` is a global TypeDef
    index (the parent planned the batch, including its final file base
    names, so the schedule never affects output). Each task builds its own
    Emitter over the shared runtime, so per-task state cannot leak. Only
    the type FILES are emitted here; the per-assembly tail
    (`__SharedBodyStubs.cs`/`__Addr.cs`/`.csproj`) is written once by the
    parent from the union of every task's `sub`/`raw`."""
    image_name, items = payload
    _worker_make_emitter(*_W['emitter_args'])
    em, meta = _W['em'], _W['meta']
    img = next((i for i in meta.images if i.name == image_name), None)
    if img is None:
        return {'files': 0, 'lifted': 0, 'failed': 0, 'fallbacks': 0,
                'emit_failed': 0, 'lifter': em.lifter is not None,
                'sub': set(), 'raw': False,
                'error': 'image not found: %s' % image_name}
    asm_dir = os.path.join(em.out_dir, em._assembly_dir_name(img.name))
    os.makedirs(asm_dir, exist_ok=True)
    before = (em.lifted, em.failed, em.fallbacks, em.emit_failed)
    files = 0
    sub = set()
    raw = False
    error = None
    for ti, base in items:
        try:
            s, r = em._emit_one_top(meta.typedefs[ti], img.name, asm_dir, base)
            sub |= s
            raw = raw or r
            files += 1
        except Exception as ex:
            error = '%s (type %d): %s: %s' % (image_name, ti, type(ex).__name__, ex)
            break
    after = (em.lifted, em.failed, em.fallbacks, em.emit_failed)
    return {'files': files, 'lifted': after[0] - before[0],
            'failed': after[1] - before[1],
            'fallbacks': after[2] - before[2],
            'emit_failed': after[3] - before[3],
            'sub': sub, 'raw': raw, 'error': error}


def _auto_workers():
    """Default width for `--workers 0`: half the cores, never more than 8.

    Both reasons are real. Memory: a worker holding a live runtime sits at
    423 MB resident after the load and 581 MB after the four heaviest
    assemblies, peaking at 672-783 MB, so twelve workers is ~8 GB of peak
    working set -- enough to die beside anything else running, which is
    what a 12-worker run did here. Politeness: a promotion build is not
    the only thing on the machine, and taking every core starves whatever
    else is running. An explicit `--workers N` still overrides this.
    """
    return max(1, min(8, (os.cpu_count() or 2) // 2))


def _worker_count(args, images):
    """Resolve --workers. A single image may now use the per-type pool,
    so only the whole-build brakes (--max-methods, --bodies) decline."""
    if args.workers < 0:
        return 0, '--workers must be >= 0'
    workers = args.workers if args.workers else _auto_workers()
    if workers < 2:
        return 1, None
    if args.max_methods is not None:
        # the cap is a whole-build brake; a per-worker cap would lift up
        # to N times the bodies that were asked for
        return 1, '--max-methods is a per-build cap; running --workers 1'
    if getattr(args, 'bodies', None):
        # --bodies is written by the parent's own Emitter; worker bodies
        # live in another process, so a pool would write the empty dict.
        return 1, '--bodies is collected parent-side; running --workers 1'
    return workers, None


def _weighted_order(images, meta):
    """Submission order for the pool: heaviest image first.

    The executor hands queued work to workers in submission order, so the
    image submitted last sets the tail. Counting native methods per image
    (`MethodDef.image` is filled by the parent's `assign_images`) is the
    cheap predictor of emit cost; ties keep metadata order because the
    sort is stable, and a caller without a metadata table gets that order
    unchanged.
    """
    if meta is None or not images:
        return list(images)
    try:
        counts = {}
        for m in meta.methods:
            if m.addr and m.image >= 0:
                counts[m.image] = counts.get(m.image, 0) + 1
        index = {img.name: i for i, img in enumerate(meta.images)}
        return sorted(images,
                      key=lambda img: -counts.get(index.get(img.name, -1), 0))
    except (AttributeError, TypeError):
        return list(images)


def _emit_assemblies(images, em, args, gmd, bp):
    """Emit every image, serially or across a per-type process pool.

    The pool runs over a flat list of per-image, per-top-type tasks (heaviest
    image's types first), so a single monolithic image (Assembly-CSharp is
    ~176k bodies in one image) uses every core instead of one. Every task
    writes only its own type file; the per-assembly files
    (`__SharedBodyStubs.cs`/`__Addr.cs`/`.csproj`) are written ONCE here in
    the parent from the collected union, so the tree is byte-identical to the
    serial build regardless of the schedule. Returns the serial counters
    either way (deltas summed in image order, so the log is the serial log).
    """
    quiet = getattr(args, 'quiet', False)
    workers, note = _worker_count(args, images)
    if note and not quiet:
        print('note: ' + note)
    t0 = time_ms()
    if workers < 1:
        workers = 1
    if workers == 1:
        total_files = 0
        for img in images:
            n = em.write_assembly_split(img)
            total_files += n
            if not quiet:
                print('  %-52s %5d types  (%d bodies, %d failed)' % (
                    img.name, n, em.lifted, em.failed), flush=True)
        return {'files': total_files, 'lifted': em.lifted,
                'failed': em.failed, 'fallbacks': em.fallbacks,
                'emit_failed': em.emit_failed, 'lifter': em.lifter is not None,
                'errors': []}
    from concurrent.futures import ProcessPoolExecutor
    initargs = (gmd, bp, args.out, args.asm, not args.decls_only,
                args.max_methods, args.verbose, args.types,
                getattr(args, 'publicize', False),
                getattr(args, 'raw_addr', False))
    # plan every image's top types up front, in metadata order (so the file
    # base names match serial); schedule the plan heaviest image first, then
    # split each image's plan into contiguous, size-balanced batches
    planned = {img.name: em._plan_top_files(img) for img in images}
    order = _weighted_order(images, getattr(em, 'meta', None))
    by_name = {img.name: img for img in images}
    jobs = []
    for img in order:
        items = [(td.index, base) for td, base in planned[img.name]]
        if items:
            for chunk in _split_balanced(items, max(1, len(items) // (workers * 4))):
                jobs.append((img.name, chunk))
    # say the width before the pool exists: a run killed part-way (a machine
    # under memory pressure will kill the parent, not a worker) otherwise
    # leaves a log that never mentions how wide it got
    if not quiet:
        print('workers: %d processes | %d images | %d type-tasks' % (
            workers, len(images), len(jobs)), flush=True)
    agg = {img.name: {'files': 0, 'lifted': 0, 'failed': 0, 'fallbacks': 0,
                      'emit_failed': 0, 'lifter': True, 'sub': set(),
                      'raw': False, 'error': None} for img in images}
    with ProcessPoolExecutor(max_workers=workers, initializer=_per_type_init,
                             initargs=initargs) as pool:
        for img_name, r in zip([j[0] for j in jobs], pool.map(_worker_emit_types, jobs)):
            a = agg[img_name]
            if r['error'] and not a['error']:
                a['error'] = r['error']
            a['files'] += r['files']
            a['lifted'] += r['lifted']
            a['failed'] += r['failed']
            a['fallbacks'] += r['fallbacks']
            a['emit_failed'] += r['emit_failed']
            a['lifter'] = a['lifter'] and r.get('lifter', True)
            a['sub'] |= r['sub']
            a['raw'] = a['raw'] or r['raw']
    # write each image's per-assembly tail once, in metadata order, from the
    # collected union (this is what makes the pool byte-identical to serial)
    total = {'files': 0, 'lifted': 0, 'failed': 0, 'fallbacks': 0,
             'emit_failed': 0, 'lifter': True, 'errors': []}
    for img in images:
        a = agg[img.name]
        try:
            a['files'] += em.write_assembly_tail(img, a['sub'], a['raw'])
        except Exception as ex:
            a['error'] = a['error'] or '%s: %s' % (type(ex).__name__, ex)
        if a['error']:
            total['errors'].append('%s: %s' % (img.name, a['error']))
        total['files'] += a['files']
        total['lifted'] += a['lifted']
        total['failed'] += a['failed']
        total['fallbacks'] += a['fallbacks']
        total['emit_failed'] += a['emit_failed']
        total['lifter'] = total['lifter'] and a['lifter']
        if not quiet:
            print('  %-52s %5d types  (%d bodies, %d failed)' % (
                img.name, a['files'], total['lifted'], total['failed']),
                flush=True)
    if not quiet:
        print('workers: %d processes | wall %d ms' % (workers, time_ms() - t0),
              flush=True)
    return total


def _split_balanced(items, batch):
    """Split `items` into contiguous chunks of ~`batch` (the last may be
    small). Contiguous, so a chunk's file writes keep planning order."""
    batch = max(1, batch)
    return [items[i:i + batch] for i in range(0, len(items), batch)]


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(
        prog='il2csharp',
        description='IL2CPP -> C# recovery with real (lifted) method bodies.')
    ap.add_argument('target', nargs='?', help='game dir, metadata file, or binary file')
    ap.add_argument('--metadata', help='explicit global-metadata.dat path (renamed files supported)')
    ap.add_argument('--binary', help='explicit GameAssembly.dll / libil2cpp.so path')
    ap.add_argument('-o', '--out', default='il2csharp_out', help='output directory')
    ap.add_argument('--only', default=None, help='comma-separated assembly name filters (substring match)')
    ap.add_argument('--types', default=None, help='case-insensitive full type-name substring; nested matches retain the owner file')
    ap.add_argument('--strict', action='store_true', help='return nonzero on body-lifting fallback or missing backend')
    ap.add_argument('--decls-only', action='store_true', help='skip method body lifting')
    ap.add_argument('--asm', action='store_true', help='include native asm comments in bodies')
    ap.add_argument('--publicize', action='store_true',
                    help='emit every declaration public (recompilation aid: bodies read '
                         'private/internal members the way native code does)')
    ap.add_argument('--raw-addr', action='store_true',
                    help='route every `(byte*)E` raw-access base through a declared '
                         '`__addr(E)` helper (recompilation aid: managed bases throw '
                         'instead of failing CS0030)')
    ap.add_argument('--max-methods', type=int, default=None, help='cap lifted bodies (debug)')
    ap.add_argument('--workers', type=int, default=1,
                    help='emit assemblies in N worker processes (0 = auto: half the cores, '
                         'max 8). The tree is byte-identical to --workers 1; only the schedule '
                         'changes')
    ap.add_argument('--probe', action='store_true', help='diagnostics only')
    ap.add_argument('--emit-h', action='store_true',
                    help='also emit an il2cpp.h-style C header (Il2CppDumper format)')
    ap.add_argument('-v', '--verbose', action='store_true')
    ap.add_argument('-q', '--quiet', action='store_true',
                    help='suppress progress; still prints errors and --json')
    ap.add_argument('--json', action='store_true',
                    help='print a one-line JSON summary on stdout')
    ap.add_argument('--manifest', metavar='FILE',
                    help='write the same JSON summary to FILE')
    ap.add_argument('--fixture', metavar='ID',
                    help='resolve the target from fixtures/registry.json '
                         '(paths never live in the repo) instead of a '
                         'literal target path')
    ap.add_argument('--label', metavar='NAME',
                    help='tag this build under out/<fixture>/<label> and '
                         'record it in the tree MANIFEST.json')
    ap.add_argument('--bodies', nargs='?', const='bodies.json', metavar='FILE',
                    help='write address-keyed C# bodies for Sunshine --rival '
                         '(default: <out>/bodies.json)')
    args = ap.parse_args(argv[1:])

    if args.max_methods is not None and args.max_methods < 0:
        ap.error('--max-methods must be nonnegative')
    if args.workers < 0:
        ap.error('--workers must be >= 0 (0 picks half the cores, max 8)')
    fixture_id = args.fixture
    if args.fixture:
        # --fixture resolves the game through the local registry; an explicit
        # --target/--metadata/--binary still wins, so existing commands and
        # tests keep working unchanged.
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        '..', 'tools'))
        try:
            import fixtures as _fixtures
            fx = _fixtures.resolve(args.fixture)
        except Exception as ex:
            print('error: fixture %r: %s' % (args.fixture, ex))
            return 1
        if args.target is None and not (args.metadata and args.binary):
            args.target = str(fx.game_dir)
            args.metadata = args.metadata or str(fx.metadata)
            args.binary = args.binary or str(fx.binary)
        fixture_id = fx.id
    if not args.target and not (args.metadata and args.binary):
        ap.error('provide a target or both --metadata and --binary')
    try:
        gmd, bp = find_game_files(args.target, metadata=args.metadata, binary=args.binary)
    except (OSError, ValueError) as ex:
        print('error:', ex)
        return 1
    if not gmd:
        print('error: could not locate global-metadata.dat under', args.target)
        return 1
    def say(*parts):
        if not args.quiet:
            print(*parts)
    say('metadata:', gmd)
    say('binary  :', bp)
    try:
        meta = Metadata(gmd)
    except (OSError, ValueError, struct.error) as ex:
        print('error: could not read metadata:', ex)
        return 1
    say('metadata v%d | %d types | %d methods | %d images | %d string literals' % (
        meta.version, len(meta.typedefs), len(meta.methods), len(meta.images),
        len(meta.string_literals)))
    if not bp:
        print('error: no binary found (need GameAssembly.dll / libil2cpp.so)')
        return 1
    try:
        bin_ = load_binary(bp)
    except (OSError, ValueError, struct.error) as ex:
        print('error: could not read binary:', ex)
        return 1
    if bin_ is None:
        print('error: unsupported binary format')
        return 1
    say('binary loaded: %d sections, %d exports%s' % (len(bin_.sections), len(bin_.exports), (' | relocs: %d' % bin_.reloc_applied) if getattr(bin_, 'reloc_applied', 0) else ''))
    il = Il2Cpp(meta, bin_)
    il.verbose = args.verbose
    t0 = time_ms()
    try:
        il.assign_images()
        try:
            il.find_registrations()
        except RuntimeError:
            # The Android loader assumes a different registration struct
            # shape. Probed on the x64 PE it does not fail: it lands on a
            # code_reg_va 0x10 off the classic answer with the same module
            # count and the same resolved method coverage, so trying it on
            # a PE trades a clean error for a silently wrong registration.
            if not isinstance(bin_, ELF):
                raise
            il.find_registrations_android()
        il.load_function_bounds()
        il.resolve_method_addrs()
    except (OSError, ValueError, IndexError, KeyError, struct.error,
            RuntimeError) as ex:
        print('error: could not read code/metadata registrations:', ex)
        return 1
    getattr(il, '_mod_ptr_cache', {}).clear()  # free raw pointer arrays
    n_addr = sum(1 for m in meta.methods if m.addr)
    say('registrations ok | %d/%d methods have native code | %d ms' % (
        n_addr, len(meta.methods), time_ms() - t0))

    if args.probe:
        for name, mod in sorted(il.modules.items()):
            print('  %-50s methods=%d' % (name, mod.method_pointer_count))
        return 0

    if not args.decls_only:
        if is_arm64_binary(bin_) and not HAVE_CAPSTONE:
            say('warning: Capstone not installed; ARM64 bodies disabled (pip install capstone)')
        elif not is_arm64_binary(bin_) and not HAVE_ICED:
            say('warning: iced-x86 not installed; x64 bodies disabled (pip install iced-x86)')

    only = [t.strip().lower() for t in args.only.split(',')] if args.only else None
    images = [img for img in meta.images
              if not only or any(t in img.name.lower() for t in only)]
    if only and not images:
        print('error: --only matched no assembly:', args.only)
        return 1

    if args.label and args.out == 'il2csharp_out':
        # A label with no explicit -o lands in the fixture's out/ namespace,
        # so a build is self-describing and git-ignored as a whole.
        if not fixture_id:
            print('error: --label needs --fixture')
            return 1
        args.out = os.path.join('out', fixture_id, args.label)
    os.makedirs(args.out, exist_ok=True)
    if args.emit_h:
        t0 = time_ms()
        hpath = os.path.join(args.out, 'il2cpp.h')
        n_types = HeaderEmitter(il, hpath).write()
        say('il2cpp.h: %d types in %d ms -> %s' % (n_types, time_ms() - t0, hpath))
    workers, _note = _worker_count(args, images)
    # the parent keeps an Emitter for the two whole-tree files; with a pool
    # running it needs no Lifter of its own
    em = Emitter(il, args.out, asm_comments=args.asm,
                 with_bodies=not args.decls_only and workers == 1,
                 max_methods=args.max_methods, verbose=args.verbose,
                 type_filter=args.types, publicize=args.publicize,
                 raw_addr=args.raw_addr)
    t0 = time_ms()
    stats = _emit_assemblies(images, em, args, gmd, bp)
    em.write_script_json(os.path.join(args.out, 'script.json'))
    em.write_string_literals(os.path.join(args.out, 'stringliteral.json'))
    for err in stats['errors']:
        print('error:', err)
    bodies_path = None
    if args.bodies:
        bodies_path = args.bodies if os.path.isabs(args.bodies) else os.path.join(args.out, args.bodies)
        parent = os.path.dirname(os.path.abspath(bodies_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        em.write_bodies(bodies_path)
        say('bodies: %d -> %s' % (len(em.bodies), bodies_path))
    elapsed = time_ms() - t0
    summary = {
        'out': os.path.abspath(args.out),
        'files': stats['files'],
        'lifted': stats['lifted'],
        'failed': stats['failed'],
        'fallbacks': stats['fallbacks'],
        'emit_failed': stats['emit_failed'],
        'ms': elapsed,
        'bodies': os.path.abspath(bodies_path) if bodies_path else None,
    }
    if args.manifest:
        import json
        os.makedirs(os.path.dirname(os.path.abspath(args.manifest)) or '.', exist_ok=True)
        with open(args.manifest, 'w', encoding='utf-8') as fh:
            json.dump(summary, fh, indent=1)
        say('manifest:', os.path.abspath(args.manifest))
    say('done: %d type files in %d ms | bodies lifted: %d, failed: %d | '
        'structured fallbacks: %d, type emit failures: %d' % (
        stats['files'], elapsed, stats['lifted'], stats['failed'],
        stats['fallbacks'], stats['emit_failed']))
    _write_manifest(args, summary, gmd, bp)
    if args.json:
        import json
        print(json.dumps(summary, separators=(',', ':')))
    failed = bool(stats['failed'] or stats['emit_failed'] or stats['errors'])
    if args.strict and not args.decls_only:
        failed = failed or bool(stats['fallbacks']) or not stats['lifter']
    return 1 if failed else 0


def _write_manifest(args, summary, gmd, bp):
    """Record what produced this tree, beside the tree.

    The historical promotion records kept this in hand-written JSON;
    making it a build by-product means nobody can forget it. Never fatal:
    a manifest failure must not lose a completed build.
    """
    import hashlib
    import json
    import subprocess
    try:
        def sha(path):
            h = hashlib.sha256()
            with open(path, 'rb') as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b''):
                    h.update(chunk)
            return h.hexdigest()
        try:
            commit = subprocess.run(['git', 'rev-parse', 'HEAD'],
                                    cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                    capture_output=True, text=True,
                                    timeout=20).stdout.strip()
        except Exception:
            commit = None
        # cli.py lives in il2cpp/, so the repo root is one level up
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sources = {}
        for name in ('il2csharp.py',):
            p = os.path.join(root, name)
            if os.path.isfile(p):
                sources[name] = sha(p)
        pkg = os.path.join(root, 'il2cpp')
        for dirpath, dirnames, filenames in os.walk(pkg):
            dirnames[:] = [x for x in dirnames if x != '__pycache__']
            for name in sorted(filenames):
                if name.endswith('.py'):
                    p = os.path.join(dirpath, name)
                    sources[os.path.relpath(p, root).replace(os.sep, '/')] = sha(p)
        payload = {
            'kind': 'build manifest',
            'fixture': getattr(args, 'fixture', None),
            'label': getattr(args, 'label', None),
            'out': summary['out'],
            'source_commit': commit or None,
            'source_fingerprints': sources,
            'flags': {
                'strict': bool(args.strict),
                'decls_only': bool(args.decls_only),
                'publicize': bool(args.publicize),
                'raw_addr': bool(args.raw_addr),
                'only': args.only,
                'types': args.types,
                'workers': args.workers,
                'max_methods': args.max_methods,
            },
            'metadata': os.path.abspath(gmd),
            'binary': os.path.abspath(bp),
            'metadata_sha256': sha(gmd),
            'binary_sha256': sha(bp),
            **{k: summary[k] for k in ('files', 'lifted', 'failed', 'fallbacks',
                                       'emit_failed', 'ms', 'bodies')},
        }
        path = os.path.join(summary['out'], 'MANIFEST.json')
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(payload, fh, indent=1)
        if not args.quiet:
            print('manifest:', path)
    except Exception as ex:
        print('warning: could not write MANIFEST.json:', ex)


def time_ms():
    import time
    return int(time.time() * 1000)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
