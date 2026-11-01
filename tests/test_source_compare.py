"""The source-vs-tree quality report: matching, normalization and the
conservative exclusions (async state machines, unavailable bodies)."""
from tools.source_compare import (census, compare, index_cs, index_tree,
                                  _normalize_type)


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


def test_matching_reports_full_recall_and_skips_transformed(tmp_path):
    src, out = _trees(tmp_path)
    src_idx = index_cs(str(src))
    tree_idx = index_tree(str(out), ['Asm'])
    rows, unmatched = compare(src_idx, tree_idx)
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
