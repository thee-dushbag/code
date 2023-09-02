<link rel="stylesheet" href="./static/style.css">

# Lua Operators

## Arithmetic Operators
 1. `+` Addition
 2. `*` Multiplication
 3. `-` Subtraction
 4. `^` Exponentiation
 5. `/` Division
 6. `%` Modulo

## Comparator Operators
 1. `< ` Less than
 2. `> ` Greater than
 3. `<=` Less than or equal to
 4. `>=` Greater than or equal to
 5. `==` Equals
 6. `~=` Not Equals

Note: Two values, except for the basic
types, are equal iff they are the same
objects.

```lua
-- Lua code...
a = {}; a.x = 1; a.y = 2
b = {}; b.x = 1; b.y = 2
c = a
print(a == c) --> true
print(a == b) --> false
-- nil is only equal to nil
```

## Logical Operators
1. <span class="special">_not_</span>
2. <span class="special">_or_</span>
3. <span class="special">_and_</span>

Note: false and nil are the only values that are  
false in lua, others are true. To delete a variable  
in lua, assign it a nil, even in the table

The c expression 
```c
// c code...
int a = 8, b = 9, c;
c = (a == 0)? b * 10: b * 5;
```
can be written as
```lua
-- Lua code...
a = 8; b = 9
c = (a == 0) and (b * 10) or (b * 5)
-- though, it's not advised to use it. Use
if a == 0 then c = b * 10 else c = b * 5 end
-- verbose but correct, certainly...(*_*)
```
in lua.

## Concatenation and Length Operator
Note: Lua, like javascript, has coersion.
Example:
```lua
-- Lua code...
value = 5 + '5'
print(value) --> 10
print(type(value)) --> number
```

To concatenate strings, use <span class="special">..</span> operator. (Two adjacent dots.)  
Note: string lua type is a table of characters with number indecies. (I told you, it's getting crazy.) and that is actually how lua arrays work, just tables with integer keys.

To get the length of an array(a table with number keys in some order) use <span class="special">#</span> operator.  
Note: Lua indexing starts at 1 (Juat a convention.)

Concatenation example
```lua
-- Lua code...
myname = 'Simon Nganga'
print("Hello "..myname..", how was your day?")
-- Hello Simon Nganga, how was your day?

-- if its argument is not an string, it is converted to on
-- therefore, Coersion comes to the rescue...(o_o)
print(0..1) --> 01
```

Length operator example
```lua
--Lua code...
value = '123456789'
print(#value) --> 9
```

## Multiline String
Lua supports multiline strings.
The Quotes ('' and "") strings are single line strings, for multiline, we use operators 
<span class='special'>[[]]</span>.
Example:

```lua
-- Lua code...
sstr = 'String One'
dstr = "String Two"
mstr = [[
  String
  Three
]]

function stype(args)
  for _, arg in ipairs(args) do
    print("Typeof '"..arg.."': "..type(arg))
  end
end

stype({sstr, dstr, mstr})
-- Output:

```
