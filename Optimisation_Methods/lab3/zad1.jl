using JuMP, GLPK, LinearAlgebra

# Function to parse a problem instance from a file
function parse_gap_file(filename::String)
    problems = []

    open(filename, "r") do file
        content = read(file, String)
        int_strings = split(content)
        integers = parse.(Int, int_strings)

        i = 1
        num_problems = integers[i]
        i += 1
        for problem_index in 1:num_problems
            # println("Reading problem nr ", problem_index)
            m = integers[i]
            n = integers[i+1]
            i += 2
            # println("Number of machines: ", m, ", Number of jobs: ", n)

            c = []
            for machine_index in 1:m
                push!(c, integers[i: i+n])
                i += n
            end

            p = []
            for machine_index in 1:m
                push!(p, integers[i: i+n])
                i += n
            end

            T = []
            j = i
            while j < i+m
                push!(T, integers[j])
                j += 1
            end
            i = j


            push!(problems, (m, n, c, p, T))
        end
    end
    return problems
end

# Linear Programming Model for the Generalized Assignment Problem, m-maszyny, n-zadania
function solve_lp_ga(m, c, p, T, J, Mprim, zero_assignments)
    M = collect(1:m)

    model = Model(GLPK.Optimizer)
    # ustalenie zmiennej, czy job jest przypisany do maszyny
    @variable(model, 0 <= x[M, J] ) 

    # Kazde zadanie musi byc przypisane do jednej maszyny
    for j in J
        @constraint(model, sum(x[i, j] for i in M) == 1 )
    end

    # We cannot take more than T[i] time.
    for i in Mprim
        @constraint(model, sum(p[i][j] * x[i, j] for j in J) <= T[i])
    end

    # "Removed variables/edges"
    for (i,j) in zero_assignments
        if j in J
            @constraint(model, x[i,j] == 0)
        end
    end

    # Minimize costs.
    @objective(model, Min, sum(c[i][j] * x[i, j] for i in M, j in J)) 
    
    optimize!(model)
    return value.(x), objective_value(model)
end

# Iterative relaxation method
function iterative_relaxation(m, n, c, p, T)
    F = falses(m, n)
    M = collect(1:m)
    J = collect(1:n)
    Mprim = collect(1:m)

    zero_assignments = Set{Tuple{Int, Int}}()
    while !isempty(J)
        x, _ = solve_lp_ga(m, c, p, T, J, Mprim, zero_assignments)

        # Remove zero assignments krok (ii)a)
        for (i, j) in [(i, j) for i in M, j in J]
            if x[i,j] == 0
                push!(zero_assignments, (i, j))
            end
        end

        # step ii b # Removal from J
        J_removal = Set{Int}()
        for (i, j) in [(i, j) for i in M, j in J]
            if round(x[i, j], digits=15) == 1
                F[i,j] = true # F <- F U {ij}
                push!(J_removal, j)
                T[i] -= p[i][j] # Ti <- Ti - pij
            end
        end
        J = setdiff(J, J_removal) #J <- J\{j}

        # if length(J_removal) > 0
        #     println("Removed ", length(J_removal), " Jobs", J_removal)
        # end

        # step ii c # Removal from M
        M_removal = Set{Int}()
        for i in M
            degree = isempty(J) ? 0 : sum(x[i, j] > 0 for j in J)  
            if (degree == 1) || (degree == 2 && sum(x[i, :]) >= 1)
                push!(M_removal, i)
            end
        end
        # if length(M_removal) > 0
        #     println("Removed ", length(M_removal), " Machines", M_removal)
        # end

        Mprim = setdiff(Mprim, M_removal)
    end

    total_cost = sum(p[i][j] * F[i, j] for i in M, j in 1:n)
    return F, total_cost
end

# Function to evaluate the algorithm on a dataset
function evaluate_gap_dataset(file_path::String)
    problems = parse_gap_file(file_path)
    results = []
    maxratios = []

    for (m, n, c, p, T) in problems
        F, cost = iterative_relaxation(m, n, c, p, deepcopy(T))
        problem_ratios = []
        
        for i in 1:m #maszyny
            t = 0
            for j in 1:n #problemy
                t += F[i,j] * p[i][j]
            end
            push!(problem_ratios, t/T[i])
            # println("ratio for maszyne $i = $zuzycie / $(origin_capacities[i])") 
        end 

        push!(maxratios, maximum(problem_ratios))   
        push!(results, cost)
    end
    return results, maxratios
end

file_path = ARGS[1]
(results, maxratios) = evaluate_gap_dataset(file_path)

for i in 1:length(maxratios)
    println("Problem $i: MaxRatio ti/Ti: $(maxratios[i]): Result: $(results[i])")
end
