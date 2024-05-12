# Mateusz Pełechaty, 261737
using JuMP
using GLPK

function solve_problem(r::Matrix{Int}, t::Matrix{Int}, M::Int, verbose=true)

    # r[i, j] - liczba komórek pamięci potrzebna do policzenia funkcji i podprogramem j
    # t[i, j] - czas potrzebny do policzenia funkcji i podprogramem j
    # M - maksymalna liczba komórek pamięci

    n, m = size(r)
    functions = 1:n
    subprograms = 1:m

    model = Model(GLPK.Optimizer)

    # x[i, j] == 1 jeżeli funkcje i liczymy podprogramem j
    @variable(model, x[functions, subprograms], Bin) 

    # Every function must be calculated
    for i in functions
        @constraint(model, sum(x[i, j] for j in subprograms) >= 1)
    end

    # Total memory used lesser than M
    @constraint(model, sum(r[i, j] * x[i, j] for i in functions, j in subprograms) <= M)

    # Minimize total time used.
    @objective(model, Min, sum(t[i, j] * x[i, j] for i in functions, j in subprograms))


    print(model) # drukuj model
    # rozwiaz egzemplarz
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
    r = [1 2 3 99; 
         4 5 6 98; 
         7 8 9 91]

    t = [1 2 3 1;
         4 5 6 1;
         7 8 9 1]
    
    M = 20
    
    status, cost, x = solve_problem(r, t, M)
    println("status: ", status)
    println("cost: ", cost)
    println("x: ", x)

end

main()
