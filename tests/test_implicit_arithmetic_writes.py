"""Unmodelled implicit arithmetic cannot retain old managed register values."""
import pytest
from iced_x86 import Decoder
from il2cpp import Expr
from test_native_values import lifter, execute, INT, OBJECT


@pytest.mark.parametrize('extension', [4, 5, 6, 7], ids=['mul','imul','div','idiv'])
@pytest.mark.parametrize('width', [1, 2, 4, 8])
@pytest.mark.parametrize('memory', [False, True])
@pytest.mark.parametrize('dry', [False, True])
def test_all_implicit_outputs_are_fresh_and_source_is_not_a_destination(extension, width, memory, dry):
    prefix = {1: '', 2: '66', 4: '', 8: '48'}[width]
    opcode = 'f6' if width == 1 else 'f7'
    modrm = (0 if memory else 0xc0) | extension << 3 | 1
    raw = prefix + opcode + f'{modrm:02x}'
    old_a = Expr('oldVector', OBJECT, 'obj')
    old_d = Expr('oldBoolean', INT, 'int')
    source = Expr('operand', INT, 'int')
    lift = lifter({'RAX': old_a, 'RDX': old_d, 'RCX': source})
    lift.dry = dry
    lift.flags = (Expr('oldCompare', INT, 'int'), Expr('0', INT, 'int'))
    execute(lift, raw)
    assert lift.regs['RCX'] is source
    changed = ['RAX'] if width == 1 else ['RAX', 'RDX']
    for name in changed:
        value = lift.regs[name]
        assert value._unk and value.ty is None and value.kind == '?'
        assert value.text not in ('oldVector', 'oldBoolean', 'operand')
    if width == 1:
        assert lift.regs['RDX'] is old_d
    else:
        assert lift.regs['RAX'] is not lift.regs['RDX']
        assert lift.regs['RAX'].text != lift.regs['RDX'].text
    assert lift.flags is None


@pytest.mark.parametrize('raw', ['f7e8', 'f7ea', '48f7e8', '48f7ea'])
def test_operand_aliasing_an_implicit_output_does_not_keep_its_old_value(raw):
    lift = lifter({'RAX': Expr('oldA', OBJECT, 'obj'),
                   'RDX': Expr('oldD', OBJECT, 'obj')})
    execute(lift, raw)
    assert lift.regs['RAX']._unk and lift.regs['RDX']._unk


def test_each_execution_creates_distinct_values():
    lift = lifter({'RAX': Expr('oldA', INT, 'int'), 'RDX': Expr('oldD', INT, 'int')})
    execute(lift, 'f7e9')
    first = {k: v.text for k, v in lift.regs.items()}
    execute(lift, 'f7e9')
    assert lift.regs['RAX'].text != first['RAX']
    assert lift.regs['RDX'].text != first['RDX']


@pytest.mark.parametrize('raw,expected', [('0fafc1', 'left * right'),
                                         ('6bc103', 'right * 3')])
def test_explicit_two_and_three_operand_imul_are_unchanged(raw, expected):
    lift = lifter({'RAX': Expr('left', INT, 'int'),
                   'RCX': Expr('right', INT, 'int'),
                   'RDX': Expr('untouched', INT, 'int')})
    execute(lift, raw)
    assert lift.regs['RAX'].text == expected
    assert lift.regs['RDX'].text == 'untouched'
