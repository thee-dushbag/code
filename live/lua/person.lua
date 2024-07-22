--- @class Person
--- @field name string
--- @field age integer
--- @field email string
local p = {}

--- @type string
p.GREETING_TEMPLATE = "Hello %s, how was your day?"

--- Create a new Person instance
--- @return Person
function p.new()
  return setmetatable({
    name = "", age = 0, email = ""
  }, { __index = p })
end

--- Initialize/reset a person instance with new fiels
--- @param self Person
--- @param name string
--- @param age integer
--- @param email string
--- @return nil
function p:init(name, email, age)
  self.name = name
  self.email = email
  self.age = age
end

--- Create a greeter string as per the GREETING_TEMPLATE setting
--- @param self Person
--- @return string
function p:greeting()
  return string.format(self.GREETING_TEMPLATE, self.name)
end

--- Print the greeting from Person:greeting
--- @param self Person
--- @return nil
function p:greet()
  print(self:greeting());
end

--- Shortcur for new then init
--- @param name string
--- @param email string
--- @param age integer
--- @return Person
function p.create(name, email, age)
  local self = p:new()
  self:init(name, email, age)
  return self
end

return {
  Person = p
}
