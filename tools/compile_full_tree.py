"""Whole-tree compile of a full limbus tree against the editor closure.

Excludes exactly the images whose types the reference closure also provides
(the editor's engine modules + BCL). Packages the editor does NOT ship
(UnityEngine.UI, UnityEngine.Purchasing.*, Unity.*) must stay as sources.
"""
import glob
import json
import os
import sys

REPO = r'E:\desktop\work\LimbusDecompile\il2csharp'
TREE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'out/limbus/full0')
REPORT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    REPO, 'validation_reports/limbus/full0.whole.compile.json')

sys.path.insert(0, os.path.join(REPO, 'tools'))
import compile_corpus  # noqa: E402

_refs = []
for _pat in ('Editor/Data/Managed/UnityEngine/*.dll',
             'Editor/Data/NetStandard/**/*.dll'):
    _refs.extend(glob.glob(os.path.join(r'D:\unity_editor_6000', _pat), recursive=True))
EXCLUDE = tuple(sorted({os.path.splitext(os.path.basename(r))[0] for r in _refs}))

dirs = [d for d in sorted(os.listdir(TREE)) if d in EXCLUDE
        and os.path.isdir(os.path.join(TREE, d))]
print('images excluded from sources:', len(dirs))

rc = compile_corpus.compile_tree(
    TREE, REPORT, refs_dirs=(), unity_roots=[r'D:\unity_editor_6000'],
    managed_dirs=(), exclude=(), exclude_images=False, dotnet_refs=False,
    timeout=3600, exclude_dirs=tuple(dirs))
summary = json.load(open(REPORT, encoding='utf-8'))
print(json.dumps({k: summary[k] for k in
                  ('source_files', 'closure_refs', 'files_with_errors',
                   'errors', 'errors_by_code')}, indent=2))
sys.exit(0 if rc in (0, 1) else 2)
