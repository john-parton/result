<!-- markdownlint-disable -->

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `result`




**Global Variables**
---------------
- **OkErr**

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Ok`
A value that indicates success and which stores arbitrary data for the return value. 

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(value: 'T') → None
```






---

#### <kbd>property</kbd> ok_value

Return the inner value. 

---

#### <kbd>property</kbd> value

Return the inner value. 

@deprecated Use `ok_value` or `err_value` instead. This method will be removed in a future version. 



---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L185"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'Callable[[T], Result[U, E]]') → Result[U, E]
```

The contained result is `Ok`, so return the result of `op` with the original value passed in 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L192"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'Callable[[T], Awaitable[Result[U, E]]]') → Result[U, E]
```

The contained result is `Ok`, so return the result of `op` with the original value passed in 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → None
```

Return `None`. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(_message: 'str') → T
```

Return the value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L113"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(message: 'str') → NoReturn
```

Raise an UnwrapError since this type is `Ok` 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L207"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], Any]') → Result[T, E]
```

Calls a function with the contained value if `Ok`. Returns the original result. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L214"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], Any]') → Result[T, E]
```

Calls a function with the contained value if `Err`. Returns the original result. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → Literal[False]
```





---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → Literal[True]
```





---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L149"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'Callable[[T], U]') → Ok[U]
```

The contained result is `Ok`, so return `Ok` with original value mapped to a new value using the passed in function. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L156"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'Callable[[T], Awaitable[U]]') → Ok[U]
```

The contained result is `Ok`, so return the result of `op` with the original value passed in 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'object') → Ok[T]
```

The contained result is `Ok`, so return `Ok` with the original value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'object', op: 'Callable[[T], U]') → U
```

The contained result is `Ok`, so return the original value mapped to a new value using the passed in function. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L172"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'object', op: 'Callable[[T], U]') → U
```

The contained result is `Ok`, so return original value mapped to a new value using the passed in `op` function. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → T
```

Return the value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'object') → Ok[T]
```

The contained result is `Ok`, so return `Ok` with the original value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → T
```

Return the value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L125"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → NoReturn
```

Raise an UnwrapError since this type is `Ok` 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(_default: 'U') → T
```

Return the value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'object') → T
```

Return the value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(e: 'object') → T
```

Return the value. 


---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L234"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Err`
A value that signifies failure and which stores arbitrary data for the error. 

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L250"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(value: 'E') → None
```






---

#### <kbd>property</kbd> err_value

Return the inner value. 

---

#### <kbd>property</kbd> value

Return the inner value. 

@deprecated Use `ok_value` or `err_value` instead. This method will be removed in a future version. 



---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L393"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'object') → Err[E]
```

The contained result is `Err`, so return `Err` with the original value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L399"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'object') → Err[E]
```

The contained result is `Err`, so return `Err` with the original value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L277"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → E
```

Return the error. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L306"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(message: 'str') → NoReturn
```

Raises an `UnwrapError`. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L318"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(_message: 'str') → E
```

Return the inner value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L412"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], Any]') → Result[T, E]
```

Calls a function with the contained value if `Ok`. Returns the original result. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L418"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], Any]') → Result[T, E]
```

Calls a function with the contained value if `Err`. Returns the original result. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L268"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → Literal[True]
```





---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L265"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → Literal[False]
```





---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L361"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'object') → Err[E]
```

Return `Err` with the same value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L367"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'object') → Err[E]
```

The contained result is `Ok`, so return the result of `op` with the original value passed in 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L386"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'Callable[[E], F]') → Err[F]
```

The contained result is `Err`, so return `Err` with original error mapped to a new value using the passed in function. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L374"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'U', op: 'object') → U
```

Return the default value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L380"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'Callable[[], U]', op: 'object') → U
```

Return the result of the default operation 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L271"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → None
```

Return `None`. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L405"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'Callable[[E], Result[T, F]]') → Result[T, F]
```

The contained result is `Err`, so return the result of `op` with the original value passed in 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L324"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → NoReturn
```

Raises an `UnwrapError`. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L336"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → E
```

Return the inner value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L342"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(default: 'U') → U
```

Return `default`. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L348"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'Callable[[E], T]') → T
```

The contained result is ``Err``, so return the result of applying ``op`` to the error value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L355"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(e: 'Type[TBE]') → NoReturn
```

The contained result is ``Err``, so raise the exception with the value. 


---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L442"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `UnwrapError`
Exception raised from ``.unwrap_<...>`` and ``.expect_<...>`` calls. 

The original ``Result`` can be accessed via the ``.result`` attribute, but this is not intended for regular use, as type information is lost: ``UnwrapError`` doesn't know about both ``T`` and ``E``, since it's raised from ``Ok()`` or ``Err()`` which only knows about either ``T`` or ``E``, not both. 

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L455"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(result: 'Result[object, object]', message: 'str') → None
```






---

#### <kbd>property</kbd> result

Returns the original result. 






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
