#include "simulation.hpp"
#include <algorithm>
#include <cmath>
#include <stdexcept>

Simulation::Simulation(double w, double h) : width(w), height(h) {
    if (!std::isfinite(w) || !std::isfinite(h) || w <= 0 || h <= 0)
        throw std::invalid_argument("invalid bounds");
}

void Simulation::add(Particle p) {
    for (double value : {p.radius, p.mass, p.position.x, p.position.y, p.velocity.x, p.velocity.y})
        if (!std::isfinite(value)) throw std::invalid_argument("invalid particle");
    if (p.radius <= 0 || p.mass < 1e-9 || p.position.x < p.radius || p.position.y < p.radius ||
        p.position.x > width - p.radius || p.position.y > height - p.radius)
        throw std::invalid_argument("particle outside bounds or invalid geometry");
    bodies.push_back(p);
}

static void wall(double& position, double& velocity, double radius, double bound) {
    position = std::clamp(position, radius, bound - radius);
    if ((position <= radius && velocity < 0) || (position >= bound - radius && velocity > 0))
        velocity = -velocity;
}

void Simulation::step(double dt) {
    if (!std::isfinite(dt) || dt <= 0 || dt > 1) throw std::invalid_argument("invalid time step");
    for (auto& p : bodies) {
        p.position.x += dt * p.velocity.x;
        p.position.y += dt * p.velocity.y;
    }
    for (size_t i = 0; i < bodies.size(); ++i) {
        for (size_t j = i + 1; j < bodies.size(); ++j) {
            auto& a = bodies[i];
            auto& b = bodies[j];
            double dx = b.position.x - a.position.x, dy = b.position.y - a.position.y;
            double distance = std::hypot(dx, dy), overlap = a.radius + b.radius - distance;
            if (overlap < 0) continue;
            Vec normal = distance ? Vec{dx / distance, dy / distance} : Vec{1, 0};
            double invA = 1 / a.mass, invB = 1 / b.mass, total = invA + invB;
            a.position.x -= overlap * normal.x * invA / total;
            a.position.y -= overlap * normal.y * invA / total;
            b.position.x += overlap * normal.x * invB / total;
            b.position.y += overlap * normal.y * invB / total;
            double speed = (b.velocity.x - a.velocity.x) * normal.x +
                           (b.velocity.y - a.velocity.y) * normal.y;
            if (speed >= 0) continue;
            double impulse = -2 * speed / total;
            a.velocity.x -= impulse * invA * normal.x;
            a.velocity.y -= impulse * invA * normal.y;
            b.velocity.x += impulse * invB * normal.x;
            b.velocity.y += impulse * invB * normal.y;
        }
    }
    for (auto& p : bodies) {
        wall(p.position.x, p.velocity.x, p.radius, width);
        wall(p.position.y, p.velocity.y, p.radius, height);
    }
}
