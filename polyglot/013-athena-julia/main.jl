include("Athena.jl")

function main(args)
    length(args) == 3 || throw(ArgumentError("usage: julia main.jl N PROBABILITY SEED"))
    result = @timed Athena.estimate(parse(Int, args[1]), parse(Float64, args[2]), parse(Int, args[3]))
    println(result.value)
    println("seconds (including first-call compilation): ", result.time)
end

try
    main(ARGS)
catch error
    showerror(stderr, error)
    println(stderr)
    exit(2)
end
