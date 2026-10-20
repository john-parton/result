# Result

[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/john-parton/result/ci.yml?branch=main)](https://github.com/john-parton/result/actions/workflows/ci.yml?query=branch%3Amain)

A simple Result type for Python 3.12+ [inspired by
Rust](https://doc.rust-lang.org/std/result/), fully type annotated.

Documentation: <https://john-parton.github.io/result/>

## About this fork

This is a fork of [rustedpy/result](https://github.com/rustedpy/result), which
is no longer maintained (see
[issue 201](https://github.com/rustedpy/result/issues/201)). Many thanks to
Danilo Bargen, the rustedpy organization and all the contributors to the
original project: the design and most of the API here come from their work.

This fork makes breaking changes; see
[Changes from rustedpy/result](#changes-from-rustedpyresult) below.

LLMs (GitHub Copilot) were used to help write tests and clean up
documentation in this fork.

## Changes from rustedpy/result

Migrating from upstream:

**Requirements and tooling**

- Requires Python 3.12+ (upstream supports 3.8+). The code uses PEP 695
  generics (`class Ok[T]`), and the package has no runtime dependencies.
- Packaging and development use [uv](https://docs.astral.sh/uv/)
  (`uv_build`, `uv.lock`), replacing setuptools, `Makefile`, `tox` and
  `requirements-dev.txt`.
- Linting and formatting use ruff, and type checking uses pyrefly and
  pyright, replacing flake8 and mypy. The mypy plugin-based
  type tests (`tests/type_checking`) are removed.

**`Ok` and `Err`**

- They are frozen, slotted dataclasses. Assigning to or deleting a field
  raises `FrozenInstanceError`, a subclass of `AttributeError`.
- The value is a public field, `ok_value` or `err_value`, and is passed
  positionally only: `Ok(1)` works, but `Ok(value=1)` or `Ok(ok_value=1)`
  raises `TypeError`. The private `_value` attribute is gone.
- `repr()` is the dataclass default: `Ok(ok_value=1)`, not `Ok(1)`. It can no
  longer be passed to `eval()`.
- Equality requires the same class (upstream used `isinstance`), and
  `hash(Ok(x)) == hash(Err(x))`. They still compare unequal.
- They can no longer be iterated or unpacked (`__iter__` is removed).
- `.value` is still available but remains deprecated.
- `Result[T, E]` is a PEP 695 `type` alias (`Ok[T] | Err[E]`) rather than a
  `typing.Union`, so it can no longer be passed to `isinstance`. Use
  `isinstance(r, (Ok, Err))` or `OkErr`.

**Removed or merged**

- Do notation is removed: `do()`, `do_async()` and `DoException`.
- The `as_result` and `as_async_result` decorators are removed. See
  [Handling exceptions](#handling-exceptions) for the alternatives.
- The `is_ok()` and `is_err()` type guard functions are removed. Use `match`,
  or `isinstance(r, Ok)` / `isinstance(r, Err)`; the `.is_ok()` and
  `.is_err()` methods remain.
- There is no "chain everything" ethos. `match` is the primary way to handle
  a result; the combinator methods (`map`, `and_then`, ...) remain for simple
  sequences of steps. See [Pipelines](#pipelines).

## Installation

This fork is not published to PyPI: `pip install result` installs the
unmaintained upstream package, not this fork. Install a tagged release from
GitHub instead. The latest release is
[v0.18.0](https://github.com/john-parton/result/releases/tag/v0.18.0).

``` sh
$ pip install "git+https://github.com/john-parton/result@v0.18.0"
```

or, with [uv](https://docs.astral.sh/uv/):

``` sh
$ uv add git+https://github.com/john-parton/result --tag v0.18.0
```

To depend on it from another project's `pyproject.toml`:

``` toml
dependencies = ["result @ git+https://github.com/john-parton/result@v0.18.0"]
```

Each [release](https://github.com/john-parton/result/releases) also has the
built wheel attached, which can be installed directly without cloning:

``` sh
$ pip install https://github.com/john-parton/result/releases/download/v0.18.0/result-0.18.0-py3-none-any.whl
```

## Summary

The idea is that a result value can be either `Ok(value)` or
`Err(error)`, with a way to differentiate between the two. `Ok` and
`Err` are both classes encapsulating an arbitrary value. `Result[T, E]`
is a generic type alias for `Ok[T] | Err[E]`. It will
change code like this:

``` python
def get_user_by_email(email: str) -> tuple[User | None, str | None]:
    """
    Return the user instance or an error message.
    """
    if not user_exists(email):
        return None, "User does not exist"
    if not user_active(email):
        return None, "User is inactive"
    user = get_user(email)
    return user, None


user, reason = get_user_by_email("ueli@example.com")
if user is None:
    raise RuntimeError(f"Could not fetch user: {reason}")
else:
    do_something(user)
```

To something like this:

``` python
from result import Ok, Err, Result


def get_user_by_email(email: str) -> Result[User, str]:
    """
    Return the user instance or an error message.
    """
    if not user_exists(email):
        return Err("User does not exist")
    if not user_active(email):
        return Err("User is inactive")
    user = get_user(email)
    return Ok(user)


match get_user_by_email(email):
    case Ok(user):
        # type(user) == User
        do_something(user)
    case Err(reason):
        # type(reason) == str
        raise RuntimeError(f"Could not fetch user: {reason}")
```

`Ok` and `Err` support positional patterns, and type checkers narrow the
captured value, so `match` is the recommended way to handle a result. If
you only need one branch, `isinstance(result, Ok)` and
`isinstance(result, Err)` narrow the type too; note that `.ok_value` exists
only on an instance of `Ok` and `.err_value` exists only on an instance of
`Err`.

Not all methods
(<https://doc.rust-lang.org/std/result/enum.Result.html>) have been
implemented, only the ones that make sense in the Python context.
All of this in a package allowing easier handling of values that can
be OK or not, without resorting to custom exceptions.

## Why use Result?

The most compelling reason is that exceptions are a non-local jump. A `raise`
transfers control to whichever handler up the call stack happens to match,
skipping everything in between, and nothing in a function's signature says it
can happen. That undermines
[structured programming](https://en.wikipedia.org/wiki/Structured_programming),
where control flow is built from sequence, selection and iteration, and you
can read a function and see every way it can continue.

Returning failures as values keeps control flow local and visible. It is
easier to reason about, and the type checker will not let you touch the
success value without dealing with the failure case, so it is harder to miss
a nasty edge case.

Here is a surprising effect of using exceptions for flow control:

``` python
def read_port(raw: str) -> int:
    port = int(raw)  # ValueError if not a number
    if not 0 < port < 65536:
        raise ValueError(f"port out of range: {port}")
    return port


def configure(env: dict[str, str]) -> Config:
    return Config(host=env["HOST"], port=read_port(env["PORT"]))


try:
    config = configure(os.environ)
except ValueError as e:
    log.error("bad port: %s", e)
    config = DEFAULT_CONFIG
```

If `PORT` is not set, `env["PORT"]` raises a `KeyError`. That is not a
`ValueError`, so it jumps straight past the handler and crashes the program,
and nothing in the signatures warned you. In the other direction, any
`ValueError`, even one that has nothing to do with the port, is reported as
`bad port`.

With `Result`, every failure the caller needs to handle is part of the
return type, and the control flow reads top to bottom:

``` python
def read_port(raw: str) -> Result[int, str]:
    try:
        port = int(raw)
    except ValueError:
        return Err(f"not a number: {raw!r}")
    if not (0 < port < 65536):
        return Err(f"port out of range: {port}")
    return Ok(port)


def configure(env: dict[str, str]) -> Result[Config, str]:
    if "HOST" not in env:
        return Err("HOST is not set")
    if "PORT" not in env:
        return Err("PORT is not set")
    match read_port(env["PORT"]):
        case Err() as err:
            return err
        case Ok(port):
            return Ok(Config(host=env["HOST"], port=port))


match configure(os.environ):
    case Ok(config):
        ...
    case Err(reason):
        log.error("bad config: %s", reason)
        config = DEFAULT_CONFIG
```

It is a little longer, but the missing `PORT` is now an ordinary `Err` that
is handled in the same place as the others, and the one `try` is narrow: it
wraps only `int()`, the call that can raise (see
[Handling exceptions](#handling-exceptions)).

This does not mean exceptions are never appropriate. Use `Result` for
expected failures that callers should handle, and leave exceptions for bugs
and truly unexpected conditions.

## API

The API reference is built from the docstrings with
[Sphinx](https://www.sphinx-doc.org/) and published at
<https://john-parton.github.io/result/api.html>; see
[Contributing](#contributing) for how to build it locally.

Creating an instance:

``` python
>>> from result import Ok, Err
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
```

Checking whether a result is `Ok` or `Err`:

``` python
match result:
    case Ok(value):
        do_something(value)
    case Err(error):
        raise RuntimeError(error)
```

`isinstance` is handy when you only care about one branch:

``` python
if isinstance(result, Err):
    raise RuntimeError(result.err_value)
do_something(result.ok_value)
```

The `.is_ok()` and `.is_err()` methods return plain booleans, which is fine
for filters and assertions, but type checkers don't use them to narrow
`result`.

You can also check if an object is `Ok` or `Err` by using the `OkErr`
type. Please note that this type is designed purely for convenience, and
should not be used for anything else. Using `(Ok, Err)` also works fine:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> isinstance(res1, OkErr)
True
>>> isinstance(res2, OkErr)
True
>>> isinstance(1, OkErr)
False
>>> isinstance(res1, (Ok, Err))
True
```

Convert a `Result` to the value or `None`:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.ok()
'yay'
>>> res2.ok() is None
True
```

Convert a `Result` to the error or `None`:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.err() is None
True
>>> res2.err()
'nay'
```

Access the value directly, without any other checks:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.ok_value
'yay'
>>> res2.err_value
'nay'
```

Note that these are frozen fields: you cannot assign to them. Results are
immutable.

When the value inside is irrelevant, we suggest using `None` or a
`bool`, but you're free to use any value you think works best. An
instance of a `Result` (`Ok` or `Err`) must always contain something. If
you're looking for a type that might contain a value you may be
interested in a [maybe](https://github.com/rustedpy/maybe).

The `unwrap` method returns the value if `Ok` and `unwrap_err` method
returns the error value if `Err`, otherwise it raises an `UnwrapError`:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.unwrap()
'yay'
>>> res2.unwrap()
Traceback (most recent call last):
  ...
result.result.UnwrapError: Called `Result.unwrap()` on an `Err` value: 'nay'
>>> res1.unwrap_err()
Traceback (most recent call last):
  ...
result.result.UnwrapError: Called `Result.unwrap_err()` on an `Ok` value
>>> res2.unwrap_err()
'nay'
```

A custom error message can be displayed instead by using `expect` and
`expect_err`:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.expect('not ok')
'yay'
>>> res2.expect('not ok')
Traceback (most recent call last):
  ...
result.result.UnwrapError: not ok: 'nay'
>>> res1.expect_err('not err')
Traceback (most recent call last):
  ...
result.result.UnwrapError: not err: 'yay'
>>> res2.expect_err('not err')
'nay'
```

A default value can be returned instead by using `unwrap_or` or
`unwrap_or_else`:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.unwrap_or('default')
'yay'
>>> res2.unwrap_or('default')
'default'
>>> res1.unwrap_or_else(str.upper)
'yay'
>>> res2.unwrap_or_else(str.upper)
'NAY'
```

The `unwrap` method will raised an `UnwrapError`. A custom exception can
be raised by using the `unwrap_or_raise` method instead:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.unwrap_or_raise(ValueError)
'yay'
>>> res2.unwrap_or_raise(ValueError)
Traceback (most recent call last):
  ...
ValueError: nay
```

Values and errors can be mapped using `map`, `map_or`, `map_or_else` and
`map_err`:

``` python
>>> Ok(1).map(lambda x: x + 1)
Ok(ok_value=2)
>>> Err('nay').map(lambda x: x + 1)
Err(err_value='nay')
>>> Ok(1).map_or(-1, lambda x: x + 1)
2
>>> Err(1).map_or(-1, lambda x: x + 1)
-1
>>> Ok(1).map_or_else(lambda: 3, lambda x: x + 1)
2
>>> Err('nay').map_or_else(lambda: 3, lambda x: x + 1)
3
>>> Ok(1).map_err(lambda x: x + 1)
Ok(ok_value=1)
>>> Err(1).map_err(lambda x: x + 1)
Err(err_value=2)
```

Both the `Ok` and `Err` classes are frozen, slotted dataclasses: assigning
to a field raises `FrozenInstanceError` (a subclass of `AttributeError`),
adding an attribute also fails (with `TypeError` before Python 3.14, due to
a CPython bug with frozen slotted dataclasses), and the value is passed
positionally only.

### Handling exceptions

There is no decorator for turning exception-raising functions into
`Result`-returning ones. An explicit `try`/`except` is only a few lines, and
it lets you keep the `try` narrow, so that bugs in your own code are not
silently turned into `Err`.

For third-party code, catch the specific exceptions you expect and return
`Ok` or `Err`:

``` python
def parse_port(raw: str) -> Result[int, ValueError]:
    try:
        return Ok(int(raw))
    except ValueError as e:
        return Err(e)
```

You can also map the exception to your own error type, or add context:

``` python
def load(raw: str) -> Result[Config, ConfigError]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return Err(ConfigError(f"invalid JSON: {e}"))
    return Ok(Config.from_dict(data))
```

For async code it works the same way, with `await` inside the `try`:

``` python
async def fetch(url: str) -> Result[bytes, httpx.HTTPError]:
    try:
        return Ok(await client.get_bytes(url))
    except httpx.HTTPError as e:
        return Err(e)
```

For functions you wrote yourself, return `Ok`/`Err` from the body directly
rather than raising and catching.

Catching `Exception` (or `BaseException`) is rarely a good idea; name the
exception types you expect.

### Pipelines

When each step returns a `Result`, `and_then` and `map` keep the happy path
flat: the first `Err` short-circuits the rest.

``` python
def handle(raw: str) -> Result[Reply, ValueError | OSError]:
    return parse_port(raw).and_then(connect).map(Conn.greet)
```

The same thing written with `match` is noticeably longer:

``` python
def handle(raw: str) -> Result[Reply, ValueError | OSError]:
    match parse_port(raw):
        case Err() as err:
            return err
        case Ok(port):
            pass
    match connect(port):
        case Err() as err:
            return err
        case Ok(conn):
            return Ok(conn.greet())
```

Use whichever reads better. This fork just doesn't push a "chain everything"
style: reach for a pipeline when the steps are a simple sequence of
`Result`-returning functions, and for `match` when you need to branch on or
handle each outcome.

## Type checking

The library is fully annotated and is checked with
[pyrefly](https://pyrefly.org/) and [pyright](https://github.com/microsoft/pyright)
(Pylance in strict mode). Any modern type checker should work, including
narrowing in `match` statements and `isinstance` checks.

## Contributing

Requires [uv](https://docs.astral.sh/uv/).

1. Run `uv sync` to create the virtualenv and install dependencies
2. Switch to a new git branch and make your changes
3. Test your changes:
  - `uv run pytest`
  - `uv run ruff check` and `uv run ruff format --check`
  - `uv run pyrefly check`
  - You can also start a Python REPL (`uv run python`) and import `result`
4. Update documentation
  - Edit any relevant docstrings, markdown files
  - Build the docs with
    `uv run --group docs sphinx-build -W docs docs/_build/html`
    and open `docs/_build/html/index.html`
5. Add an entry to the [changelog](https://github.com/john-parton/result/blob/main/CHANGELOG.md)
6. Git commit all your changes and create a new PR.

## Related Projects

- [dry-python/returns: Make your functions return something meaningful, typed, and safe!](https://github.com/dry-python/returns)
- [alexandermalyga/poltergeist: Rust-like error handling in Python, with type-safety in mind.](https://github.com/alexandermalyga/poltergeist)

## License

MIT License
