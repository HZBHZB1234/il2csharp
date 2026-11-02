"""The source-vs-tree quality report: matching, normalization and the
conservative exclusions (async state machines, unavailable bodies)."""
from tools.source_compare import (census, compare, index_cs, index_tree,
                                  _normalize_type, _body_has_code)


SOURCE = """
namespace N
{
    public class C
    {
        private int f;

        public int M(int a)
        {
            return Helper(a) + G();
        }

        public bool P
        {
            get { return f == 1; }
        }

        public async System.Threading.Tasks.Task A()
        {
            await Ready();
        }
    }
}
"""

TREE = """
namespace N
{
    public partial class C
    {
        private int f;

        public int M(int v0)
        {
            return Helper(v0) + G();
        }

        public bool P
        {
            get { return f == 1; }
        }

        public async System.Threading.Tasks.Task A()
        {
            await Ready();
        }

        public void Stub()
        {
            throw new global::System.NotImplementedException("Method body was not recovered.");
        }
    }
}
"""


def _trees(tmp_path):
    src = tmp_path / 'src'
    src.mkdir()
    (src / 'C.cs').write_text(SOURCE, encoding='utf-8')
    out = tmp_path / 'out'
    (out / 'Asm').mkdir(parents=True)
    (out / 'Asm' / 'C.cs').write_text(TREE, encoding='utf-8')
    return src, out


def test_type_names_normalize_metadata_arity_and_nesting():
    assert _normalize_type('N.Outer/Inner') == 'N.Outer.Inner'
    assert _normalize_type('System.Collections.Generic.List`1') == \
        'System.Collections.Generic.List'


def test_test_project_directories_are_skipped(tmp_path):
    src = tmp_path / 'src'
    (src / 'NetCoreTests').mkdir(parents=True)
    (src / 'NetCoreTests' / 'T.cs').write_text(
        'class T { void M() { A(); } }', encoding='utf-8')
    (src / 'Runtime').mkdir()
    (src / 'Runtime' / 'R.cs').write_text(
        'class R { void M() { A(); } }', encoding='utf-8')
    idx = index_cs(str(src))
    assert 'R' in idx and 'T' not in idx


def test_nested_type_path_is_not_prefixed_twice(tmp_path):
    src = tmp_path / 'src'
    src.mkdir()
    (src / 'N.cs').write_text(
        'namespace N { class Outer { class Inner { void M() { A(); } } } }',
        encoding='utf-8')
    idx = index_cs(str(src))
    assert ('M', 0) in idx['N.Outer.Inner']
    assert 'N.N.Outer.Inner' not in idx


def test_comments_are_not_calls_and_comment_only_bodies_are_empty(tmp_path):
    src = tmp_path / 'src'
    src.mkdir()
    (src / 'C.cs').write_text(
        'class C {\n'
        '  void M() {\n'
        '    // Fake(); still a comment\n'
        '    Real();\n'
        '    /* Other(); */\n'
        '  }\n'
        '  void OnlyComments() { // Gone();\n'
        '  }\n'
        '}\n', encoding='utf-8')
    idx = index_cs(str(src))
    m = idx['C'][('M', 0)][0]
    assert 'Fake' not in m.body and 'Other' not in m.body
    assert 'Real' in m.body
    only = idx['C'][('OnlyComments', 0)][0]
    assert not _body_has_code(only.body)


def test_conditional_and_lambda_methods_are_transformed(tmp_path):
    src = tmp_path / 'src'
    src.mkdir()
    (src / 'C.cs').write_text(
        'using System.Diagnostics;\n'
        'class C {\n'
        '  [Conditional("X")] void Hidden() { A(); }\n'
        '  void Closure() { System.Action a = () => A(); a(); }\n'
        '  void Plain() { A(); }\n'
        '}\n', encoding='utf-8')
    idx = index_cs(str(src))
    assert idx['C'][('Hidden', 0)][0].transformed
    assert idx['C'][('Closure', 0)][0].transformed
    assert not idx['C'][('Plain', 0)][0].transformed


def test_inlined_state_machine_output_is_not_scored(tmp_path):
    src = tmp_path / 'src'
    src.mkdir()
    (src / 'C.cs').write_text(
        'class C { int M() { return A(); } }', encoding='utf-8')
    out = tmp_path / 'out'
    (out / 'Asm').mkdir(parents=True)
    (out / 'Asm' / 'C.cs').write_text(
        'class C { int M() { '
        'object b = AsyncUniTaskMethodBuilder<int>.Start<C.<M>d__0>; '
        'return 0; } }', encoding='utf-8')
    rows, unmatched, _samples = compare(index_cs(str(src)),
                              index_tree(str(out), ['Asm']))
    assert not rows
    assert unmatched['inlined'] == 1

    (out / 'Asm' / 'C.cs').write_text(
        'class C { int M() { '
        'object b = new C._M_d__0(); '
        'return 0; } }', encoding='utf-8')
    rows, unmatched, _samples = compare(index_cs(str(src)),
                              index_tree(str(out), ['Asm']))
    assert not rows
    assert unmatched['inlined'] == 1


def test_matching_reports_full_recall_and_skips_transformed(tmp_path):
    src, out = _trees(tmp_path)
    src_idx = index_cs(str(src))
    tree_idx = index_tree(str(out), ['Asm'])
    rows, unmatched, _samples = compare(src_idx, tree_idx)
    by_name = {(r['type'], r['method']): r for r in rows}
    assert ('N.C', 'M') in by_name
    assert by_name[('N.C', 'M')]['call_recall'] == 1.0
    assert ('N.C', 'get_P') in by_name
    assert unmatched['transformed'] == 1          # the async method
    assert unmatched['stub'] == 0                 # Stub has no source twin
    # the async twin is not scored, and a source-less stub is not invented
    assert all(r['method'] != 'A' for r in rows)


def test_census_counts_decompiler_tells(tmp_path):
    _src, out = _trees(tmp_path)
    files, tells = census(str(out), ['Asm'])
    assert files == 1
    assert tells.get('sub_call', 0) == 0
    assert 'byte_ptr' not in tells
