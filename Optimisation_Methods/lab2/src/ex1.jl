# Mateusz Pełechaty, 261737

using LinearAlgebra

using JuMP
using GLPK
using Cbc

function almostMinCostFlow(
    B :: Vector{Int}, # Blue Vertices
    R :: Vector{Int}, # Red Vertices
    T :: Vector{Int}, # Cost of edge (s, b)
    q :: Matrix{Int},
    verbose :: Bool
)
    n = length(B)
    m = length(R)	
    model = Model(Cbc.Optimizer) # GLPK / CBC / CPLEX

    @variable(model, x[B] >= 0)

    # For any r in R, r was has connection to blue picked vertice
    for r in R
        @constraint(model, sum(q[b, r] * x[b] for b in B) >= 1)
    end
    @objective(model, Min, sum(T[b] * x[b] for b in B))

    
    print(model) 

    if verbose
        optimize!(model)
    else
        set_silent(model)
        optimize!(model)
        unset_silent(model)
    end

    status = termination_status(model)

    if status == MOI.OPTIMAL
        return status, objective_value(model), value.(x)
    else
        return status, nothing, nothing
    end


end



function main()
    BlueVertices = collect(1:7)
    RedVertices = collect(1:3)
    TimeCosts = collect(1:7)

    Connections = [
      # 1 2 3
        1 0 0;
        1 0 0;
        1 0 0;
        0 1 0;
        0 1 0;
        0 1 0;
        0 1 1;
    ]

    status, cost, x = almostMinCostFlow(
        BlueVertices, # B, 
        RedVertices, # R, 
        TimeCosts, # T, 
        Connections, # q,
        true
    )
    println("status: ", status)
    println("cost: ", cost)
    println("x: ", x)

end

main()