local M = {}

M.add = function(a, b)
  return a + b
end

M.sub = function(a, b)
  return a - b
end

M.mul = function(a, b)
  return a * b
end

M.div = function(a, b)
  return a / b
end

M.exp = function(a, b)
  return a ^ b
end

M.mod = function(a, b)
  return a % b
end

return M