"""Promote one built label to be the fixture's baseline tree.

Encodes the promotion ritual the historical docs describe as prose: compare
per-file sha256 between two labels, prove no stale files, then move. Promotion
is a human decision, so the move only happens with an explicit ``--move``;
without it the tool only reports.

Usage::

    python tools/promote.py --fixture limbus --candidate r12 --baseline r11
    python tools/promote.py --fixture limbus --candidate r12 --baseline r11 --move

Both labels live under ``out/<fixture>/`` and must carry a MANIFEST.json
(written by the build; see ``il2csharp.py --label``).
"""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'tools'))

from fixtures import FixtureError, out_root  # noqa: E402

MANIFEST = 'MANIFEST.json'


def manifest_of(label_dir):
    path = Path(label_dir) / MANIFEST
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


def hash_tree(root):
    """{relpath: sha256} for every file under root, MANIFEST excluded."""
    out = {}
    for path in sorted(Path(root).rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel == MANIFEST:
            continue
        h = hashlib.sha256()
        with open(path, 'rb') as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b''):
                h.update(chunk)
        out[rel] = h.hexdigest()
    return out


def aggregate(hashes):
    """One digest over the sorted (path, sha256) pairs."""
    h = hashlib.sha256()
    for rel in sorted(hashes):
        h.update(rel.encode('utf-8'))
        h.update(b'\0')
        h.update(hashes[rel].encode('ascii'))
        h.update(b'\0')
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--fixture', required=True)
    ap.add_argument('--candidate', required=True, help='label to promote')
    ap.add_argument('--baseline', required=True, help='label it replaces')
    ap.add_argument('--move', action='store_true',
                    help='actually replace the baseline (default: report only)')
    ap.add_argument('--report', help='write the proof JSON here')
    args = ap.parse_args(argv)

    cand = out_root() / args.fixture / args.candidate
    base = out_root() / args.fixture / args.baseline
    for label, path in (('candidate', cand), ('baseline', base)):
        if not path.is_dir():
            print('error: %s tree missing: %s' % (label, path))
            return 2

    cand_hashes, base_hashes = hash_tree(cand), hash_tree(base)
    added = sorted(set(cand_hashes) - set(base_hashes))
    removed = sorted(set(base_hashes) - set(cand_hashes))
    mismatched = sorted(rel for rel in set(cand_hashes) & set(base_hashes)
                        if cand_hashes[rel] != base_hashes[rel])
    proof = {
        'kind': 'promotion proof',
        'fixture': args.fixture,
        'candidate': args.candidate,
        'baseline': args.baseline,
        'candidate_manifest': manifest_of(cand),
        'baseline_manifest': manifest_of(base),
        'files_candidate': len(cand_hashes),
        'files_baseline': len(base_hashes),
        'added': len(added),
        'removed': len(removed),
        'mismatched': len(mismatched),
        'candidate_aggregate': aggregate(cand_hashes),
        'baseline_aggregate': aggregate(base_hashes),
        'added_paths': added, 'removed_paths': removed,
        'mismatched_paths': mismatched,
    }
    if args.report:
        path = Path(args.report)
        if path.parent:
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')

    print('promotion proof: %s/%s -> %s/%s' % (
        args.fixture, args.candidate, args.fixture, args.baseline))
    print('  files        : %d -> %d' % (len(base_hashes), len(cand_hashes)))
    print('  added        : %d' % len(added))
    print('  removed      : %d' % len(removed))
    print('  mismatched   : %d' % len(mismatched))
    print('  aggregates   : %s -> %s' % (
        proof['baseline_aggregate'][:12], proof['candidate_aggregate'][:12]))
    for label, rels in (('added', added), ('removed', removed),
                        ('mismatched', mismatched)):
        for rel in rels[:10]:
            print('    %s: %s' % (label, rel))

    if not args.move:
        print('  (report only; pass --move to replace the baseline)')
        return 0
    if removed:
        print('error: refusing to promote: the candidate drops %d baseline '
              'files (stale-tree risk). Resolve or delete them first.'
              % len(removed))
        return 1
    backup = out_root() / args.fixture / ('.backup-' + args.baseline)
    if backup.exists():
        shutil.rmtree(backup)
    shutil.move(str(base), str(backup))
    shutil.move(str(cand), str(base))
    print('  moved        : %s -> %s (previous baseline kept at %s)'
          % (cand, base, backup))
    return 0


if __name__ == '__main__':
    sys.exit(main())
