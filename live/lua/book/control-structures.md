<link rel="stylesheet" href="./static/style.css">

# Control Structures
1. <span class="special">_if_</span>
2. <span class="special">_while_</span>
3. <span class="special">_for_</span>
4. <span class="special">_repeat_</span>

The `if`, `while` and `for` structure's block can be terminated using `end` and for the `repeat`, `until` is used.

Examples:
```lua
--Lua code...
-- if then else
local a, b = 1, 10
if a < b then
  print("[if] a is less than or equal to b")
elseif a == b then
  print("[elseif] a is equal to b")
else
  print("[else] a is greater than b")
end -- end of if block

-- while loop
while a < b do
  print("[while] a: "..a)
  a = a + 1
end -- end of while block

-- for loop
----- Numeric For: Mainly used to step some numeric values from start to end.
-- [syntax]: for i=exp2,exp2,exp3 do <something> end
-- - exp1 - initalization (this is local to the for block)
-- - exp2 - end/stop value
-- - exp3 - step value (default 1)
for i = 0, b do
  print("[2 for] i: "..i)
end -- end of for block

for i = 100, 0, -10 do
  print("[3 for] i: "..i)
end -- end of for block

----- Generic For: Mainly used to traverse data in a container(table).
-- Consider some data
numbers = {9, 8, 7, 6, 5, 4, 3, 2, 1}
for index, value in ipairs(numbers) do
  print("numbers['"..index.."']: "..value)
end

data = {
  name = 'Simon Nganga',
  age = 20,
  school = 'Jkuat University'
}
for key, value in pairs(data) do
 print("data['"..key.."']: "..value)
end

--repeat loop
repeat
  print("[repeat] a: "..a)
  a = a - 1
until a == 0 -- end of repeat block
```

### Break and Return
<span class='special'>break</span> is simply used to exit a loop and can only be used in one. <span class='special'>return</span> on the other hand, is used to occassionally exit a function and return a result. A function has an implicit `return` at the end before `end` which returns nil, using return before end of the function raises an error, can only be used at the end of a block. Be it an if then else, while, for, repeat, function, class and module block.

Example:
```lua
-- Lua code

```