local Limiter = require("limiter")
local function run()
    assert(#arg == 2, "usage: lua5.4 main.lua RATE BURST")
    local limiter = Limiter.new(tonumber(arg[1]), tonumber(arg[2]))
    for line in io.lines() do
        if not line:match("^%s*$") then
            local time, key, cost = line:match("^%s*(%d+)%s+(%S+)%s+(%d+)%s*$")
            local allowed, retry = limiter:admit(key, tonumber(time), tonumber(cost))
            print(key, allowed and "allow" or "deny", retry)
        end
    end
end

local ok, problem = pcall(run)
if not ok then io.stderr:write(problem, "\n"); os.exit(2) end
