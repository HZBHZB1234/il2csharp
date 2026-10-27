"""Image role classification: engine / third-party / game-original.

The build's image set is 162 assemblies on the limbus v39 fixture, and
only a small minority is the game's own code:

    engine          77 images  10,149 types  67,139 bodies  (22.4%)
    third-party     70 images   7,603 types  54,057 bodies  (18.1%)
    game-original   15 images  33,280 types 178,175 bodies  (59.5%)

Decompiling the engine and the third-party plugins buys nothing: the
engine's real managed assemblies ship with a Unity install (true names,
true signatures, XML docs), and both buckets are where the bulk of the
whole-tree Roslyn error debt lives -- the game code referencing a real
UnityEngine is the metric that means something (roadmap P5 slice C).

Classification is by image name prefix, which is what the roadmap's
slice A3 specifies. The metadata's `assemblies` / `referencedAssemblies`
tables would give an exact reference graph (and the third parties'
versions), but only the row's nameIndex (`+0x14`, stride 68) is
verified on this fixture -- the candidate start/count fields are not
monotone across the 162 rows, so the graph is not decoded yet and the
prefix table is the honest source of truth. Every unknown name lands in
`game-original` on purpose: a build that drops something by accident is
worse than one that keeps an extra image.
"""

# Engine: Unity's own modules plus the BCL the runtime ships. These are
# available as real managed DLLs (Unity install / NuGet reference packs).
ENGINE_PREFIXES = (
    'UnityEngine',
    'UnityEditor',
    'mscorlib',
    'netstandard',
    'System',
    'Mono.',
    'Microsoft.',
    'Unity.InternalAPIEngineBridge',
)

# Third-party: libraries the game embeds as plugins. Each ships its own
# real managed assembly (NuGet / the vendor's release), so recovering its
# source from IL2CPP is the same wasted effort as the engine's.
THIRD_PARTY_PREFIXES = (
    'Newtonsoft.Json',
    'Facepunch.Steamworks',
    'UniTask',
    'DOTween',
    'spine',
    'ACTk',
    'FMODUnity',
    'Firebase',
    'SocketIOUnity',
    'Unity.ProBuilder',
    'Unity.TextMeshPro',
    'Cinemachine',
    'Unity.RenderPipelines',
    'Unity.Burst',
    'Unity.Collections',
    'Unity.Mathematics',
    'Unity.Timeline',
    'Unity.ResourceManager',
    'Unity.Addressables',
    'Unity.Services',
    'Unity.2D.',
    'Unity.UnifiedRayTracing',
    'Unity.MemoryProfiler',
    'Unity.RenderPipeline',
    'Febucci.TextAnimator',
    'AllIn1SpriteShader',
    'UIEffect',
    'Coffee.SoftMaskForUGUI',
    'LokoSolo.PinchableScrollRect',
    'RubyTextMeshPro',
    'sc.posteffects',
    'material-timeline',
    'ChainMeshStudio',
    'Timeline.Samples',
    'Purchasing.Common',
)

ROLE_ENGINE = 'engine'
ROLE_THIRD_PARTY = 'third-party'
ROLE_GAME = 'game-original'


def role_of(image_name):
    """'engine' | 'third-party' | 'game-original' for one image name."""
    stem = image_name.rsplit('.', 1)[0] if image_name.endswith('.dll') \
        else image_name
    if stem.startswith(ENGINE_PREFIXES):
        return ROLE_ENGINE
    if stem.startswith(THIRD_PARTY_PREFIXES):
        return ROLE_THIRD_PARTY
    return ROLE_GAME


def classify(image_names):
    """[(name, role)] in the given order."""
    return [(n, role_of(n)) for n in image_names]


def select(image_names, keep=(), drop=()):
    """Filter image names by role and/or explicit name substrings.

    `keep` and `drop` are role names ('engine' / 'third-party' /
    'game-original') or case-insensitive name substrings; `keep` runs
    first, then `drop`. An empty `keep` means "everything". Order is
    preserved so the build's heaviest-first scheduling is unaffected.
    """
    out = []
    for n in image_names:
        r = role_of(n)
        low = n.lower()
        if keep:
            hit = r in keep or any(t.lower() in low for t in keep)
            if not hit:
                continue
        if drop:
            hit = r in drop or any(t.lower() in low for t in drop)
            if hit:
                continue
        out.append(n)
    return out


def summarise(image_names, bodies_by_name=None):
    """Per-role image/type/body totals, for docs and the build log."""
    from collections import Counter
    imgs = Counter()
    for n in image_names:
        imgs[role_of(n)] += 1
    rows = []
    for role in (ROLE_ENGINE, ROLE_THIRD_PARTY, ROLE_GAME):
        b = (bodies_by_name or {}).get(role)
        rows.append((role, imgs.get(role, 0), b))
    return rows
