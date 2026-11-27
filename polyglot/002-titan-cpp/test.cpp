#include "simulation.hpp"
#include <cassert>
#include <stdexcept>

int main() {
    Simulation world(20, 20);
    world.add({{4, 5}, {1, 0}, 1, 1});
    world.add({{6, 5}, {-1, 0}, 1, 1});
    world.add({{1, 10}, {-1, 0}, 1, 1});
    world.step(0.1);
    const auto& p = world.particles();
    assert(p[0].velocity.x == -1 && p[1].velocity.x == 1);
    assert(p[2].position.x == 1 && p[2].velocity.x == 1);
    try { world.step(0); } catch (const std::invalid_argument&) { return 0; }
    return 1;
}
