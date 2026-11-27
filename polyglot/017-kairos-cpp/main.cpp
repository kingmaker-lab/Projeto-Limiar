#include "schedule.hpp"
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <utility>

int main() {
    std::vector<Job> jobs;
    std::string line;
    try {
        while (std::getline(std::cin, line)) {
            if (line.empty()) continue;
            Job job;
            std::string extra;
            std::istringstream row(line);
            if (!(row >> job.id >> job.start >> job.end >> job.value) || row >> extra)
                throw std::invalid_argument("expected ID START END VALUE");
            if (jobs.size() == 200000) throw std::invalid_argument("too many jobs");
            jobs.push_back(job);
        }
        if (!std::cin.eof()) throw std::runtime_error("failed to read input");
        auto plan = optimize(std::move(jobs));
        std::cout << "value=" << plan.value << '\n';
        for (const auto& id : plan.jobs) std::cout << id << '\n';
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}
