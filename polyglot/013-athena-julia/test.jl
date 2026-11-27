using Test
include("Athena.jl")
@testset "Bernoulli Monte Carlo" begin
    a = Athena.estimate(10_000, 0.4, 42)
    @test a == Athena.estimate(10_000, 0.4, 42)
    @test abs(a.rate - 0.4) < 0.02
    @test 0 < a.lower < a.rate < a.upper < 1
    @test_throws ArgumentError Athena.estimate(1, 0.4, 42)
    @test_throws ArgumentError Athena.estimate(10, NaN, 42)
end
