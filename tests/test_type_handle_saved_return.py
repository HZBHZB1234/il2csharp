"""Only an exact full-width preceding-return save may extend the setup."""
import pytest
from test_type_handle_call import setup
from il2cpp.lifter.typehandles import recover_type_handle_call

def recover(state):
    il,call,value,_,_=state
    return recover_type_handle_call(il,call,0,value,block=il._proof_block)

@pytest.mark.parametrize('copy', [bytes.fromhex(x) for x in ['4889c3','4889c5','4889c6','4889c7','4989c4','4989c5','4989c6','4989c7','488bd8','488be8','488bf0','488bf8','4c8be0','4c8be8','4c8bf0','4c8bf8']])
@pytest.mark.parametrize('zero', [b'\x33\xd2',b'\x31\xd2',b'\x40\x33\xd2'])
def test_narrow_call_result_save_does_not_change_rcx(copy,zero):
    state=setup(suffix=zero+copy)
    before=state[2].text,state[2].ty,state[2].kind,state[2]._type_handle
    assert recover(state)=='typeof(int)'
    assert before==(state[2].text,state[2].ty,state[2].kind,state[2]._type_handle)

@pytest.mark.parametrize('copy', [bytes.fromhex(x) for x in ['4889c1','4889c4','4889c2','4989c0','4989c1','4989c2','4989c3','89c3','6689c3','88c3','4889cb','4889d3','488b18','48891c24','488d18','4887c3','4883c301','644889c3','904889c3','4889c390','4889c34889c5']])
def test_any_other_effect_or_unproved_save_declines(copy):
    assert recover(setup(suffix=b'\x33\xd2'+copy)) is None

@pytest.mark.parametrize('suffix',[bytes.fromhex(x) for x in ['4889c733d2','4889c7','33c94889c7','4833d24889c7','eb004889c7']])
def test_instruction_order_and_zero_definition_are_exact(suffix):
    assert recover(setup(suffix=suffix)) is None

@pytest.mark.parametrize('shape',['missing','call-only','skip-load','other-call'])
def test_save_does_not_remove_executed_cfg_requirement(shape):
    state=setup(suffix=bytes.fromhex('33d24889c7'));il,call,value,_,_=state
    block=il._proof_block
    if shape=='missing':block=None
    elif shape=='call-only':block=type(block)(insns=[call])
    elif shape=='skip-load':block=type(block)(insns=block.insns[1:])
    else:block=type(block)(insns=block.insns[:-1])
    assert recover_type_handle_call(il,call,0,value,block=block) is None
