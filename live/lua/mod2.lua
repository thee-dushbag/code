---@param template string
---@return fun(string):nil
local function _greet_impl(template)
  ---@param name string
  ---@return nil
  return function(name)
    local greeting, _ = string.gsub(template, "$name", tostring(name))
    print(greeting)
  end
end

--
---@class GreetType
---@field name string
---@field template? string
--

local DEFAULT_TEMPLATE = "Hello $name, how was your day?"

---@param options GreetType | string
local function _kgreet_impl(options)
  local name, template
  if type(options) == "string" then
    name = options
    template = DEFAULT_TEMPLATE
  else
    name = tostring(options.name)
    template = options.template or DEFAULT_TEMPLATE
  end
  _greet_impl(template)(name)
end

---@generic T
---@param sequence table<number, T>: {[number] = T}
---@return fun():T
local function _iterator_impl(sequence)
  local current_index = 0
  return function ()
    current_index = current_index + 1
    return sequence[current_index]
  end
end

---@class mod2
return {
  hello = _greet_impl("Hello $name?"),
  hi = _greet_impl("Hi $name!!!"),
  greet = _kgreet_impl,
  values = _iterator_impl
}
