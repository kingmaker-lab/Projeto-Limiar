#include "simulation.hpp"
#include <chrono>
#include <iostream>
#include <string_view>

int main(int argc, char** argv) {
    bool bench = argc == 2 && std::string_view(argv[1]) == "--bench";
    Simulation simulation(100, 100);
    for (int i = 0; i < (bench ? 100 : 2); ++i)
        simulation.add({{5.0 + i % 10 * 9, 5.0 + i / 10 * 9}, {i % 2 ? -3.0 : 3.0, 1}, 1, 1});
    auto start = std::chrono::steady_clock::now();
    for (int i = 0; i < (bench ? 1000 : 240); ++i) simulation.step(1.0 / 120);
    if (bench)
        std::cout << "seconds=" << std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count() << '\n';
    else
        for (const auto& p : simulation.particles())
            std::cout << p.position.x << ' ' << p.position.y << '\n';
}
