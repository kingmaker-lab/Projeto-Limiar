local Policy = require("policy")
local policy = Policy.new()
local MAX_LINE = 256

local function integer(word)
    if not word:match("^[0-9]+$") then
        return nil
    end
    local value = tonumber(word)
    if math.type(value) == "integer" and value >= 0 then
        return value
    end
end

local function execute(line)
    local args = {}
    for word in line:gmatch("%S+") do
        args[#args + 1] = word
    end
    if args[1] == "publish" and #args == 4 then
        local maintenance
        if args[3] == "on" or args[3] == "off" then
            maintenance = args[3] == "on"
        end
        return policy:publish(integer(args[2]), maintenance, integer(args[4]))
    elseif args[1] == "admit" and #args == 2 then
        return policy:admit(args[2])
    elseif args[1] == "release" and #args == 2 then
        return policy:release(args[2])
    end
    return "invalid"
end

-- Limita memória antes de ler uma linha vindoura de um arquivo ou pipe.
local function read_event()
    local bytes = {}
    while true do
        local byte = io.read(1)
        if byte == "\n" or (byte == nil and #bytes > 0) then
            return table.concat(bytes)
        end
        if byte == nil then
            return nil
        end
        if #bytes == MAX_LINE then
            io.stderr:write("evento excede 256 bytes\n")
            os.exit(64)
        end
        bytes[#bytes + 1] = byte
    end
end

while true do
    local line = read_event()
    if line == nil then break end
    local result = execute(line)
    io.write(string.format("%d\t%d\t%s\n", policy.generation, policy.active, result))
end
