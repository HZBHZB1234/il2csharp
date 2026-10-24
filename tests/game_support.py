"""Small, version-neutral lookups shared by game tests.

Tests keep real method identities (type and name) rather than raw MethodDef
rows wherever the fixture allows it.  A pinned build still makes the resulting
body assertions exact, but a moved MethodDef row does not silently point the
test at an unrelated method.
"""
def full_type_name(td):
    return ((td.namespace + '.') if td.namespace else '') + td.name


def find_types(il, name):
    if '.' in name:
        namespace, short = name.rsplit('.', 1)
        return [i for i, td in enumerate(il.meta.typedefs)
                if td.namespace == namespace and td.name == short]
    return [i for i, td in enumerate(il.meta.typedefs) if td.name == name]


def find_type(il, name):
    hits = find_types(il, name)
    assert len(hits) == 1, 'type %r matched %d rows: %s' % (
        name, len(hits), [full_type_name(il.meta.typedefs[i]) for i in hits[:8]])
    return il.meta.typedefs[hits[0]]


def method_rows(il, td):
    return range(td.method_start, td.method_start + td.method_count)


def find_method(il, type_name, method_name, params=None):
    td = find_type(il, type_name)
    hits = []
    for mi in method_rows(il, td):
        m = il.meta.methods[mi]
        if m.name == method_name and (params is None or m.param_count == params):
            hits.append(mi)
    assert len(hits) == 1, '%s.%s params=%r matched %d rows: %s' % (
        type_name, method_name, params, len(hits), hits[:8])
    mi = hits[0]
    return mi, il.meta.methods[mi], td


def lift(il, dec, mi):
    m = il.meta.methods[mi]
    return list(dec.lift_method(m, il.meta.typedefs[m.declaring]))


def lift_text(il, dec, mi):
    return '\n'.join(lift(il, dec, mi))
