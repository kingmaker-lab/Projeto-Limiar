local world = require("engine").new()
world:add_npc("coruja")
world:add_mission("entrega", "coruja", 2)
world:schedule(1, "coruja", "entrega", "start")
world:schedule(3, "coruja", "entrega", "progress")
world:schedule(3, "coruja", "entrega", "progress")
for _, event in ipairs(world:advance(3)) do
    print(event.time, event.id, event.status)
end
