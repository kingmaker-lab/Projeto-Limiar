local Limiter = {}
Limiter.__index = Limiter

local function integer(value, min, max)
    return math.type(value) == "integer" and value >= min and value <= max
end

function Limiter.new(rate, burst)
    assert(integer(rate, 1, 1000000) and integer(burst, 1, 1000000), "invalid rate or burst")
    return setmetatable({rate = rate, capacity = burst * 1000, keys = {}, count = 0}, Limiter)
end

function Limiter:admit(key, time, cost)
    assert(type(key) == "string" and #key <= 64 and key:match("^[a-zA-Z0-9_-]+$"), "invalid key")
    assert(integer(time, 0, 1000000000000) and integer(cost, 1, self.capacity // 1000), "invalid request")
    local bucket = self.keys[key]
    if not bucket then
        assert(self.count < 10000, "too many keys")
        bucket = {last = time, credit = self.capacity}
        self.keys[key] = bucket
        self.count = self.count + 1
    end

    assert(time >= bucket.last, "timestamp went backwards")
    bucket.credit = math.min(self.capacity, bucket.credit + (time - bucket.last) * self.rate)
    bucket.last = time
    local demand = cost * 1000
    if bucket.credit < demand then
        return false, (demand - bucket.credit + self.rate - 1) // self.rate
    end
    bucket.credit = bucket.credit - demand
    return true, 0
end

return Limiter
