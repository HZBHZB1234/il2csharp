"""Authored Win64 copies: value snapshots never replace scalar byte origins."""
import struct
from types import SimpleNamespace as NS

import pytest
from iced_x86 import Decoder

from il2cpp.binary import PE
from il2cpp.expr import Expr
from il2cpp.lifter.materialized import record_materialized_sret as record
from il2cpp.lifter.materialized import recover_materialized_sret as recover

START = 0x180001000
SOURCE, CONSUMER = START + 0x1000, START + 0x2000
VOID, VALUE, OWNER = (0, 1 << 16), (1, 0x11 << 16), (0, 0x12 << 16)


def call(ip, target):
    return b'\xe8' + struct.pack('<i', target - ip - 5)


def setup(copy=None, prefix=None, size=16, consumer_return=VALUE):
    prefix = bytes.fromhex('488d4c2420') if prefix is None else prefix
    # Read the producer's RAX echo, copy to a DIFFERENT home, pass behind
    # the consumer's own hidden return buffer. The token text is not a proof.
    copy = bytes.fromhex('0f10000f294424404531c0488d542440488d8c2480000000') if copy is None else copy
    source_ip = START + len(prefix)
    body = prefix + call(source_ip, SOURCE) + copy
    consumer_ip = START + len(body)
    body += call(consumer_ip, CONSUMER)
    insns = list(Decoder(64, body, ip=START))
    data = bytearray(0x100 + len(body))
    struct.pack_into('<I', data, 0x3c, 0x40)
    data[0x40:0x46] = b'PE\x00\x00\x64\x86'
    data[0x100:] = body
    binary = PE.__new__(PE); binary.is64 = True; binary.d = bytes(data)
    binary.va2off = lambda va: va - START + 0x100 if START <= va < START + len(body) else None
    producer = NS(index=0, addr=SOURCE, declaring=0, return_type=1,
                  generic_container=-1, is_static=True, param_count=0)
    consumer = NS(index=1, addr=CONSUMER, declaring=0,
                  return_type=1 if consumer_return == VALUE else 0,
                  generic_container=-1, is_static=True, param_count=1)
    params = [NS(type=1)]
    meta = NS(methods=[producer, consumer],
              typedefs=[NS(generic_container=-1, declaring=-1),
                        NS(generic_container=-1, declaring=-1)])
    meta.method_params = lambda method: params if method is consumer else []
    il = NS(bin=binary, meta=meta, types=[VOID, VALUE, OWNER],
            addr_candidates={SOURCE: [('method', 0)], CONSUMER: [('method', 1)]},
            _type_enum=lambda ty: (ty[1] >> 16) & 255,
            _closed_type_key=lambda ty: ty,
            _sf_field_size=lambda ty, depth: size if ty == VALUE else 8,
            returns_sret=lambda ty: ty == VALUE)
    lift = NS(il=il, out=NS(block=NS(insns=insns)),
              _cur_ip=source_ip, rsp_delta=-0x100,
              _piece_layout_proven=lambda ty: True,
              _var_types={'t1001': VALUE}, slot_types={'t1001': VALUE},
              regs={'RAX': Expr('&t1001', VALUE, 'ptr')})
    record(lift, insns[len(list(Decoder(64, prefix, ip=START)))], -0xe0, VALUE, 't1001')
    lift._cur_ip = consumer_ip
    return lift, -0xc0, VALUE


def test_complete_copy_to_different_home_is_the_materialized_value():
    lift, address, ty = setup()
    before = (dict(lift.regs), dict(lift.slot_types), dict(lift._var_types),
              tuple(lift.out.block.insns), vars(lift._materialized_sret).copy())
    assert recover(lift, address, ty) == 't1001'
    assert before == (dict(lift.regs), dict(lift.slot_types), dict(lift._var_types),
                      tuple(lift.out.block.insns), vars(lift._materialized_sret).copy())


@pytest.mark.parametrize('size,copy', [
    (16, '0f10000f294424404531c0488d542440488d8c2480000000'),
    (16, '660f1000660f11442440488d542440'),
    (16, 'f30f6f00f30f7f442440488d542440'),
    (16, '660f6f00660f7f442440488d542440'),
    (16, '0f10004889c30f294424404889d8488d542440'),
    (16, '488b104889542440488b40084889442448488d542440'),
    (24, '0f1000488b40100f294424404889442450488d542440'),
    (12, 'f20f10008b4008f20f1144244089442448488d542440'),
])
def test_full_native_copies_preserve_every_source_offset(size, copy):
    lift, address, ty = setup(size=size, copy=bytes.fromhex(copy))
    assert recover(lift, address, ty) == 't1001'


def test_idempotent_self_copy_keeps_value_without_claiming_padding_bytes():
    copy = bytes.fromhex('0f10000f29442420488d542420')
    lift, _, ty = setup(copy=copy)
    assert recover(lift, -0xe0, ty) == 't1001'
    assert not hasattr(lift.regs['RAX'], '_bytes')
    assert not hasattr(lift.regs['RAX'], '_slice')


@pytest.mark.parametrize('copy', [
    '0f100031d24889100f29442440488d542440',        # original temp mutated after save
    '0f100031d24889100f11000f29442440488d542440', # source restored, temp lifetime unproved
    '0f1000488d542440',                         # no store
    'f20f1000f20f11442440488d542440',             # only half copied
    '0f1040080f29442440488d542440',               # wrong source offset
    '0f10000f29442448488d542440',                # wrong destination offset
    '0f10000f29442440488d542448',                # ABI pointer mismatch
    '0f10000f29442440488d4c2440',                # pointer in receiver/sret position
    '0f10000f29442440488d542440c644244000',        # partial overwrite
    '0f10000f29442440488d542440488903',            # unknown-address write
    '0f10000f29442440488d542440f048830300',        # RMW alias
    '0f10000f29442440488d542440e800000000',        # intervening call
    '0f10000f29442440488d5424407400',              # another CFG edge
    '0f10000f29442440488d542440c3',                # early return
    '0f1000480f44c30f29442440488d542440',           # unmodelled CMOV
    '0f10000fc6c0000f29442440488d542440',           # shuffled vector
    '0f10000f57c00f29442440488d542440',             # clobbered vector
    '0f1000660fefc00f29442440488d542440',           # PXOR
    '0f1000660f57c00f29442440488d542440',           # XORPD
    '0f1000f30f10c10f29442440488d542440',           # scalar reg-reg merge
    '0f10004889442440488d542440',                  # pointer is not its bytes
    '488b1089d24889542440488b40084889442448488d542440', # high32 lost
    '0f10000f11442428f30f6f4424200f29442440488d542440', # overlapping, shifted source
    '0f1000670f29442440488d542440',                 # 32-bit address wraps
    '0f1000670f10000f29442440488d542440',           # 32-bit source pointer
    '0f10000f29442440488d5424400f20c0',             # control/debug register
    '0f10000f29442440488d5424400f22c0',             # control/debug register
    '0f10000f29442440488d5424400f21c0',             # control/debug register
    '0f10000f29442440488d5424400f23c0',             # control/debug register
    '0f1000640f29442440488d542440',                 # segmented store
    '0f10000f290403488d542440',                    # indexed destination
    '0f10000f29442440488d542440488d1403',           # unknown/indexed LEA destroys ptr
    '0f10000f294424404889e2488d5424404889dc',        # unknown RSP, pointer still? no use
])
def test_unproved_or_corrupted_copy_declines(copy):
    lift, address, ty = setup(copy=bytes.fromhex(copy))
    assert recover(lift, address, ty) is None


@pytest.mark.parametrize('shape', [
    'scope', 'dry-real', 'block-reuse', 'method-reuse', 'type', 'byref',
    'ip', 'before-source', 'source-candidate', 'source-shared', 'source-generic',
    'source-address', 'source-index', 'source-owner', 'source-return',
    'consumer-candidate', 'consumer-shared', 'consumer-generic', 'consumer-address',
    'consumer-owner', 'consumer-param', 'consumer-byref', 'consumer-position',
    'consumer-stack-arg', 'binary', 'binary-truncated', 'binary-offset',
    'seed-wrong-home', 'seed-register-copy', 'seed-partial', 'seed-index',
    'seed-rep', 'seed-segment', 'seed-address32', 'rsp-write', 'rcx-write', 'missing-proof',
    'abi-pe32', 'abi-arm64', 'abi-header', 'native-window-bound',
    'consumer-return-negative', 'consumer-return-bounds', 'consumer-param-count', 'no-disassembler',
])
def test_context_and_native_evidence_are_required(shape, monkeypatch):
    lift, address, ty = setup()
    il = lift.il; block = lift.out.block
    if shape in ('scope', 'dry-real', 'block-reuse', 'method-reuse'):
        lift.out = NS(block=block)
    elif shape == 'no-disassembler':
        from il2cpp.lifter import materialized
        monkeypatch.setattr(materialized, 'HAVE_ICED', False)
    elif shape == 'type': ty = OWNER
    elif shape == 'byref': ty = (VALUE[0], VALUE[1] | (1 << 29))
    elif shape == 'ip': lift._cur_ip += 1
    elif shape == 'before-source': lift._cur_ip = block.insns[0].ip
    elif shape == 'source-candidate': il.addr_candidates.pop(SOURCE)
    elif shape == 'source-shared': il.addr_candidates[SOURCE].append(('method', 1))
    elif shape == 'source-generic': il.meta.methods[0].generic_container = 0
    elif shape == 'source-address': il.meta.methods[0].addr += 1
    elif shape == 'source-index': il.meta.methods[0].index = 9
    elif shape == 'source-owner': il.meta.typedefs[0].generic_container = 0
    elif shape == 'source-return': il.meta.methods[0].return_type = 0
    elif shape == 'consumer-return-negative': il.meta.methods[1].return_type = -1
    elif shape == 'consumer-return-bounds': il.meta.methods[1].return_type = len(il.types)
    elif shape == 'consumer-param-count': il.meta.methods[1].param_count = 2
    elif shape == 'consumer-candidate': il.addr_candidates.pop(CONSUMER)
    elif shape == 'consumer-shared': il.addr_candidates[CONSUMER].append(('method', 0))
    elif shape == 'consumer-generic': il.meta.methods[1].generic_container = 0
    elif shape == 'consumer-address': il.meta.methods[1].addr += 1
    elif shape == 'consumer-owner': il.meta.methods[1].declaring = 8
    elif shape == 'consumer-param': il.meta.method_params = lambda method: [NS(type=0)]
    elif shape == 'consumer-byref':
        il.types.append((VALUE[0], VALUE[1] | (1 << 29)))
        il.meta.method_params = lambda method: [NS(type=3)]
    elif shape == 'consumer-position': il.meta.methods[1].is_static = False
    elif shape == 'consumer-stack-arg': il.meta.method_params = lambda method: [NS(type=0)] * 4 + [NS(type=1)]
    elif shape == 'binary':
        data = bytearray(il.bin.d); data[-1] ^= 1; il.bin.d = bytes(data)
    elif shape == 'binary-truncated': il.bin.d = il.bin.d[:-1]
    elif shape == 'binary-offset': il.bin.va2off = lambda va: -1
    elif shape.startswith('seed-') or shape in ('rsp-write', 'rcx-write'):
        prefixes = {'seed-wrong-home': '488d4c2428', 'seed-register-copy': '4889c1',
                    'seed-partial': '8d4c2420', 'seed-index': '488d4c0320',
                    'seed-address32': '67488d4c2420', 'seed-rep': 'f3488d4c2420', 'seed-segment': '64488d4c2420',
                    'rsp-write': '488d4c24204883ec08', 'rcx-write': '488d4c24204889d1'}
        lift, address, ty = setup(prefix=bytes.fromhex(prefixes[shape]))
    elif shape == 'missing-proof': del lift._materialized_sret
    elif shape == 'abi-pe32': il.bin.is64 = False
    elif shape == 'abi-arm64':
        data = bytearray(il.bin.d); data[0x44:0x46] = b'\x64\xaa'; il.bin.d = bytes(data)
    elif shape == 'abi-header': il.bin.d = b'bad'
    elif shape == 'native-window-bound': lift, address, ty = setup(copy=b'\x90' * 97)
    assert recover(lift, address, ty) is None


@pytest.mark.parametrize('shape', ['layout', 'small', 'large', 'unknown-size', 'source-return',
                                   'open', 'byref', 'text', 'var-type', 'slot-type', 'scope'])
def test_producer_declines_without_touching_exprs_or_field_tiles(shape):
    lift, _, ty = setup()
    del lift._materialized_sret
    if shape == 'layout': lift._piece_layout_proven = lambda ty: False
    elif shape == 'small': lift.il._sf_field_size = lambda ty, depth: 8
    elif shape == 'large': lift.il._sf_field_size = lambda ty, depth: 65
    elif shape == 'unknown-size': lift.il._sf_field_size = lambda ty, depth: None
    elif shape == 'source-return': lift.il.meta.methods[0].return_type = 0
    elif shape == 'open': lift.il._closed_type_key = lambda ty: None
    elif shape == 'byref': ty = (ty[0], ty[1] | (1 << 29))
    elif shape == 'var-type': lift._var_types.clear()
    elif shape == 'slot-type': lift.slot_types.clear()
    elif shape == 'scope': lift.out = []
    text = 'owner.field' if shape == 'text' else 't1001'
    record(lift, setup()[0].out.block.insns[1], -0xe0, ty, text)
    assert not hasattr(lift, '_materialized_sret')


@pytest.mark.parametrize('opcode', ['0f20', '0f21', '0f22', '0f23'])
def test_control_debug_registers_are_not_copy_instructions(opcode):
    from il2cpp.lifter.materialized import _copy
    # Every decoded control/debug-register MOV must decline, including the
    # extended-register encodings; a register width is not a class proof.
    from iced_x86 import Mnemonic, OpKind
    count = 0
    for prefix in ('', '48', '49', '4c', '4d'):
        for modrm in range(0xc0, 0x100):
            ins = next(iter(Decoder(64, bytes.fromhex(prefix + opcode) + bytes([modrm]))))
            if (ins.mnemonic == Mnemonic.MOV and ins.op_count == 2
                    and ins.op0_kind == ins.op1_kind == OpKind.REGISTER):
                assert not _copy(ins, {}, {})
                count += 1
    assert count > 0


def test_noncanonical_producer_does_not_walk_an_unneeded_layout():
    lift, _, ty = setup()
    del lift._materialized_sret
    lift.il.addr_candidates[SOURCE].append(('method', 1))
    def unnecessary(*args):
        raise AssertionError('layout walk before cheap canonical rejection')
    lift._piece_layout_proven = unnecessary
    record(lift, lift.out.block.insns[1], -0xe0, ty, 't1001')
    assert not hasattr(lift, '_materialized_sret')
