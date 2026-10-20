API reference
=============

.. automodule:: result
   :no-members:

.. Result and OkErr are defined in result.result but exported from result.
   autodoc looks up attribute docstrings in the module it is given, so it
   cannot see them under the public name; they are written out here instead.

.. py:type:: Result[T, E]
   :canonical: Ok[T] | Err[E]

   A simple ``Result`` type inspired by Rust.

   Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
   have been implemented, only the ones that make sense in the Python
   context.

.. py:data:: OkErr
   :value: (Ok, Err)

   A type to use in ``isinstance`` checks.

   This is purely for convenience sake, as you could also just write
   ``isinstance(res, (Ok, Err))``.

.. autoclass:: result.Ok

.. autoclass:: result.Err

.. autoexception:: result.UnwrapError
