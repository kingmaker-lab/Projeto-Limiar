#include "schedule.hpp"
#include <cassert>
#include <random>
#include <stdexcept>

static std::int64_t exhaustive(const std::vector<Job>& jobs) {
    std::int64_t best = 0;
    for (unsigned chosen = 0; chosen < (1u << jobs.size()); ++chosen) {
        bool compatible = true;
        std::int64_t value = 0;
        for (unsigned i = 0; i < jobs.size(); ++i) {
            if (!(chosen & (1u << i))) continue;
            value += jobs[i].value;
            for (unsigned j = 0; j < i; ++j) {
                if ((chosen & (1u << j)) && jobs[i].start < jobs[j].end &&
                    jobs[j].start < jobs[i].end) compatible = false;
            }
        }
        if (compatible && value > best) best = value;
    }
    return best;
}

int main() {
    auto plan = optimize({{"long",0,10,9},{"first",0,4,6},{"second",4,10,6}});
    assert(plan.value == 12);
    assert((plan.jobs == std::vector<std::string>{"first","second"}));
    assert(optimize({}).value == 0);
    std::mt19937 generator(42);
    for (int trial = 0; trial < 64; ++trial) {
        std::vector<Job> jobs;
        for (int i = 0; i < 8; ++i) {
            std::int64_t start = generator() % 10;
            std::int64_t end = start + 1 + generator() % 5;
            std::int64_t value = generator() % 20;
            jobs.push_back({std::to_string(i), start, end, value});
        }
        assert(optimize(jobs).value == exhaustive(jobs));
    }
    try { optimize({{"same",0,1,3},{"same",1,2,3}}); }
    catch (const std::invalid_argument&) { return 0; }
    return 1;
}
