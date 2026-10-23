# Changelog

This project follows semantic versioning.

Possible log types:

- `[added]` for new features.
- `[changed]` for changes in existing functionality.
- `[deprecated]` for once-stable features removed in upcoming releases.
- `[removed]` for deprecated features removed in this release.
- `[fixed]` for any bug fixes.
- `[security]` to invite users to upgrade in case of vulnerabilities.

## [Unreleased]

- `[fixed]` Lambdas passed to methods on a `Result` (for example
  `result.map(lambda v: ...)`) no longer have unknown parameter types on the
  `Ok`/`Err` side that ignores them, which strict checkers reported
  (pyright `reportUnknownLambdaType`, pyrefly `implicit-any-lambda`). Ignored
  `op` parameters are now typed `Callable[[Never], object] | object`, so the
  lambda's parameter is `Never` on that side (it disappears when joined with
  the real type) and `Err("x").map(42)` is still accepted

## [0.18.0] - 2026-10-20

First release of the [john-parton/result](https://github.com/john-parton/result)
fork of rustedpy/result, which is no longer maintained. It is not published to
PyPI; install it from the `v0.18.0` tag (see the README). This release contains
breaking changes; the README has a migration guide.

- `[changed]` Requires Python 3.12+ (upstream supported 3.8+); the code uses
  PEP 695 generics and the `type` statement
- `[changed]` `Ok` and `Err` are frozen, slotted dataclasses. The value is a
  public field (`ok_value` / `err_value`), passed positionally only, and the
  private `_value` attribute is gone. `repr()` is now `Ok(ok_value=1)`,
  equality requires the same class, and `hash(Ok(x)) == hash(Err(x))`
- `[changed]` `Result[T, E]` is a `type` alias (`Ok[T] | Err[E]`) rather than a
  `typing.Union`, so it can no longer be passed to `isinstance`; use
  `isinstance(r, (Ok, Err))` or `OkErr`
- `[removed]` `as_async_result` and `as_result`. Use an explicit `try`/`except`
  returning `Ok`/`Err` instead (see the README)
- `[removed]` Do notation (`do()`, `do_async()`, `DoException`) and the
  `__iter__` methods on `Ok` and `Err` that supported it
- `[removed]` `is_ok()` and `is_err()` type guard functions; use `match` or
  `isinstance`. The `.is_ok()` and `.is_err()` methods remain
- `[removed]` The `typing_extensions` dependency, which was only needed for
  `TypeIs`; the package now has no runtime dependencies
- `[deprecated]` `.value` remains deprecated (since 0.11.0); use `.ok_value` or
  `.err_value`
- `[added]` Documentation built with Sphinx and published to GitHub Pages;
  `result.__version__` is read from the package metadata
- `[changed]` Development tooling: uv, ruff and pyrefly replace setuptools,
  tox, flake8 and mypy; the mypy plugin type tests are removed

## [0.17.0] - 2024-06-02

- `[added]` Add `inspect()` and `inspect_err()` methods (#185)

## [0.16.1] - 2024-02-29

- `[fixed]` PyPI not showing description (#176)

## [0.16.0] - 2023-12-23

- `[added]` Add `map_async` for async functions (#165)
- `[fixed]` Add `do_async()` to handle edge case in `do()` involving multiple inlined awaits (#149)
- `[added]` Add support for Python 3.12 (#157)

## [0.15.0] - 2023-12-04

- `[added]` Add `do` function to support Haskell-style do-notation (#149)

## [0.14.0] - 2023-11-10

- `[added]` `is_ok` and `is_err` type guard functions as alternatives to `isinstance` checks (#69)
- `[added]` Add `and_then_async` for async functions (#148)

## [0.13.1] - 2023-07-19

- `[fixed]`  Use `self._value` instead of deprecated `self.value` in `Err.expect` and `Err.unwrap` to avoid raising a warning (#133)

## [0.13.0] - 2023-07-15

- `[changed]` Include captured `Err` value when `expect` and `unwrap` are called and an `UnwrapError` is raised (#98, #132)

## [0.12.0] - 2023-06-11

- `[removed]` Drop support for Python 3.7 (#126)
- `[fixed]` Pattern matching deprecation warning (#128)
- `[changed]` Minor internal implementation details (#129, #130)

## [0.11.0] - 2023-06-11

- `[changed]` `Ok` now requires an explicit value during instantiation. Please
  check out [MIGRATING.md], it will guide you through the necessary change in
  your codebase.
- `[deprecated]` `value` property to access the inner value (#37, #121)
- `[added]` `ok_value` and `err_value` to access the inner value more safely (#37, #121)

## [0.10.0] - 2023-04-29

- `[fixed]` Make python version check PEP 484 compliant (#118)
- `[added]` `as_async_result` decorator to turn regular async functions into
  `Result` returning ones (#116)

## [0.9.0] - 2022-12-09

- `[added]` Implement `unwrap_or_raise` (#95)
- `[added]` Add support for Python 3.11 (#107)
- `[changed]` Narrowing of return types on methods of `Err` and `Ok`. (#106)
- `[fixed]` Fix failing type inference for `Result.map` and similar method
  unions (#106)

## [0.8.0] - 2022-04-17

- `[added]` `as_result` decorator to turn regular functions into
  `Result` returning ones (#33, 71)
- `[removed]` Drop support for Python 3.6 (#49)
- `[added]` Implement `unwrap_or_else` (#74), `and_then` (#90) and `or_else` (#90)

## [0.7.0] - 2021-11-19

- `[removed]` Drop support for Python 3.5 (#34)
- `[added]` Add support for Python 3.9 and 3.10 (#50)
- `[changed]` Make the `Ok` type covariant in regard to its wrapped type `T`.
  Likewise for `Err` in regard to `E`. This should result in more intuitive
  type checking behaviour. For instance, `Err[TypeError]` will get recognized
  as a subtype of `Err[Exception]` by type checkers. See [PEP 438] for a
  detailed explanation of covariance and its implications.
- `[added]` Add support for Python 3.10 pattern matching (#47)
- `[changed]` `Ok` and `Err` now define `__slots__` to save memory (#55, #58)
- `[changed]` The generic type of `UnwrapError.result` now explicitly specifies `Any` (#67)

[PEP 438]: https://www.python.org/dev/peps/pep-0483/#covariance-and-contravariance

## [0.6.0] - 2021-03-17

**IMPORTANT:** This release a big API refactoring to make the API more type
safe. Unfortunately this means some breaking changes. Please check out
[MIGRATING.md], it will guide you through the necessary changes in your
codebase.


- [changed] Split result type into `Ok` and `Err` classes (#17, #27)
- [deprecated] Python 3.4 support is deprecated and will be removed in the next
  release

## [0.5.0] - 2020-03-03

 - [added] Implement `map`, `map_err`, `map_or` and `map_or_else` (#19)
 - [added] Add `unwrap_err` and `expect_err` methods (#26)
 - [changed] Type annotations: Change parameter order
   from `Result[E, T]` to `Result[T, E]` to match Rust/OCaml/F# (#7)

## [0.4.1] - 2020-02-17

 - [added] Add `py.typed` for PEP561 package compliance (#16)

## [0.4.0] - 2019-04-17

 - [added] Add `unwrap`, `unwrap_or` and `expect` (#9)
 - [removed] Drop support for Python 2 and 3.3
 - [changed] Only install typing dependency for Python <3.5

## [0.3.0] - 2017-07-12

 - [added] This library is now fully type annotated (#4, thanks @tyehle)
 - [added] Implementations for `__ne__`, `__hash__` and `__repr__`
 - [deprecated] Python 2 support is deprecated and will be removed in the 0.4 release

## [0.2.2] - 2016-09-21

 - [added] `__eq__` magic method

## [0.2.0] - 2016-05-05

 - [added] Convenience default: `Ok()` == `Ok(True)`

## [0.1.1] - 2015-12-14

 - [fixed] Import bugfix

## [0.1.0] - 2015-12-14

 - Initial version

[MIGRATING.md]: https://github.com/rustedpy/result/blob/main/MIGRATING.md
[Unreleased]: https://github.com/john-parton/result/compare/v0.18.0...HEAD
[0.18.0]: https://github.com/john-parton/result/releases/tag/v0.18.0
[0.17.0]: https://github.com/rustedpy/result/compare/v0.16.1...v0.17.0
[0.16.1]: https://github.com/rustedpy/result/compare/v0.16.0...v0.16.1
[0.16.0]: https://github.com/rustedpy/result/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/rustedpy/result/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/rustedpy/result/compare/v0.13.1...v0.14.0
[0.13.1]: https://github.com/rustedpy/result/compare/v0.13.0...v0.13.1
[0.13.0]: https://github.com/rustedpy/result/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/rustedpy/result/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/rustedpy/result/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/rustedpy/result/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/rustedpy/result/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/rustedpy/result/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/rustedpy/result/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/rustedpy/result/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/rustedpy/result/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/rustedpy/result/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/rustedpy/result/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/rustedpy/result/compare/v0.2.2...v0.3.0
[0.2.2]: https://github.com/rustedpy/result/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/rustedpy/result/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/rustedpy/result/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/rustedpy/result/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/rustedpy/result/compare/3ca7d83...v0.1.0
