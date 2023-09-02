<link rel="stylesheet" href="./static/style.css">

## Statements
### Assignments
Basic means of changing the value of a variableor a table field.  
Lua allows multiple assignments too.  
Example:
```lua
-- Lua code...
name = 'Simon Nganga' -- assign a variable a value
data = {}
data.name = name -- assign a table field a value
data['age'] = 20 -- another table field assignment

x, y = 3, 4 -- multiple assignments in lua
-- if list of variables is longer, the extras receive nil
a, b, c = 1, 2
print(a, b, c) --> 1, 2, nil
-- also, if value list has extras, they are discarded as well
d, e = 3, 4, 5 -- 5 is discarded
print(d, e) --> 3, 4
```

### Variable Scope
All the above assignments are global variables.  
To make an assignment local, use the <span class="special">local</span> keyword.  
```lua
-- Lua code...
if true then
  -- only visible in the then block
  local name = 'Simon Nganga'
  print("Hello "..name..'?')
end
print(name) --> nil
if true then
  -- visible to code after this if block
  age = 20
  print("You are "..age..'years old.')
end
print(age) --> 20
```