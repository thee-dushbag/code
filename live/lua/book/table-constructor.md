<link rel="stylesheet" href="./static/style.css">

# Table Constructor
The table data structure constructor can be used without
an argument as `{}` which will create an empty table.  
The constructor can also be used to initialize arrays
(called `sequences` or `lists`).  
Example:
```lua
-- Lua code...
days = {
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday"
}
-- the days table has keys of type number
-- which are assigned from 1 for 'Sunday' to
-- 7 for 'Saturday'.

for i = 1, #days do
  print("days["..i.."]: '"..days[i].."'")
  -- will print all the days sequentially
end
-- to get how many values are in the days table.
print("There are "..#days.." days in a week.")
```

You can also initialize a table in a record like way.  
Example:
```lua
-- Lua code...
data = {
  name = "Simon Nganga",
  age = 20,
  passion = "coding",
  school = "Havard"
}
-- These values can be accessed as
print(data.name) --> Simon Nganga
-- or
print(data['name']) --> Simon Nganga
-- for all the data keys
```

You can also nest both ways of table initialization.
Example:
```lua
-- Lua code...
data = {
  name = "Simon Nganga",
  age = 20,
  passion = "coding",
  school = "Havard",
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday"
}

-- the days of the week from sunday have no keys
-- hence, lua assigns them a numeric key from 1 to the last
-- with no key
```

Note: Some strings cannot be used as table keys.
Example `'+'` and any other stringed operator.  
To deal with this use the special syntax.

```lua
-- Lua code...
data = {
  ["my name"] = "Simon Nganga",
  ['+'] = 'addition operator'
}
print("Hello "..data['my name']..'?')
print("'+' is the "..data['+']..' in lua.')
-- consider
arr = {'r', 'g', 'b'}
-- is equal to
arr = {
  [1] = 'r',
  [2] = 'g',
  [3] = 'b'
}
```