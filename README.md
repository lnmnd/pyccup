# Pyccup

[![Build Status](https://travis-ci.org/lnmnd/pyccup.svg?branch=master)](https://travis-ci.org/lnmnd/pyccup)

Pyccup is a library for representing HTML in Python. It is a Python port of [Hiccup](https://github.com/weavejester/hiccup).


## Installation

Requires Python 3.3-3.6.

```sh
$ pip install git+https://github.com/lnmnd/pyccup@0.1.0
```

## Usage

The main function is called `html`.

```python
>>> from pyccup import html
```

The input of `html` can be a string or a list and it returns a HTML string.

String inputs are converted to text nodes.

```python
>>> html('hi')
'hi'
```

And they are escaped.

```python
>>> html('<strong>hi</strong>')
'&lt;strong&gt;hi&lt;/strong&gt;'
```

But not if they are safe strings.

```python
>>> from pyccup import safe
>>> html(safe('<strong>hi</strong>'))
'<strong>hi</strong>'
```

Lists and tuples represent HTML elements. They need at least one item. The first item is always the tag.

```python
>>> html(['br'])
'<br/>'
>>> html(('br',))
'<br/>'
```

If there is a second item and it is a dictionary the key-value pairs are added as attributes of the element.

```python
>>> html(['br', {'id': 'i', 'class': 'c'}])
'<br class="c" id="i"/>'
```

Else they are evaluated like the root element and appended as children.

```python
>>> html(['p', {'class': 'c'}, 'hi'])
'<p class="c">hi</p>'
>>> html(['div', ['p', ['span', 'hi']], ['p', 'hello']])
'<div><p><span>hi</span></p><p>hello</p></div>'
```

It provides syntax sugar for id and class attributes.

```python
>>> html(['p#i.c1.c2', 'hi'])
'<p class="c1 c2" id="i">hi</p>'
```
