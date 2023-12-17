from mpack.option import NONETYPE, NONE, Option
import pytest


def test_single_none():
    NewNone = NONETYPE()
    assert NewNone is NONE, "Id Comparison for NONE object differs."
    assert type(NONE) == NONETYPE, "NoneType differ, NONE is not an instance of NONETYPE"
    assert NewNone == NONE, "== Comparison for NONE object differs."
    with pytest.raises(NotImplementedError):
        NONE.someattribute
    with pytest.raises(NotImplementedError):
        NONE.someattribute = "somevalue"
    with pytest.raises(NotImplementedError):
        del NONE.someattribute
    with pytest.raises(NotImplementedError):
        class NewNoneType(NONETYPE):
            ...


def test_and_then():
    opt: Option[int] = Option(20)
    value = NONE

    def seti(v: int):
        nonlocal value
        value = v

    new_opt = opt.and_then(seti)
    assert value == 20, f"Expected value to be 20, found {value}"
    assert new_opt is opt, f"Expected the same Option reference"
    value = 20
    opt.reset().and_then(seti)
    assert value == 20, f"Expected and_then skip on Empty Option"


def test_or_else():
    opt: Option[int] = Option()
    value = 20

    def seti():
        nonlocal value
        value = NONE

    new_opt = opt.or_else(seti)
    assert value is NONE, f"Expected value to be NONE, found {value}"
    assert new_opt is opt, f"Expected the same Option reference"
    value = 20
    opt.reset(20).or_else(seti)
    assert value == 20, f"Expected or_else skip on Non-Empty Option"


def test_has_value():
    opt: Option[int] = Option()
    assert (
        not opt.has_value()
    ), f"Expected opt to have no value, one was found: {opt.value()}"
    opt.reset(21)
    assert opt.has_value(), f"Expected opt to have value, but NONE was found"


def test_value():
    opt: Option[int] = Option()
    with pytest.raises(ValueError):
        opt.value()
    opt.reset(20)
    assert (v := opt.value()) == 20, f"Expected value of 20, found {v}"


def test_value_or():
    opt: Option[int] = Option()
    assert (v := opt.value_or(5052)) == 5052, f"Expected value of 5052, found {v}"
    opt.reset(1234)
    assert (v := opt.value_or(5052)) == 1234, f"Expected value of 1234, found {v}"


def test_reset():
    opt: Option[int] = Option(5052)
    assert (
        v := opt.value_or(-1)
    ) == 5052, f"Expected current value to be 5052, found {v}"
    opt.reset(1234)
    assert (
        v := opt.value_or(-1)
    ) == 1234, f"Expected current value to be 1234, found {v}"
    assert (
        opt.reset() is opt
    ), f"Expected returened Option to be the exact same reference on reset"


def test_transform():
    opt: Option[int] = Option(5052)
    new_opt = opt.transform(lambda i: i - 5000)
    assert new_opt is not opt, f"Expected a completely new Option instance"
    assert (
        v := new_opt.value_or(-1)
    ) == 52, f"Expected transformation result to be 52, found {v}"
    value = 1234

    def setv(v):
        nonlocal value
        value = v

    opt.reset().transform(setv)
    assert value == 1234, f"Expected transform skip on Empty Option"
