import sys
import minizinc
import re
import time

tests = []
durations = []
required_resources = []
available_machines = []
all_machines = set()
num_machines = 0
num_resources = 0
num_tests = 0
initial_info = []
min_time = 0
max_time = 0

def read_input_file(input_file):
    """Reads the input data from the file and parses it into a suitable format."""
    with open(input_file, 'r') as file:
        data = file.readlines()
        #Parse the input TODO

    print(int(data[0].split(':')[-1]))
    parse_input_file(data)
    return data


def parse_input_file(data):
    """Parses the input data into a suitable format."""

    global num_machines
    global num_resources
    global num_tests
    
    # initial_info = [] #will store number of tests [0], number of machines [1], number of resources [2], makespan [3]
    for line in data:
        #print(line)
        if line.startswith('%'):
            match = re.search(r'\d+', line)
            initial_info.append(int(match.group()))
            

        else:
            # print(initial_info)
            num_machines = initial_info[1]
            parse_test_data(line)  #parse test data
            
    num_tests = initial_info[0]
    num_resources = initial_info[2]

    process_tests()

    return

def parse_test_data(line):
    # Regular expressions to capture test data - going to be used ahead
    test_pattern = re.compile(r"test\(\s*'(\w+)',\s*(\d+),\s*\[(.*?)\],\s*\[(.*?)\]\)")

    match = test_pattern.match(line)    # Match test data

    if match:
        test_id = match.group(1)
        duration = int(match.group(2))
        # Convert machine list to integers, stripping any extraneous characters
        machines = set(int(m.strip().strip("'\"")[1:]) for m in match.group(3).split(',') if m)
        # Convert resource list to integers, stripping any extraneous characters
        resources = set(int(r.strip().strip("'\"")[1:]) for r in match.group(4).split(',') if r)
        # print(test_id)
        
    # Append test data as dictionary
        tests.append({
            'test_id': test_id,
            'duration': duration,
            'machines': machines,
            'resources': resources
        })

    for i in range(1, num_machines + 1):
        all_machines.add(i)
    
    return tests

def process_tests():
    tests.sort(key=lambda x: x['resources'], reverse=True)
    tests.sort(key=lambda x: x['machines'], reverse=True)
    
    # tests.sort(key=lambda x: x['resources'], reverse=True)
    # tests.sort(key=lambda x: x['duration'])
    for test in tests:
        duration = test['duration']
        machines = set(test['machines'])
        resources = set(test['resources'])

        durations.append(duration)

        if machines == set(): 
            available_machines.append(all_machines)
        else: 
            available_machines.append(machines)
        
        required_resources.append(resources)

    global max_time 
    max_time = sum(durations)
    global min_time 
    min_time = max(durations)

def check_command_line_arguments():
    print(sys.argv)
    if len(sys.argv) != 3:
        print("Incorrect input format. Expected 3 arguments, got", len(sys.argv), ".\n")
        sys.exit(1)

    if (sys.argv[1].split('.')[-1] != "txt" or sys.argv[2].split('.')[-1] != "txt"):
        print("Input and output files must be text files.\n")
        sys.exit(1)
    
    if (sys.argv[1] == sys.argv[2]):
        print("Input and output files cannot be the same.\n")
        sys.exit(1)
    
    else: print ("Input and output files are valid.\n")
    

def solve_problem():
    model = minizinc.Model("model.mzn")
    #model.add_file("model.mzn")

    solver = minizinc.Solver.lookup("highs")
    instance = minizinc.Instance(solver, model)

    instance["num_tests"] = num_tests
    instance["num_machines"] = num_machines
    instance["num_resources"] = num_resources
    instance["max_time"] = max_time
    instance["min_time"] = min_time
    instance["duration"] = durations
    instance["required_resources"] = required_resources
    instance["available_machines"] = available_machines

    # print(f"max_time: {max_time}")
    # print(f"min_time: {min_time}")
    # print(f"num_tests: {num_tests}")
    # print(f"num_machines: {num_machines}")
    # print(f"num_resources: {num_resources}")
    # print(f"duration: {durations}")
    # print(f"required_resources: {required_resources}")
    # print(f"available_machines: {available_machines}")


    result = instance.solve()
    print(f"Solution: {result}")



def main():
    start_time = time.time()

    check_command_line_arguments()
    read_input_file(sys.argv[1])

    output_file = sys.argv[2]
    
    solution = solve_problem()

    with open(output_file, 'w') as file:
        file.write("Solution " + str(solution) + ";\n")

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")  # Print the elapsed time


if __name__ == "__main__":
    main()
