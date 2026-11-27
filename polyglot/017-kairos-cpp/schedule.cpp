#include "schedule.hpp"
#include <algorithm>
#include <stdexcept>
#include <tuple>
#include <unordered_set>

Plan optimize(std::vector<Job> jobs) {
    if (jobs.size() > 200000) throw std::invalid_argument("too many jobs");
    std::unordered_set<std::string> ids;
    for (const auto& job : jobs) {
        if (job.id.empty() || !ids.insert(job.id).second || job.start < 0 ||
            job.end <= job.start || job.value < 0 || job.value > 1000000000)
            throw std::invalid_argument("invalid or duplicate job");
    }
    std::sort(jobs.begin(), jobs.end(), [](const Job& a, const Job& b) {
        return std::tie(a.end, a.start, a.id) < std::tie(b.end, b.start, b.id);
    });
    std::vector<std::int64_t> ends, best(jobs.size() + 1);
    std::vector<std::size_t> predecessor(jobs.size());
    std::vector<bool> selected(jobs.size());
    ends.reserve(jobs.size());
    for (std::size_t i = 0; i < jobs.size(); ++i) {
        predecessor[i] = std::upper_bound(ends.begin(), ends.end(), jobs[i].start) - ends.begin();
        auto value = jobs[i].value + best[predecessor[i]];
        selected[i] = value > best[i];
        best[i+1] = selected[i] ? value : best[i];
        ends.push_back(jobs[i].end);
    }
    Plan plan{best.back(), {}};
    for (std::size_t i = jobs.size(); i > 0;) {
        --i;
        if (selected[i]) {
            plan.jobs.push_back(jobs[i].id);
            i = predecessor[i];
        }
    }
    std::reverse(plan.jobs.begin(), plan.jobs.end());
    return plan;
}
