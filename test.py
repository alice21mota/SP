from datetime import timedelta
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
tests_order = []

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

def read_input_file(input_file):
    """Reads the input data from the file and parses it into a suitable format."""
    with open(input_file, 'r') as file:
        data = file.readlines()

    parse_input_file(data)
    return data

def parse_input_file(data):
    """Parses the input data into a suitable format."""

    global num_machines
    global num_resources
    global num_tests
    
    for line in data:
        if line.startswith('%'):
            match = re.search(r'\d+', line)
            initial_info.append(int(match.group()))

        else:
            num_machines = initial_info[1]
            parse_test_data(line)
            
    num_tests = initial_info[0]
    num_resources = initial_info[2]

    process_tests()
    return

def parse_test_data(line):
    # Regular expressions to capture test data
    test_pattern = re.compile(r"test\(\s*'(\w+)',\s*(\d+),\s*\[(.*?)\],\s*\[(.*?)\]\)")

    match = test_pattern.match(line)    # Match test data

    if match:
        test_id = match.group(1)
        duration = int(match.group(2))
        # Convert machine list to integers
        machines = set(int(m.strip().strip("'\"")[1:]) for m in match.group(3).split(',') if m)
        # Convert resource list to integers
        resources = set(int(r.strip().strip("'\"")[1:]) for r in match.group(4).split(',') if r)
        
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

def calculate_min_time():
    # Calculate min_time as the maximum sum of durations of tests that use the same resources
    resource_groups = {}
    for i, resource_set in enumerate(required_resources):
        for resource in resource_set:
            if resource not in resource_groups:
                resource_groups[resource] = 0
            resource_groups[resource] += durations[i]

    return max(resource_groups.values())

def process_tests():
    tests.sort(key=lambda x: x['resources'], reverse=True)
    # tests.sort(key=lambda x: x['machines'], reverse=True)
    # Extract test data into separate lists
    for test in tests:
        duration = test['duration']
        machines = set(test['machines'])
        resources = set(test['resources'])
        test_id = test['test_id'].lstrip('t')

        durations.append(duration)

        if machines == set(): 
            available_machines.append(all_machines)
        else: 
            available_machines.append(machines)
        
        required_resources.append(resources)
        tests_order.append(int(test_id))
    
    print("tests_order: ", tests_order)

    global max_time, min_time 
    max_time = sum(durations)
    min_time = calculate_min_time()

def solve_problem(makespan, remaining_time):
    print("remaining: ", remaining_time)
    model = minizinc.Model("model.mzn")
    solver = minizinc.Solver.lookup("highs")
    instance = minizinc.Instance(solver, model)

    instance["num_tests"] = num_tests
    instance["max_time"] = makespan
    instance["min_time"] = min_time
    instance["num_machines"] = num_machines
    instance["num_resources"] = num_resources
    instance["duration"] = durations
    instance["required_resources"] = required_resources
    instance["available_machines"] = available_machines



    result = instance.solve(free_search=True, timeout=timedelta(seconds=remaining_time))
    return result

def binary_search_makespan(start_time):
    low = min_time
    high = max_time
    optimal_result = None
    time_limit = 299  # Set to 5 minutes

    while low <= high:
        # Check elapsed time
        elapsed_time = time.time() - start_time
        print(f"Elapsed time__: {elapsed_time:.2f} seconds")
        if time.time() - start_time > time_limit:
            print("Time limit exceeded. Terminating search.")
            break
        mid = (low + high) // 2
        print(f"Low: {low}, High: {high}", "Mid: ", mid)
        print(f"Trying makespan: {mid}")

        remaining_time = time_limit - elapsed_time  # Calculate remaining time
        print(f"Remaining time: {remaining_time:.2f} seconds")
        result = solve_problem(mid, remaining_time)

        if result and result is not None:
            print(f"Found makespan: {mid}")
            print(result)
            optimal_result = result
            high = min(optimal_result["makespan"] - 1, mid-1)  # Try smaller makespan
            #high = mid - 1  # Try smaller makespan
        else:
            low = mid + 1  # Try larger makespan

    return optimal_result

def get_output(result):
    makespan_obtained = result["makespan"]
    print(f"Obtained makespan: {makespan_obtained}")
    starts = result["start_times"]
    print(f"Start times: {starts}")
    machines_selected = result["selected_machine"]
    print(f"Machines selected: {machines_selected}")

    # Create a list of tuples (test_number, start_time, machine_selected)
    test_info = [(tests_order[i], starts[i], machines_selected[i], required_resources[i]) for i in range(len(starts))]
    print("test_info: ", test_info)
    
    # Sort the list of tuples by test_number
    test_info.sort(key=lambda x: x[0])
    print("Sorted test_info: ", test_info)

    # Extract the sorted start times and machines selected
    sorted_starts = [info[1] for info in test_info]
    print("Sorted start times: ", sorted_starts)
    sorted_machines_selected = [info[2] for info in test_info]
    ordered_resources = [info[3] for info in test_info]
    print("Sorted machines selected: ", sorted_machines_selected)

    return format_output(makespan_obtained, sorted_starts, sorted_machines_selected, ordered_resources)

def format_output(makespan, start_times, selected_machine, ordered_resources):
    machine_assignments = {}

    # Group tests by machine
    for i, machine in enumerate(selected_machine):
        test_id = f"t{i+1}"
        start_time = start_times[i]
        # res = required_resources[i] if required_resources[i] != set() else []
        
        # # If no resources provided, assign empty list
        res = ordered_resources[i] if ordered_resources and i < len(ordered_resources) else []
        
        if machine not in machine_assignments:
            machine_assignments[machine] = []
        machine_assignments[machine].append((test_id, start_time, res))

    # Format the output string
    output_str = f"% Makespan : {makespan}\n"
    for machine, tests in sorted(machine_assignments.items()):
        formatted_tests = ", ".join([f"(\'{test[0]}\',{test[1]}" + (f",[{','.join([f'\'r{r}\'' for r in test[2]])}]" if test[2] else "") + ")" for test in tests])
        output_str += f"machine( \'m{machine}\', {len(tests)}, [{formatted_tests}])\n"

    print(output_str)

    return output_str  

def main():
    start_time = time.time()

    check_command_line_arguments()
    read_input_file(sys.argv[1])

    output_file = sys.argv[2]
    
    result = binary_search_makespan(time.time())

    with open(output_file, 'w') as file:
        if result:
            file.write(str(get_output(result)) + "\n")

        else:
            file.write("No solution found.\n")
        
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    with open(output_file, 'a') as file:
        file.write(f"Elapsed time: {elapsed_time:.2f} seconds\n")
    print(f"Elapsed time: {elapsed_time:.2f} seconds") 

if __name__ == "__main__":
    main()
