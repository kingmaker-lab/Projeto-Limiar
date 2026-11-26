local Policy = {}
Policy.__index = Policy

local function valid_count(value)
    return math.type(value) == "integer" and value >= 1 and value <= 10000
end

function Policy.new()
    return setmetatable({
        generation = 0, maintenance = false, limit = 100, active = 0, sessions = {},
    }, Policy)
end

function Policy:publish(expected, maintenance, limit)
    if math.type(expected) ~= "integer" or expected < 0 or
        type(maintenance) ~= "boolean" or not valid_count(limit) then
        return "invalid"
    end
    if expected ~= self.generation then
        return "stale"
    end
    if self.generation == math.maxinteger then
        return "exhausted"
    end
    self.generation = self.generation + 1
    self.maintenance = maintenance
    self.limit = limit
    return "published"
end

local function valid_session(session)
    return type(session) == "string" and #session <= 64 and
        session:match("^[a-zA-Z0-9_-]+$") ~= nil
end

function Policy:admit(session)
    if not valid_session(session) then
        return "invalid"
    end
    if self.sessions[session] then
        return "duplicate"
    end
    if self.maintenance then
        return "maintenance"
    end
    if self.active >= self.limit then
        return "capacity"
    end
    self.sessions[session] = true
    self.active = self.active + 1
    return "accepted"
end

function Policy:release(session)
    if not valid_session(session) then
        return "invalid"
    end
    if not self.sessions[session] then
        return "absent"
    end
    self.sessions[session] = nil
    self.active = self.active - 1
    return "released"
end

return Policy
