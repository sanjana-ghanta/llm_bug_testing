# Bug Overview

## Bug #1: Math-82 (Off-by-One Error)
**Language:** Java  
**Type:** Logic Error  
**Difficulty:** Easy

**The Bug:**
```java
if (MathUtils.compareTo(entry, 0, epsilon) > 0) {
```

**The Fix:**
```java
if (MathUtils.compareTo(entry, 0, epsilon) >= 0) {
```

**What's Wrong:** Uses strict `>` instead of `>=`, causing the algorithm to skip valid pivot candidates when entry equals zero.

---

## Bug #2: Math-5 (Wrong Constant)
**Language:** Java  
**Type:** Edge Case  
**Difficulty:** Easy

**The Bug:**
```java
if (real == 0.0 && imaginary == 0.0) {
    return INF;
}
```

**The Fix:**
```java
if (real == 0.0 && imaginary == 0.0) {
    return NaN;
}
```

**What's Wrong:** Returns infinity instead of NaN for 1/0. Mathematically incorrect.

---

## Bug #3: Lang-6 (Variable Confusion)
**Language:** Java  
**Type:** Index Error  
**Difficulty:** Medium

**The Bug:**
```java
for (int pt = 0; pt < consumed; pt++) {
    pos += Character.charCount(Character.codePointAt(input, pt));  // uses pt
}
```

**The Fix:**
```java
for (int pt = 0; pt < consumed; pt++) {
    pos += Character.charCount(Character.codePointAt(input, pos));  // uses pos
}
```

**What's Wrong:** Uses loop counter `pt` instead of position `pos`. Causes IndexOutOfBoundsException.

---

## Bug #4: pandas-1 (Missing Item in List)
**Language:** Python  
**Type:** Logic Error  
**Difficulty:** Easy

**The Bug:**
```python
is_excluded_checks = (is_period_dtype, is_interval_dtype)  # incomplete
```

**The Fix:**
```python
is_excluded_checks = (is_period_dtype, is_interval_dtype, is_categorical_dtype)
```

**What's Wrong:** Missing `is_categorical_dtype` in exclusion list, causing categorical data to be misclassified as strings.

---

## Bug #5: black-1 (Missing Exception Handling)
**Language:** Python  
**Type:** Exception Handling  
**Difficulty:** Medium

**The Bug:**
```python
executor = ProcessPoolExecutor(max_workers=worker_count)  # can raise OSError
try:
    # use executor
finally:
    executor.shutdown()  # fails if executor is None
```

**The Fix:**
```python
try:
    executor = ProcessPoolExecutor(max_workers=worker_count)
except OSError:
    executor = None
try:
    # use executor
finally:
    if executor is not None:
        executor.shutdown()
```

**What's Wrong:** No exception handling for OSError. Then tries to call shutdown() on None.

---

## Bug #6: keras-1 (Control Dependencies)
**Language:** Python  
**Type:** Concurrency  
**Difficulty:** Hard

**The Bug:**
```python
def update(x, new_x):
    return tf_state_ops.assign(x, new_x)  # no execution guarantee
```

**The Fix:**
```python
def update(x, new_x):
    op = tf_state_ops.assign(x, new_x)
    with tf.control_dependencies([op]):  # ensures execution
        return tf.identity(x)
```

**What's Wrong:** TensorFlow operations need control dependencies to ensure execution order.

---

## Bug #7: scrapy-1 (Logic Flow Error)
**Language:** Python  
**Type:** Logic Error  
**Difficulty:** Medium

**The Bug:**
```python
for domain in allowed_domains:
    if url_pattern.match(domain):
        warnings.warn(...)  # warns but doesn't skip
domains = [re.escape(d) for d in allowed_domains if d is not None]  # includes URLs
```

**The Fix:**
```python
domains = []
for domain in allowed_domains:
    if domain is None:
        continue
    elif url_pattern.match(domain):
        warnings.warn(...)
    else:
        domains.append(re.escape(domain))  # only valid domains
```

**What's Wrong:** Warns about invalid URLs but still includes them in the regex.

---

## Bug #8: youtube-dl-1 (Boolean Logic)
**Language:** Python  
**Type:** Logic Error  
**Difficulty:** Medium

**The Bug:**
```python
UNARY_OPERATORS = {
    '': lambda v: v is not None,  # treats False as truthy
    '!': lambda v: v is None,     # treats True as falsy
}
```

**The Fix:**
```python
UNARY_OPERATORS = {
    '': lambda v: (v is True) if isinstance(v, bool) else (v is not None),  
    '!': lambda v: (v is False) if isinstance(v, bool) else (v is None),    
}
```

**What's Wrong:** Doesn't distinguish between False and None, or True and not-None.

---

## Bug Types Summary

| Type | Count |
|------|-------|
| Logic Errors | 5 |
| Exception/Null Handling | 2 |
| Index/Variable Errors | 1 |
| Concurrency | 1 |
| Edge Cases | 1 |

**Easy Bugs:** Math-82, Math-5, pandas-1  
**Medium Bugs:** Lang-6, black-1, scrapy-1, youtube-dl-1  
**Hard Bugs:** keras-1
