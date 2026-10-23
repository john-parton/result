"""
Callable parameters that `Ok` and `Err` ignore still give lambdas a type.

On a `Result` (`Ok[T] | Err[E]`) a type checker evaluates a lambda argument
once per union member. If the ignoring side annotates the parameter as plain
`object`, the lambda's parameters are `Unknown` there, which strict checkers
report. `assert_type` below is checked statically by pyrefly (`uv run pyrefly
check`); the calls are also run to confirm the callables are never invoked.
"""

from __future__ import annotations

from typing import Never, NoReturn, assert_type

import pytest

from result import Err, Ok


def _boom(*_args: object) -> NoReturn:
    pytest.fail("ignored callable was called")


def test_ok_ignored_callables_infer_parameters() -> None:
    ok = Ok(1)

    assert ok.unwrap_or_else(lambda e: assert_type(e, Never) and _boom()) == 1
    assert ok.map_or_else(lambda e: assert_type(e, Never) and _boom(), str) == "1"
    assert ok.map_err(lambda e: assert_type(e, Never) and _boom()) == ok
    assert ok.or_else(lambda e: assert_type(e, Never) and _boom()) == ok


def test_err_ignored_callables_infer_parameters() -> None:
    err = Err("x")

    assert err.map(lambda v: assert_type(v, Never) and _boom()) == err
    assert err.map_or("d", lambda v: assert_type(v, Never) and _boom()) == "d"
    assert (
        err.map_or_else(lambda: "d", lambda v: assert_type(v, Never) and _boom()) == "d"
    )
    assert err.and_then(lambda v: assert_type(v, Never) and _boom()) == err


@pytest.mark.asyncio
async def test_err_ignored_async_callables_infer_parameters() -> None:
    err = Err("x")

    async def boom_async(*args: object) -> None:
        _boom(*args)

    assert await err.map_async(lambda v: boom_async(assert_type(v, Never))) == err
    assert await err.and_then_async(lambda v: boom_async(assert_type(v, Never))) == err


def test_ignored_callables_accept_any_object() -> None:
    """The ignored parameter stays permissive; it is never called."""
    assert Ok(1).unwrap_or_else(42) == 1
    assert Ok(1).map_or_else(42, str) == "1"
    assert Ok(1).map_err(42) == Ok(1)
    assert Ok(1).or_else(42) == Ok(1)

    assert Err("x").map(42) == Err("x")
    assert Err("x").map_or("d", 42) == "d"
    assert Err("x").map_or_else(lambda: "d", 42) == "d"
    assert Err("x").and_then(42) == Err("x")
