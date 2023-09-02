<link rel="stylesheet" href="./static/style.css">

# Lua Functions
There are two variants of functions in lua like in javascript.  
 - Anonymous Functions (Functions without names.)
 - Blocked Functions

Note: You can use the `tostring` function to convert an value to a string explicitly and `tonumber` to convert an value to a number explicitly.

Example:
```lua
-- Lua code...
function block_function(arg1, arg2, arg3)
  for i = 1, 10 do
    print("i: "..i)
  end
end
---> Unnamed function.
anonymous_function = function(arg1, arg2, arg3)
  print("Hello world...")
end
function main()
  -- Calling functions...
  block_function(1, 2, 3)
  anonymous_function(1, 2, 3)
  -- Functions are also first class in Lua, Therefore.
  func = anonymous_function
  function caller(f, arg1, arg2, arg3)
    return f(args1, arg2, arg3)
  end
  caller(func, 1, 2, 3)
end
```

For functions with more than one argument and none must be called with the parenthesis, parenthesis are optional for functions with one argument.

```lua
-- Lua code...
function one_arg(arg)
  print("You passed: ", arg)
end
add_arg = function(x, y) return x + y end
no_arg = function() print("No Arg Function.") end

-- Calling the functions...
one_arg 1
one_arg(1)
no_arg --> this is not a function call
no_arg()
add_arg(5, 6)
-- add_arg 5, 6 <-- Error
-- this is also okay. Both of them
one_arg {1, 2, 3, name='mapping'}
one_arg{1, 2, 3, name='mapping'}
```

Calling a function with less arguments will cause the parameters missing the values to be assigned to nil while extra arguments are discarded.

```lua
-- Lua code...
function two_args(one, two)
  print("one: "..tostring(one).." | two: "..tostring(two))
end
two_args 1 --> one: 1 | two: nil
two_args(1, 2, 3) --> one: 1 | two: 2
```

## Returning multiple values
Lua functions can return multiple results by listing them all
after the `return` keyword.

```lua
-- Lua code...
function square(number)
  return number, number ^ 2
end

for i = 1, 10 do
  number, squared = square(i) -- bind to both values
  print(number.." ^ 2 = "..squared)
end
```

___Read more Rules on Multiple Result Function in book___

Note: You can force a multi-result function to return one result by enclosing it in parenthesis.

You can unpack an array using the `unpack` function.

```lua
-- Lua code...
function myunpack(array, index)
  index = index or 1 -- if start index if not passed
  if array[index] then
    return array[index], myunpack(array, index + 1)
  end
end
-- a, b, c = unpack {1, 2, 3} -- error, i don't know why?
a, b, c = myunpack {1, 2, 3} -- okay
print(a, b, c) -- 1, 2, 3
```

## Multi argument functions
The print function in Lua can receive an arbitrary number of arguments on call.
Example:
```lua
-- Lua code ...
function add(...) -- the three dots is called the varargs
  -- it collects the arguments which again behave like an
  -- array and can be destructed. Eg
  -- local a, b = ...
  local init = 0, count
  for index, value in ipairs {...} do
    print("arguments["..index.."]: "..value)
    init = init + value
    count = index
  end
  print("You passed "..count.." values as parameters.")
  return init, count
end
sum, count = add(5, 6, 7, 8)
print("Sum: "..sum.." | Count: "..count)
-- Sum: 26 | Count: 4
```

We can use the sunction `select` to query about varargs passed to it. Function signature
`function select(selector, ...)`, the `selector` argument can
be an integer on which select will return the argument in `varargs` corresponding to that index(selector) else, selector can be a string `'#'` which will return the number of extra arguments passed to it.

Example: Let's refactor the above code. Notice `local count`.
```lua
-- Lua code...
function add(...)
  local init = 0 count = select('#', ...) -- get the number of passed varargs
  for index, value in ipairs {...} do
    print("arguments["..index.."]: "..value)
    init = init + value
  end
  print("You passed "..count.." values as parameters.")
  return init, count
end
sum, count = add(5, 6, 7, 8)
print("Sum: "..sum.." | Count: "..count)
-- Sum: 26 | Count: 4
```

## Named Arguments
Lua only supports positional arguments, named arguments are achieved through an unofficial trick.
Remember table, yes that one, can be used to pass named values that are destructed by the receiver function, check for types and must options and provide defaults to the missing parameters before passing the values to the implementation function.

Example:
```lua
-- Lua code ...
function _impl_rename(old, new, follow_symlink, throw_no_exist)
  -- Rename the old resource to the new passed name
  -- using the follow_symlink and thrwo_no_exist
  -- parameters to handle the errors or edge cases
  print("Renaming: '"..old.."' to '"..new.."'")
end

function rename(options) -- interface function
  -- check for correct types and valid values
  if type(options.old) ~= 'string' then
    error("Invalid value for old: ", options.old)
  end
  if type(options.new) ~= 'string' then
    error("Invalid value for new: ", options.new)
  end
  if options.throw_on_exit == nil then
    options.throw_on_exit = true -- default value
  end
  -- call the implementation respecting positional arguments
  return _impl_rename(
    options.old,
    options.new,
    options.follow_symlink, -- nil is also false
    options.throw_on_exit
  )
end

-- calling the interface function
rename {
  old='./content.md',
  new='./book-content.md',
  throw_on_exit=false
}
-- perfect, short and sweet.
```
