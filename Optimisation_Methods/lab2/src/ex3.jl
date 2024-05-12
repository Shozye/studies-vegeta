# Mateusz Pełechaty, 261737
using LinearAlgebra

using JuMP
using GLPK
using Cbc

function schedule(
    T :: Matrix{Int}
)
    n, M = size(T)
    println("n: ", n)
    println("M: ", M)
    Z = collect(1:n)
    P = collect(1:M)

    model = Model(GLPK.Optimizer) # GLPK / CBC / CPLEX

    infty = sum(T[i, p] for i in Z for p in P)


    @variable(model, s[Z, P] >= 0)
    @variable(model, prec[Z, Z], Bin)
    @variable(model, ms >= 0)

    # p is a precedence matrix
    for i in Z
        for j in Z
            if i != j
                @constraint(model, prec[i, j] == 1 - prec[j, i])
            end
        end
    end

    # Every task i had to start at every processor. 
    # It is suficcient to check only the first processor
    for i in Z
        @constraint(model, s[i, 1] >= 0)
    end

    # For every i, Pi should finish task x before Pi+1 starts this task
    for p in 1:(M-1)
        for any in Z
            @constraint(model, s[any, p] + T[any, p] <= s[any, p+1])
        end
    end

    # One processor p, can execute one task at a time and 
    # if i < j, it should finish task πi before task πj .
    # This rule also ensures same order of tasks
    for p in P
        for i in Z
            for j in Z
                if i != j
                    @constraint(model, s[j, p] + infty * (1-prec[i,j]) >= s[i,p] + T[i,p])
                end
            end
        end
    end

    for i in Z
        @constraint(model, s[i, M] + T[i, M] <= ms)
    end
    @objective(model, Min, ms)

    print(model) # drukuj model
    # rozwiaz egzemplarz

    optimize!(model)

    status = termination_status(model)

    if status == MOI.OPTIMAL
        return status, objective_value(model), value.(s)
    else
        return status, nothing, nothing
    end
end

function int(x)
    return floor(Int, x)
end

function GanttDiagram( 
    T :: Matrix{ Int }, # Execution Times
    s  # Start Time
)
    n, M = size(T)
    a = ""
    
    first_processor_order = [x[2] for x in sort([(s[i, 1], i) for i in 1:n], by= x -> x[1])]

    for p in 1:M
        a *= "PROC(" * string(p) * "): "
        current_task_index = 1
        current_time = 0
        while current_task_index <= n
            task = first_processor_order[current_task_index]

            if current_time < s[task, p]
                a *= "   "
            elseif current_time == s[task, p]
                a *= " | "
            elseif current_time > s[task, p] && s[task,p] + T[task, p] > current_time
                if task < 10
                    a *= " " * string(task) * " "
                elseif task < 100
                    a *= " " * string(task)
                end
            elseif current_time == s[task,p] + T[task, p]
                a *= " | "
                current_task_index += 1
            end
            current_time += 1
        end
        a *= "\n"
    end
    return a
end

function main()
    T =  [3       3       2;
        9       3       8;
        9       8       5;
        4       8       4;
        6      10       3;
        6       3       1;
        7      10       3]       
    n, M = size(T)
    
    status, cost, x = schedule(T)
    if status == MOI.OPTIMAL
        println("the total cost: ", cost)
        println(GanttDiagram(T, x))

    else
        println("Status: ", status)
    end

end

main()