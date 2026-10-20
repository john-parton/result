from __future__ import annotations

from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Final,
    Literal,
    NoReturn,
)
from warnings import warn

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


@dataclass(frozen=True, slots=True, init=False)
class Ok[T]:
    """A value that indicates success and which stores arbitrary data for the return value."""

    ok_value: T

    def __init__(self, ok_value: T, /) -> None:
        object.__setattr__(self, "ok_value", ok_value)

    def is_ok(self) -> Literal[True]:
        return True

    def is_err(self) -> Literal[False]:
        return False

    def ok(self) -> T:
        """Return the value."""
        return self.ok_value

    def err(self) -> None:
        """Return `None`."""
        return

    @property
    def value(self) -> T:
        """
        Return the inner value.

        @deprecated Use `ok_value` or `err_value` instead. This method will be
        removed in a future version.
        """
        warn(
            "Accessing `.value` on Result type is deprecated, please use "
            "`.ok_value` or `.err_value` instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.ok_value

    def expect(self, _message: str) -> T:
        """Return the value."""
        return self.ok_value

    def expect_err(self, message: str) -> NoReturn:
        """Raise an UnwrapError since this type is `Ok`."""
        raise UnwrapError(self, message)

    def unwrap(self) -> T:
        """Return the value."""
        return self.ok_value

    def unwrap_err(self) -> NoReturn:
        """Raise an UnwrapError since this type is `Ok`."""
        raise UnwrapError(self, "Called `Result.unwrap_err()` on an `Ok` value")

    def unwrap_or(self, _default: object) -> T:
        """Return the value."""
        return self.ok_value

    def unwrap_or_else(self, op: object) -> T:
        """Return the value."""
        return self.ok_value

    def unwrap_or_raise(self, e: object) -> T:
        """Return the value."""
        return self.ok_value

    def map[U](self, op: Callable[[T], U]) -> Ok[U]:
        """
        The contained result is `Ok`, so return `Ok` with original value mapped to
        a new value using the passed in function.
        """
        return Ok(op(self.ok_value))

    async def map_async[U](self, op: Callable[[T], Awaitable[U]]) -> Ok[U]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in.
        """
        return Ok(await op(self.ok_value))

    def map_or[U](self, default: object, op: Callable[[T], U]) -> U:
        """
        The contained result is `Ok`, so return the original value mapped to a new
        value using the passed in function.
        """
        return op(self.ok_value)

    def map_or_else[U](self, default_op: object, op: Callable[[T], U]) -> U:
        """
        The contained result is `Ok`, so return original value mapped to
        a new value using the passed in `op` function.
        """
        return op(self.ok_value)

    def map_err(self, op: object) -> Ok[T]:
        """The contained result is `Ok`, so return `Ok` with the original value."""
        return self

    def and_then[U, E](self, op: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in.
        """
        return op(self.ok_value)

    async def and_then_async[U, E](
        self, op: Callable[[T], Awaitable[Result[U, E]]]
    ) -> Result[U, E]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in.
        """
        return await op(self.ok_value)

    def or_else(self, op: object) -> Ok[T]:
        """The contained result is `Ok`, so return `Ok` with the original value."""
        return self

    def inspect[E](self, op: Callable[[T], Any]) -> Result[T, E]:
        """Calls a function with the contained value if `Ok`. Returns the original result."""
        op(self.ok_value)
        return self

    def inspect_err[E](self, op: Callable[[E], Any]) -> Result[T, E]:
        """Calls a function with the contained value if `Err`. Returns the original result."""
        return self


@dataclass(frozen=True, slots=True, init=False)
class Err[E]:
    """A value that signifies failure and which stores arbitrary data for the error."""

    err_value: E

    def __init__(self, err_value: E, /) -> None:
        object.__setattr__(self, "err_value", err_value)

    def is_ok(self) -> Literal[False]:
        return False

    def is_err(self) -> Literal[True]:
        return True

    def ok(self) -> None:
        """Return `None`."""
        return

    def err(self) -> E:
        """Return the error."""
        return self.err_value

    @property
    def value(self) -> E:
        """
        Return the inner value.

        @deprecated Use `ok_value` or `err_value` instead. This method will be
        removed in a future version.
        """
        warn(
            "Accessing `.value` on Result type is deprecated, please use "
            "`.ok_value` or '.err_value' instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.err_value

    def expect(self, message: str) -> NoReturn:
        """Raises an `UnwrapError`."""
        exc = UnwrapError(
            self,
            f"{message}: {self.err_value!r}",
        )
        if isinstance(self.err_value, BaseException):
            raise exc from self.err_value
        raise exc

    def expect_err(self, _message: str) -> E:
        """Return the inner value."""
        return self.err_value

    def unwrap(self) -> NoReturn:
        """Raises an `UnwrapError`."""
        exc = UnwrapError(
            self,
            f"Called `Result.unwrap()` on an `Err` value: {self.err_value!r}",
        )
        if isinstance(self.err_value, BaseException):
            raise exc from self.err_value
        raise exc

    def unwrap_err(self) -> E:
        """Return the inner value."""
        return self.err_value

    def unwrap_or[U](self, default: U) -> U:
        """Return `default`."""
        return default

    def unwrap_or_else[T](self, op: Callable[[E], T]) -> T:
        """
        The contained result is ``Err``, so return the result of applying
        ``op`` to the error value.
        """
        return op(self.err_value)

    def unwrap_or_raise[TBE: BaseException](self, e: type[TBE]) -> NoReturn:
        """The contained result is ``Err``, so raise the exception with the value."""
        raise e(self.err_value)

    def map(self, op: object) -> Err[E]:
        """Return `Err` with the same value."""
        return self

    async def map_async(self, op: object) -> Err[E]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in.
        """
        return self

    def map_or[U](self, default: U, op: object) -> U:
        """Return the default value."""
        return default

    def map_or_else[U](self, default_op: Callable[[], U], op: object) -> U:
        """Return the result of the default operation."""
        return default_op()

    def map_err[F](self, op: Callable[[E], F]) -> Err[F]:
        """
        The contained result is `Err`, so return `Err` with original error mapped to
        a new value using the passed in function.
        """
        return Err(op(self.err_value))

    def and_then(self, op: object) -> Err[E]:
        """The contained result is `Err`, so return `Err` with the original value."""
        return self

    async def and_then_async(self, op: object) -> Err[E]:
        """The contained result is `Err`, so return `Err` with the original value."""
        return self

    def or_else[T, F](self, op: Callable[[E], Result[T, F]]) -> Result[T, F]:
        """
        The contained result is `Err`, so return the result of `op` with the
        original value passed in.
        """
        return op(self.err_value)

    def inspect[T](self, op: Callable[[T], Any]) -> Result[T, E]:
        """Calls a function with the contained value if `Ok`. Returns the original result."""
        return self

    def inspect_err[T](self, op: Callable[[E], Any]) -> Result[T, E]:
        """Calls a function with the contained value if `Err`. Returns the original result."""
        op(self.err_value)
        return self


# define Result as a generic type alias for use
# in type annotations
"""
A simple `Result` type inspired by Rust.
Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
have been implemented, only the ones that make sense in the Python context.
"""
type Result[T, E] = Ok[T] | Err[E]

"""
A type to use in `isinstance` checks.
This is purely for convenience sake, as you could also just write `isinstance(res, (Ok, Err))
"""
OkErr: Final = (Ok, Err)


class UnwrapError(Exception):
    """
    Exception raised from ``.unwrap_<...>`` and ``.expect_<...>`` calls.

    The original ``Result`` can be accessed via the ``.result`` attribute, but
    this is not intended for regular use, as type information is lost:
    ``UnwrapError`` doesn't know about both ``T`` and ``E``, since it's raised
    from ``Ok()`` or ``Err()`` which only knows about either ``T`` or ``E``,
    not both.
    """

    _result: Result[object, object]

    def __init__(self, result: Result[object, object], message: str) -> None:
        self._result = result
        super().__init__(message)

    @property
    def result(self) -> Result[Any, Any]:
        """Returns the original result."""
        return self._result
