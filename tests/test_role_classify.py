"""Image role classification and the build's role filters.

The fixture's 162 images split three ways (measured on limbus v39):

    engine          77 images  10,149 types  67,139 bodies  (22.4%)
    third-party     71 images   7,627 types  54,059 bodies  (18.1%)
    game-original   14 images  33,256 types 178,173 bodies  (59.5%)

Engine and third-party assemblies ship as real managed DLLs (a Unity
install's `Editor/Data/Managed/UnityEngine/*.dll`, or the vendor's
NuGet package), so lifting their bodies from IL2CPP reproduces
information that already exists, worse. They are also where the bulk of
the whole-tree Roslyn error debt lives.

An unknown name lands in `game-original` on purpose: dropping an image
by accident costs more than keeping one extra.
"""
from role_classify import (ROLE_ENGINE, ROLE_GAME, ROLE_THIRD_PARTY,
                           classify, role_of, select)


def test_engine_prefixes():
    assert role_of('UnityEngine.CoreModule.dll') == ROLE_ENGINE
    assert role_of('UnityEngine.dll') == ROLE_ENGINE
    assert role_of('mscorlib.dll') == ROLE_ENGINE
    assert role_of('System.dll') == ROLE_ENGINE
    assert role_of('System.Xml.dll') == ROLE_ENGINE
    assert role_of('netstandard.dll') == ROLE_ENGINE
    assert role_of('Mono.Security.dll') == ROLE_ENGINE
    assert role_of('Unity.InternalAPIEngineBridge.001.dll') == ROLE_ENGINE


def test_third_party_prefixes():
    assert role_of('Newtonsoft.Json.dll') == ROLE_THIRD_PARTY
    assert role_of('UniTask.dll') == ROLE_THIRD_PARTY
    assert role_of('DOTween.dll') == ROLE_THIRD_PARTY
    assert role_of('DOTweenPro.dll') == ROLE_THIRD_PARTY
    assert role_of('spine-csharp.dll') == ROLE_THIRD_PARTY
    assert role_of('FMODUnity.dll') == ROLE_THIRD_PARTY
    assert role_of('Facepunch.Steamworks.Win64.dll') == ROLE_THIRD_PARTY
    assert role_of('Unity.RenderPipelines.Core.Runtime.dll') == ROLE_THIRD_PARTY
    assert role_of('Unity.TextMeshPro.dll') == ROLE_THIRD_PARTY
    assert role_of('Cinemachine.dll') == ROLE_THIRD_PARTY
    assert role_of('Unity.Burst.dll') == ROLE_THIRD_PARTY
    assert role_of('Unity.Mathematics.dll') == ROLE_THIRD_PARTY
    assert role_of('Firebase.App.dll') == ROLE_THIRD_PARTY


def test_game_originals():
    assert role_of('Assembly-CSharp.dll') == ROLE_GAME
    assert role_of('Assembly-CSharp-firstpass.dll') == ROLE_GAME
    assert role_of('ProjectMoon.BaseStructures.dll') == ROLE_GAME
    assert role_of('RpgSystemCore.dll') == ROLE_GAME
    assert role_of('LimbusCompany.AddressableConstants.dll') == ROLE_GAME
    assert role_of('__Generated') == ROLE_GAME


def test_unknown_names_default_to_game():
    """Dropping an image by accident costs more than keeping one extra."""
    assert role_of('SomeUnknownVendor.Runtime.dll') == ROLE_GAME
    assert role_of('') == ROLE_GAME


def test_classify_preserves_order():
    names = ['UnityEngine.CoreModule.dll', 'Assembly-CSharp.dll',
             'Newtonsoft.Json.dll']
    assert classify(names) == [
        ('UnityEngine.CoreModule.dll', ROLE_ENGINE),
        ('Assembly-CSharp.dll', ROLE_GAME),
        ('Newtonsoft.Json.dll', ROLE_THIRD_PARTY),
    ]


def test_select_keep_game_only():
    names = ['Assembly-CSharp.dll', 'UnityEngine.CoreModule.dll',
             'Newtonsoft.Json.dll', 'ProjectMoon.BaseStructures.dll']
    assert select(names, keep=[ROLE_GAME]) == [
        'Assembly-CSharp.dll', 'ProjectMoon.BaseStructures.dll']


def test_select_drop_roles():
    names = ['Assembly-CSharp.dll', 'UnityEngine.CoreModule.dll',
             'Newtonsoft.Json.dll']
    assert select(names, drop=[ROLE_ENGINE]) == [
        'Assembly-CSharp.dll', 'Newtonsoft.Json.dll']
    assert select(names, drop=[ROLE_ENGINE, ROLE_THIRD_PARTY]) == [
        'Assembly-CSharp.dll']


def test_select_name_substring_and_role_together():
    names = ['Assembly-CSharp.dll', 'Assembly-CSharp-firstpass.dll',
             'UnityEngine.CoreModule.dll']
    # keep: only the exact Assembly-CSharp (substring), not the firstpass one
    out = select(names, keep=['assembly-csharp.dll'])
    assert out == ['Assembly-CSharp.dll']


def test_select_empty_keep_means_everything():
    names = ['a.dll', 'b.dll']
    assert select(names) == names
    assert select(names, drop=[]) == names
