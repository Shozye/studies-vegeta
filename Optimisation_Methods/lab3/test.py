optimal_values = [
    "c515-1  336",
    "c520-1  434",
    "c525-1  580",
    "c530-1  656",
    "c515-2  327",
    "c520-2  436",
    "c525-2  564",
    "c530-2  644",
    "c515-3  339",
    "c520-3  420",
    "c525-3  573",
    "c530-3  673",
    "c515-4  341",
    "c520-4  419",
    "c525-4  570",
    "c530-4  647",
    "c515-5  326",
    "c520-5  428",
    "c525-5  564",
    "c530-5  664",
    "c824-1  563",
    "c832-1  761",
    "c840-1  942",
    "c848-1  1133",
    "c824-2  558",
    "c832-2  759",
    "c840-2  949",
    "c848-2  1134",
    "c824-3  564",
    "c832-3  758",
    "c840-3  968",
    "c848-3  1141",
    "c824-4  568",
    "c832-4  752",
    "c840-4  945",
    "c848-4  1117",
    "c824-5  559",
    "c832-5  747",
    "c840-5  951",
    "c848-5  1127",
    "c1030-1  709",
    "c1040-1  958",
    "c1050-1  1139",
    "c1060-1  1451",
    "c1030-2  717",
    "c1040-2  963",
    "c1050-2  1178",
    "c1060-2  1449",
    "c1030-3  712",
    "c1040-3  960",
    "c1050-3  1195",
    "c1060-3  1433",
    "c1030-4  723",
    "c1040-4  947",
    "c1050-4  1171",
    "c1060-4  1447",
    "c1030-5  706",
    "c1040-5  947",
    "c1050-5  1171",
    "c1060-5  1446"
]

name_to_gap = {
    "c515": "gap1",
    "c520": "gap2",
    "c525": "gap3",
    "c530": "gap4",
    "c824": "gap5",
    "c832": "gap6",
    "c840": "gap7",
    "c848": "gap8",
    "c1030": "gap9",
    "c1040": "gap10",
    "c1050": "gap11",
    "c1060": "gap12",
}

my_data = {}

with open("out/out.out", 'r') as file:
    data = file.read()


for file_with_problem in data.split("file "):
    lines = file_with_problem.split("\n")
    
    filename = lines[0]
    if filename != '':
        my_data[filename] = []
    
    for line in lines[1:-1]:
        splitted = line.split(" ")
        problem_num = splitted[1][:-1]
        maxRatio = splitted[4][:-1]
        CostValue = splitted[6]
        
        my_data[filename].append((problem_num, maxRatio, CostValue))


def do_line(filename, problem_number, optimal_value, approximation_cost_value, max_ratio):
    if optimal_value == -1:
        optimal_value = "---"
        
    optimal_ratio = "---" if optimal_value == "---" else round(float(approximation_cost_value) / float(optimal_value), 4)
    return f"{problem_number} & {round(float(max_ratio), 4)} & {approximation_cost_value} & {optimal_value} & {optimal_ratio}\\\\ \\hline" 

def do_latex_table(table, filename):
    table_beginning = r"""
    \begin{table}[]
    \caption{"""+f"Tests on file {filename}"+r"""}
    \centering
    \begin{tabular}{llllll}
    Problem no. & Max Time Ratio & Approx Cost Val  & Opt Val & Val Ratio \\ """ + table + r"""\end{tabular}
    \end{table}
    """
    return table_beginning

def do_table(filename: str):
    data = my_data[filename]
    table_lines = ""
    for (problem_no, maxratio, costvalue) in data:
        
        optimal_value = -1
        for opt in optimal_values:
            filename_problem, val = opt.split("  ")
            weird_filename, prob = filename_problem.split("-")
            weird_filename_to_normal = name_to_gap[weird_filename] + ".txt"
            if weird_filename_to_normal == filename and prob == problem_no:
                optimal_value = val
        
        table_lines += do_line(filename, problem_no, optimal_value, costvalue, maxratio) + "\n"
    return table_lines



for filename in my_data:
    print(do_latex_table(do_table(filename), filename))
