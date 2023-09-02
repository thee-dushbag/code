function factorial(n)
  if n == 0 then
    return 1
  else
    return n * factorial(n - 1)
  end
end

mod = require("mod")
-- mod.hi("Simon Nganga")
-- print(factorial(4))

-- use tonumber to convert a string to a number
-- use tostring to convert a number to a string
-- to get the length of a number, prefix it with #

function testnumb()
  number = mod.getnumber()
  if number then
    print("Hoooray! You entered as number: "..number)
  else
    print("(-_-).. Don't you know what a number is?")
  end
end

function luaerror()
  error("This is an error...")
end

-- mod.getstringsize()
-- mod['getstringsize']()
-- print("How many values in mod: "..#mod)
-- print(mod)
-- testnumb()
-- luaerror()
-- mod.tabledata()
-- mod.daysprint()
-- mod.testkeys()
-- mod.scopes()
-- mod.structures()
-- mod.breaking()
-- mod.doend()
-- mod.stringtypes()
-- mod.multfunc()
-- mod.testfunc()
-- mod.multargfuncr()

-- m = require('test')
-- print(type(m))
-- m.hello()
mod.named()
