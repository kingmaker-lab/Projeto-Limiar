local Engine = {}
Engine.__index = Engine

local function identifier(value)
    assert(type(value) == "string" and #value <= 32 and value:match("^[%w_-]+$"), "invalid identifier")
end

function Engine.new()
    return setmetatable({npcs = {}, missions = {}, now = 0, queue = {}, sequence = 0}, Engine)
end

function Engine:add_npc(id)
    identifier(id)
    assert(self.npcs[id] == nil, "duplicate NPC")
    self.npcs[id] = true
end

function Engine:add_mission(id, npc, goal)
    identifier(id)
    assert(self.npcs[npc] and not self.missions[id], "unknown NPC or duplicate mission")
    assert(math.type(goal) == "integer" and goal >= 1 and goal <= 1000000, "invalid mission goal")
    self.missions[id] = {npc = npc, goal = goal, progress = 0, status = "pending"}
end

function Engine:schedule(time, npc, mission, action)
    assert(math.type(time) == "integer" and time >= self.now, "invalid time")
    assert(self.missions[mission] and self.missions[mission].npc == npc, "mission belongs to another NPC")
    assert(action == "start" or action == "progress" or action == "cancel", "unknown action")
    self.sequence = self.sequence + 1
    self.queue[#self.queue + 1] = {time = time, sequence = self.sequence, mission = mission, action = action}
end

function Engine:advance(time)
    assert(math.type(time) == "integer" and time >= self.now, "invalid time")
    table.sort(self.queue, function(a, b)
        if a.time == b.time then return a.sequence < b.sequence end
        return a.time < b.time
    end)
    local output, pending = {}, {}
    for _, event in ipairs(self.queue) do
        if event.time > time then
            pending[#pending + 1] = event
        else
            local mission = self.missions[event.mission]
            local applied = true
            if event.action == "start" and mission.status == "pending" then
                mission.status = "active"
            elseif event.action == "cancel" and (mission.status == "active" or mission.status == "pending") then
                mission.status = "cancelled"
            elseif event.action == "progress" and mission.status == "active" then
                mission.progress = mission.progress + 1
                if mission.progress == mission.goal then mission.status = "completed" end
            else
                applied = false
            end
            output[#output + 1] = {time = event.time, id = event.mission, status = mission.status, applied = applied}
        end
    end
    self.queue, self.now = pending, time
    return output
end

return Engine
