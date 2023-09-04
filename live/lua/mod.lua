local M = {} -- this is a table
-- create a table and store its reference in M
-- Gooooood stuuuuf...

-- Luas table is similar to javascript object
-- eg M.name = "Simon Nganga"
-- is same as M["name"] = "Simon Nganga"
-- and reading the values is same....

M.hi = function(name)
  print("Hello " .. name .. ", how was your day?")
end

M.getnumber = function()
  io.write("Enter a number: ")
  number = io.read()
  return tonumber(number)
end

M.getstringsize = function()
  io.write("Enter a string to get its length: ")
  str = io.read()
  print("Length of '" .. str .. "': " .. tostring(#str))
end

M.getnames = function(n)
  local count = tonumber(n)
  if count == nil then
    error("Expected a number in getnames function...")
  end
  local names = {}
  print("Enter " .. count .. " names please...")
  for i = 1, count do
    io.write("Name " .. i .. ": ")
    names[i] = io.read()
  end
  return names
end

M.tabledata = function()
  data = {
    name = 'Simon Nganga',
    age = 20,
    school = 'Havard'
  }
  print("My name is " .. data.name)
end

M.daysprint = function()
  days = {
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
  }
  for i = 1, #days do
    print("days[" .. i .. "]: '" .. days[i] .. "'")
  end
  print("There are " .. #days .. " days in a week.")
end

M.testkeys = function()
  local data = {
    ["my name"] = "Simon Nganga",
    ['+'] = 'addition operator'
  }
  print("Hello " .. data['my name'] .. '?')
  print("'+' is the " .. data['+'] .. ' in lua.')
end

M.scopes = function()
  if true then
    -- only visible in the then block
    local name = 'Simon Nganga'
    print("Hello " .. name .. '?')
  end
  -- ignore:type(nil)
  -- print(name) --> nil
  if true then
    -- visible to code after this if block
    age = 20
    print("You are " .. age .. 'years old.')
  end
  print(age) --> 20
end

M.structures = function()
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
    print("[while] a: " .. a)
    a = a + 1
  end -- end of while block

  -- for loop
  ----- Numeric For: Mainly used to step some numeric values from start to end.
  -- [syntax]: for i=exp2,exp2,exp3 do <something> end
  -- - exp1 - initalization (this is local to the for block)
  -- - exp2 - end/stop value
  -- - exp3 - step value (default 1)
  for i = 0, b do
    print("[2 for] i: " .. i)
  end -- end of for block

  for i = 100, 0, -10 do
    print("[3 for] i: " .. i)
  end -- end of for block

  ----- Generic For: Mainly used to traverse data in a container(table).
  -- Consider some data
  numbers = { 9, 8, 7, 6, 5, 4, 3, 2, 1 }
  for index, value in ipairs(numbers) do
    print("numbers['" .. index .. "']: " .. value)
  end

  data = {
    name = 'Simon Nganga',
    age = 20,
    school = 'Jkuat University'
  }
  for key, value in pairs(data) do
    print("data['" .. key .. "']: " .. value)
  end

  --repeat loop
  repeat
    print("[repeat] a: " .. a)
    a = a - 1
  until a == 0 -- end of repeat block
end

-- if there are holes in your array
-- eg arr = {}; arr[10] = 100
-- this arr has holes for index 1..9
-- to get the largest index
-- use table.maxn(arr) since #arr wont work

M.doend = function()
  do
    print("Hello ")
    print("World")
  end
end

M.breaking = function()
  return -- will not return
  -- do return end -- will return
      print("Hello World")
end

M.stringtypes = function()
  local sstr = 'String One'
  local dstr = "String Two"
  local mstr = [[
    String
    Three
  ]]
  function stype(args)
    for _, arg in ipairs(args) do
      print("Typeof '" .. arg .. "': " .. type(arg))
    end
  end

  stype({ sstr, dstr, mstr })
end

M.multfunc = function()
  function square(number)
    return number, number ^ 2
  end

  for i = 1, 10 do
    number, squared = square(i)
    print(number .. " ^ 2 = " .. squared)
  end
end

M.testfunc = function()
  local function myunpack(array, index)
    index = index or 1 -- if start index if not passed
    if array[index] then
      return array[index], myunpack(array, index + 1)
    end
  end

  -- a, b, c = unpack {1, 2, 3} -- error
  local a, b, c = myunpack { 1, 2, 3 } -- okay
  print(a, b, c)               -- 1, 2, 3
end


M.multargfunc = function()
  local function add(...)
    local init = 0
    local count
    for index, value in ipairs { ... } do
      print("arguments[" .. index .. "]: " .. value)
      init = init + value
      count = index
    end
    print("You passed " .. count .. " values as parameters.")
    return init, count
  end
  local sum, count = add(5, 6, 7, 8)
  print("Sum: " .. sum .. " | Count: " .. count)
end

M.multargfuncr = function()
  -- Lua code...
  function add(...)
    local init = 0
    count = select('#', ...)                -- get the number of passed varargs
    for index, value in ipairs { ... } do
      print("arguments[" .. index .. "]: " .. value)
      init = init + value
    end
    print("You passed " .. count .. " values as parameters.")
    return init, count
  end

  local sum, count = add(5, 6, 7, 8)
  print("Sum: " .. sum .. " | Count: " .. count)
  -- Sum: 26 | Count: 4
end

M.named = function()
  local function _impl_rename(old, new, follow_symlink, throw_no_exist)
    print("Renaming: '" .. old .. "' to '" .. new .. "'")
  end
  local function rename(options)
    if type(options.old) ~= 'string' then
      error("Invalid value for old: ", options.old)
    end
    if type(options.new) ~= 'string' then
      error("Invalid value for new: ", options.new)
    end
    if options.throw_on_exit == nil then
      options.throw_on_exit = true
    end
    return _impl_rename(
      options.old,
      options.new,
      options.follow_symlink,
      options.throw_on_exit
    )
  end
  rename {
    old = './content.md',
    new = './book-content.md',
    throw_on_exit = false
  }
end

return M
