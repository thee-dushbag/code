local person = require "person"

local me = person.Person.create("Simon Nganga", "simongash@gmail.com", 21)
me:greet()
-- person.Person.GREETING_TEMPLATE = "Hey %s?"
me.GREETING_TEMPLATE = "Hey %s?"
me:greet()

local sis = person.Person.create("Faith Njeri", "faithnjeri@gmail.com", 11)
sis:greet()

--- @class Vec
--- @field x number
--- @field y number
--- @field z number
local Vec = {}

function Vec.new()
    return setmetatable({
        x = 0,
        y = 0,
        z = 0
    }, {
        __index = Vec,
        __add = function(p1, p2)
            return Vec.create(
                p1.x + p2.x,
                p1.y + p2.y,
                p1.z + p2.z
            )
        end,
        __sub = function(p1, p2)
            return Vec.create(
                p1.x - p2.x,
                p1.y - p2.y,
                p1.z - p2.z
            )
        end,
        __div = function(p1, p2)
            return Vec.create(
                p1.x / p2.x,
                p1.y / p2.y,
                p1.z / p2.z
            )
        end,
        __mul = function(p1, p2)
            return Vec.create(
                p1.x * p2.x,
                p1.y * p2.y,
                p1.z * p2.z
            )
        end,
        __concat = function(p1, p2)
            return p1 + p2 * {
                x = 10, y = 30, z = 60
            }
        end,
        __tostring = function(p)
            return p:tostring()
        end,
    });
end

function Vec:init(x, y, z)
    self.x = x
    self.y = y
    self.z = z
end

function Vec.create(x, y, z)
    local self = Vec.new()
    self:init(x, y, z)
    return self
end

function Vec:tostring()
    return string.format("Vec(x=%.2f, y=%.2f, z=%.2f)", self.x, self.y, self.z)
end

local v1, v2 = Vec.create(1, 2, 3), Vec.create(4, 5, 6)

print(v1, v2)
print(v1 + v2)
print(v1 * v2)
print(v1 - v2)
print(v1 / v2)
print(v1 .. v2)
