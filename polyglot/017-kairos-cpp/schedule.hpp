#pragma once
#include <cstdint>
#include <string>
#include <vector>

struct Job {
    std::string id;
    std::int64_t start, end, value;
};

struct Plan {
    std::int64_t value;
    std::vector<std::string> jobs;
};

Plan optimize(std::vector<Job> jobs);
