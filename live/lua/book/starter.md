<link rel="stylesheet" href="./static/style.css">

## Lua Starter
#### Lua comments start with `--`. Example
```lua
-- This is a comment
```
#### Lua primitive types
1. <span class="special">string</span> (both '' and "" are used, the quotes)
2. <span class="special">number</span> (any numeric value. 1..10)
3. <span class="special">nil</span> (nil is like null in js, designed to be completly unique.)
4. <span class="special">boolean</span> (true and false values)
5. <span class="special">function</span> (function keyword is used)
6. <span class="special">table</span> (surprisingly, this is also used as an array and module, wait you will see...)

Note: Lua to table as javascript to object  
#### Similarity with javascript object...
```javascript
/* Javascript code... */
mapping = {} // this is an object initialization
mapping.name = 'Simon Nganga'
mapping['name'] = 'Simon Nganga'
```

```lua
-- Lua code...
mapping = {} -- this is a table initialization
mapping.name = 'Simon Nganga'
mapping['name'] = 'Simon Nganga'
```