# Hi Package
<small>_Thank you very much_ <sup style="font-size: 5pt;">💚</sup>😃<sub style="font-size: 5pt;">💘</sub>.</small>

<style>
* {
  font-family: CaskaydiaCove Nerd Font Mono, monospace;
}

h1:hover, h2:hover, h3:hover, h4:hover, h5:hover, h6:hover {
  text-decoration: 3px solid underline;
}
</style>

## Contents

- [Hi Package](#hi-package)
  - [Contents](#contents)
  - [Introduction](#introduction)
    - [Dependencies](#dependencies)
    - [Contributors](#contributors)
  - [Package Contents](#package-contents)
  - [Description](#description)
  - [Defaults](#defaults)
  - [Usage](#usage)

## Introduction

This package provides the most commonly used functions `hi` and `say_hi`. Used by beginners to test different functions and try out new was of callbacks and everything else.

### Dependencies
1. `rich` package.
2. `click` package.
3. `python3` interpreter.

### Contributors
Thanks to ___Simon Nganga___ the sole creator and maintainer of this beautiful package. You can contact him via his [email](mailto://happyfortunes5052@gmail.com?subject=Hi) and [github](https://github.com/thee-dushbag) account.

More information can be found on the module `hi.__meta__.py`.
```python
from hi import __meta__ as meta
print(meta.__author__) # Simon Nganga
print(meta.__author_email__) # happyfortunes5052@gmail.com
# And the rest. 
```
## Package Contents

This are the main contents the package exports.
The arguments `format` and `key` have inbuilt
[defaults](#defaults "See default global variables in the package.") which can be changed.

```python
# Function signatures
def hi(name: str, *, format: Optional[str], key: Optional[str]) -> str: ...
def say_hi(name: str, *, format: Optional[str] = None, key: Optional[str] = None): ...
```

## Description

The `format` argument the exported functions represent the template used in greeting and the `key` represents the substitution for `name` in the `format` argument.

## Defaults

Script defaults.
| Argument | Type | Value |
| -------- | ----- | ----------------------------------- |
| `format` | `str` | `'Hello {name}, how was your day?'` |
| `key` | `str` | `'name'` |

Terminal defaults.
<small>The `format` value is in `rich` format.</small>
| Argument | Type | Value |
| -------- | ----- | ----------------------------------- |
| `format` | `str` | `'[green]Hello [yellow][italic]{name}[/yellow][/italic][green], how was your day?'` |
| `key` | `str` | `'name'` |

## Usage

The package is both `import`able and `terminal` capable.

- #### Scripting

The [defaults](#defaults) can be changed for global usage by changing appropriate variables.

_NOTE: \_There is a subtle difference between `hi.hi` and `hi.say_hi`. The function `hi.hi` returns its output while `hi.say_hi` prints its output._

| Target   | Variable to Change |
| -------- | ------------------ |
| `format` | `hi.FORMAT`        |
| `key`    | `hi.NAME_KEY`      |

Using defaults.

```python
# Example Usage: (Using Defaults)
import hi # Import the module
name = 'Simon Nganga' # Name to say hi to
greeting = hi.hi(name)
print(greeting) # Hello Simon Nganga, how was your day?
# This can all be shortened to.       |
hi.say_hi(name) # --------------------+
```

Using custom values.

```python
# Example Usage: (Custom Defaults)
import hi # import the package
# Change the defaults to desired appropriate values.
FORMAT = 'Hi {greet_name_here}?' # Set a custom format.
KEY = 'greet_name_here' # Set the target key for name substitution.
name = 'Simon Nganga' # Name to greet
greeting = hi.hi(name, format=FORMAT, key=KEY) # Pass the format to be used on each call.
print(greeting) # Hi Simon Nganga?
hi.say_hi(name, format=FORMAT, key=KEY) # Similar output as above.

# If the FORMAT and KEY are to be used for all functions calls
# then setting then for global use is a much better option
# instead of redundant argument passing.

hi.FORMAT = FORMAT # Set the above format as global format
hi.NAME_KEY = KEY # Set the above key as global key
greeting = hi.hi(name)
print(greeting) # Hi Simon Nganga?
hi.say_hi(name) # Similar output as above.
```

As usual, passed arguments (_ie_ `format` and `key`) override (_ie_ has a higher precedence over) the `global` [defaults](#defaults).

- #### Terminal

The package `hi` is runnable as it posses the `__main__.py` module for use with `python3 -m hi` in the terminal.

_*NOTE*: All terminal capabilities are defined in the module `hi.__main__.py` which uses the `click` and `rich` package. The terminal output is color formatted using `rich`_

Usage Defaults.

```bash
$ # Example: (Using defaults)
$ NAME="Simon Nganga"
$ python3 -m hi greet "$NAME"
$ # The actual output is (Somewhat the actual output):
$ # \033[92mHello \033[93;3mSimon Nganga\033[0m \033[92mhow was your day?\033[0m
Hello Simon Nganga, how was your day
```

Usage with custom arguments.

```bash
$ # Example: (Using custom values)
$ # Remember single quotes to prevent curly braces from expanding or throwing syntax errors in bash.
$ FORMAT='[green]Hello [bold yellow]{NAME_TO_GREET}[/bold yellow], did you eat an :apple:?'
$ # The format above is click formatted text. click will know what to do with it. (:apple: is an icon in click.)
$ KEY='NAME_TO_GREET'
$ NAME="Simon Nganga"
$ python3 -m hi greet -f "$FORMAT" -k "$KEY" "$NAME"
$ # The actual output is (Somewhat the actual output):
$ # \033[92mHello \033[93;1mSimon Nganga\033[0m \033[92mdid you eat an 🍎?\033[0m
Hello Simon Nganga, did you eat an 🍎?
```