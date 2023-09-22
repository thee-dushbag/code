local mod2 = require("mod2")
local name = "Simon Nganga"
mod2.hello(name)
mod2.hi(name)

mod2.greet {
  name = name,
  template = "Hi $name?"
}

local names = {
  "Simon",
  "Nganga",
  "Njoroge",
  "Faith",
  "Njeri",
  "Wanjiru"
}

-- local f = io.open("test.txt", "r")
-- if f then
--   for line in f:lines() do
--     print("Line: "..tostring(line))
--   end
--   -- for counter = 1, 10 do
--   --   f:write("This is line "..tostring(counter)..'\n')
--   -- end
--   f:close()
-- end

-- local file = io.open("test.txt", "r+")
-- if file then
--   file:write("Hello World")
--   file:close()
-- end
-- local next_value = mod2.values(names)
-- while true do
--   local value = next_value()
--   if value == nil then break end
--   print("Value: "..tostring(value))
-- end

-- for vname in mod2.values(names) do
--   print("Name: "..tostring(vname))
-- end

-- local first, second, last = table.unpack {
--   "Simon",
--   "Nganga",
--   "Njoroge"
-- }

-- print(first, second, last)

-- do
--   local oldPrint = print
--   print = function (...)
--     oldPrint("Printing: ", ...)
--   end
-- end
