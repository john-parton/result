"""A `Result` type inspired by Rust: `Ok(value)` or `Err(error)`."""

from importlib.metadata import version

from .result import (
    Err,
    Ok,
    OkErr,
    Result,
    UnwrapError,
)

__all__ = [
    "Err",
    "Ok",
    "OkErr",
    "Result",
    "UnwrapError",
]
__version__ = version("result")
