module Athena
using Random

function estimate(n::Int, p::Float64, seed::Int)
    2 <= n <= 10^7 || throw(ArgumentError("n outside 2..10000000"))
    0 < p < 1 || throw(ArgumentError("expected 0 < p < 1"))
    seed >= 0 || throw(ArgumentError("seed must be nonnegative"))
    rng = MersenneTwister(seed)
    hits = count(_ -> rand(rng) < p, 1:n)
    rate = hits / n
    z = 1.959963984540054
    factor = 1 + z^2 / n
    center = (rate + z^2 / (2n)) / factor
    radius = z * sqrt(rate * (1 - rate) / n + z^2 / (4n^2)) / factor
    return (; n, hits, rate, lower=max(0.0, center-radius), upper=min(1.0, center+radius))
end
end
