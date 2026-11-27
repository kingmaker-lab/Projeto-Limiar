#pragma once
#include <vector>

struct Vec { double x, y; };
struct Particle { Vec position, velocity; double radius, mass; };
class Simulation {
    double width, height;
    std::vector<Particle> bodies;
public:
    Simulation(double width, double height);
    void add(Particle particle);
    void step(double dt);
    const std::vector<Particle>& particles() const { return bodies; }
};
