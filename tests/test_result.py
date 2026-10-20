from __future__ import annotations

import pytest

from result import Err, Ok, OkErr, Result, UnwrapError


def test_ok_factories() -> None:
    instance = Ok(1)
    assert instance.ok_value == 1
    assert instance.is_ok() is True


def test_err_factories() -> None:
    instance = Err(2)
    assert instance.err_value == 2
    assert instance.is_err() is True


def test_eq() -> None:
    assert Ok(1) == Ok(1)
    assert Err(1) == Err(1)
    assert Ok(1) != Err(1)
    assert Ok(1) != Ok(2)
    assert Err(1) != Err(2)
    assert Ok(1) == Ok(1)
    assert Ok(1) != "abc"
    assert Ok("0") != Ok(0)


def test_hash() -> None:
    assert len({Ok(1), Err("2"), Ok(1), Err("2")}) == 2
    assert len({Ok(1), Ok(2)}) == 2
    assert len({Ok("a"), Err("a")}) == 2


def test_repr() -> None:
    """``repr()`` is the dataclass repr, naming the field."""
    assert repr(Ok(123)) == "Ok(ok_value=123)"
    assert repr(Err(-1)) == "Err(err_value=-1)"


def test_ok_value() -> None:
    res = Ok("haha")
    assert res.ok_value == "haha"


def test_err_value() -> None:
    res = Err("haha")
    assert res.err_value == "haha"


def test_ok() -> None:
    res = Ok("haha")
    assert res.is_ok() is True
    assert res.is_err() is False
    assert res.ok_value == "haha"


def test_err() -> None:
    res = Err(":(")
    assert res.is_ok() is False
    assert res.is_err() is True
    assert res.err_value == ":("


def test_err_value_is_exception() -> None:
    res = Err(ValueError("Some Error"))
    assert res.is_ok() is False
    assert res.is_err() is True

    with pytest.raises(UnwrapError):
        res.unwrap()

    try:
        res.unwrap()
    except UnwrapError as e:
        cause = e.__cause__
        assert isinstance(cause, ValueError)


def test_ok_method() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert o.ok() == "yay"
    assert n.ok() is None  # type: ignore[func-returns-value]


def test_err_method() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert o.err() is None  # type: ignore[func-returns-value]
    assert n.err() == "nay"


def test_expect() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert o.expect("failure") == "yay"
    with pytest.raises(UnwrapError):
        n.expect("failure")


def test_expect_err() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert n.expect_err("hello") == "nay"
    with pytest.raises(UnwrapError):
        o.expect_err("hello")


def test_unwrap() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert o.unwrap() == "yay"
    with pytest.raises(UnwrapError):
        n.unwrap()


def test_unwrap_err() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert n.unwrap_err() == "nay"
    with pytest.raises(UnwrapError):
        o.unwrap_err()


def test_unwrap_or() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert o.unwrap_or("some_default") == "yay"
    assert n.unwrap_or("another_default") == "another_default"


def test_unwrap_or_else() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert o.unwrap_or_else(str.upper) == "yay"
    assert n.unwrap_or_else(str.upper) == "NAY"


def test_unwrap_or_raise() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert o.unwrap_or_raise(ValueError) == "yay"
    with pytest.raises(ValueError) as exc_info:
        n.unwrap_or_raise(ValueError)
    assert exc_info.value.args == ("nay",)


def test_map() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert o.map(str.upper).ok() == "YAY"
    assert n.map(str.upper).err() == "nay"

    num = Ok(3)
    errnum = Err(2)
    assert num.map(str).ok() == "3"
    assert errnum.map(str).err() == 2


def test_map_or() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert o.map_or("hay", str.upper) == "YAY"
    assert n.map_or("hay", str.upper) == "hay"

    num = Ok(3)
    errnum = Err(2)
    assert num.map_or("-1", str) == "3"
    assert errnum.map_or("-1", str) == "-1"


def test_map_or_else() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert o.map_or_else(lambda: "hay", str.upper) == "YAY"
    assert n.map_or_else(lambda: "hay", str.upper) == "hay"

    num = Ok(3)
    errnum = Err(2)
    assert num.map_or_else(lambda: "-1", str) == "3"
    assert errnum.map_or_else(lambda: "-1", str) == "-1"


def test_map_err() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert o.map_err(str.upper).ok() == "yay"
    assert n.map_err(str.upper).err() == "NAY"


def test_and_then() -> None:
    assert Ok(2).and_then(sq).and_then(sq).ok() == 16
    assert Ok(2).and_then(sq).and_then(to_err).err() == 4
    assert Ok(2).and_then(to_err).and_then(sq).err() == 2
    assert Err(3).and_then(sq).and_then(sq).err() == 3

    assert Ok(2).and_then(sq_lambda).and_then(sq_lambda).ok() == 16
    assert Ok(2).and_then(sq_lambda).and_then(to_err_lambda).err() == 4
    assert Ok(2).and_then(to_err_lambda).and_then(sq_lambda).err() == 2
    assert Err(3).and_then(sq_lambda).and_then(sq_lambda).err() == 3


def test_inspect() -> None:
    oks: list[int] = []
    def add_to_oks(x: int) -> None:
        return oks.append(x)

    assert Ok(2).inspect(add_to_oks) == Ok(2)
    assert Err("e").inspect(add_to_oks) == Err("e")
    assert oks == [2]


def test_inspect_err() -> None:
    errs: list[str] = []
    def add_to_errs(x: str) -> None:
        return errs.append(x)

    assert Ok(2).inspect_err(add_to_errs) == Ok(2)
    assert Err("e").inspect_err(add_to_errs) == Err("e")
    assert errs == ["e"]


def test_inspect_regular_fn() -> None:
    oks: list[str] = []

    def _add_to_oks(x: str) -> str:
        oks.append(x)
        return x + x

    assert Ok("hello").inspect(_add_to_oks) == Ok("hello")
    assert Err("error").inspect(_add_to_oks) == Err("error")
    assert oks == ["hello"]


@pytest.mark.asyncio
async def test_and_then_async() -> None:
    assert (
        await (await Ok(2).and_then_async(sq_async)).and_then_async(sq_async)
    ).ok() == 16
    assert (
        await (await Ok(2).and_then_async(sq_async)).and_then_async(to_err_async)
    ).err() == 4
    assert (
        await (await Ok(2).and_then_async(to_err_async)).and_then_async(to_err_async)
    ).err() == 2
    assert (
        await (await Err(3).and_then_async(sq_async)).and_then_async(sq_async)
    ).err() == 3


@pytest.mark.asyncio
async def test_map_async() -> None:
    async def str_upper_async(s: str) -> str:
        return s.upper()

    async def str_async(x: int) -> str:
        return str(x)

    o = Ok("yay")
    n = Err("nay")
    assert (await o.map_async(str_upper_async)).ok() == "YAY"
    assert (await n.map_async(str_upper_async)).err() == "nay"

    num = Ok(3)
    errnum = Err(2)
    assert (await num.map_async(str_async)).ok() == "3"
    assert (await errnum.map_async(str_async)).err() == 2


def test_or_else() -> None:
    assert Ok(2).or_else(sq).or_else(sq).ok() == 2
    assert Ok(2).or_else(to_err).or_else(sq).ok() == 2
    assert Err(3).or_else(sq).or_else(to_err).ok() == 9
    assert Err(3).or_else(to_err).or_else(to_err).err() == 3

    assert Ok(2).or_else(sq_lambda).or_else(sq).ok() == 2
    assert Ok(2).or_else(to_err_lambda).or_else(sq_lambda).ok() == 2
    assert Err(3).or_else(sq_lambda).or_else(to_err_lambda).ok() == 9
    assert Err(3).or_else(to_err_lambda).or_else(to_err_lambda).err() == 3


def test_isinstance_result_type() -> None:
    o = Ok("yay")
    n = Err("nay")
    assert isinstance(o, OkErr)
    assert isinstance(n, OkErr)
    assert not isinstance(1, OkErr)


def test_error_context() -> None:
    n = Err("nay")
    with pytest.raises(UnwrapError) as exc_info:
        n.unwrap()
    exc = exc_info.value
    assert exc.result is n


def test_slots() -> None:
    """Ok and Err have slots, so assigning arbitrary attributes fails."""
    o = Ok("yay")
    n = Err("nay")
    with pytest.raises(AttributeError):
        o.some_arbitrary_attribute = 1  # type: ignore[attr-defined]
    with pytest.raises(AttributeError):
        n.some_arbitrary_attribute = 1  # type: ignore[attr-defined]


def sq(i: int) -> Result[int, int]:
    return Ok(i * i)


async def sq_async(i: int) -> Result[int, int]:
    return Ok(i * i)


def to_err(i: int) -> Result[int, int]:
    return Err(i)


async def to_err_async(i: int) -> Result[int, int]:
    return Err(i)


# Lambda versions of the same functions, just for test/type coverage
def sq_lambda(i: int) -> Result[int, int]:
    return Ok(i * i)
def to_err_lambda(i: int) -> Result[int, int]:
    return Err(i)
