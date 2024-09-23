import sys
#import minizinc
import re

tests = []
durations = []
required_resources = []
available_machines = []
all_machines = set()

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
    
    initial_info = [] #will store number of tests [0], number of machines [1], number of resources [2], makespan [3]
    for line in data:
        #print(line)
        while line.startswith('%'):
            match = re.search(r'\d+', line)
            initial_info.append(int(match.group()))
            break
        
        parsed_tests = parse_test_data(line)  #parse test data
            

    num_tests = initial_info[0]
    num_machines = initial_info[1]
    num_resources = initial_info[2]

    return

def parse_test_data(line):
    # Regular expressions to capture test data - going to be used ahead
    test_pattern = re.compile(r"test\(\s*'(\w+)',\s*(\d+),\s*\[(.*?)\],\s*\[(.*?)\]\)")

    match = test_pattern.match(line)    # Match test data

    if match:
        test_id = match.group(1)
        duration = int(match.group(2))
        # machines = [m.strip() for m in match.group(3).split(',') if m]  # Clean machine list
        # resources = [r.strip() for r in match.group(4).split(',') if r] # Clean resource list   
        # Convert machine list to integers, stripping any extraneous characters
        machines = [int(m.strip().strip("'\"")[1:]) for m in match.group(3).split(',') if m]
        # Convert resource list to integers, stripping any extraneous characters
        resources = [int(r.strip().strip("'\"")[1:]) for r in match.group(4).split(',') if r]
        # print(test_id)

    
        
    # Append test data as dictionary
        tests.append({
            'test_id': test_id,
            'duration': duration,
            'machines': machines,
            'resources': resources
        })
        durations.append(duration)
        available_machines.append(machines)
        required_resources.append(resources)

    
    for i in range(1, len(available_machines) + 1):
        all_machines.add(i)
    
    return tests

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
    


def main():
    # if len(sys.argv) != 3:
    #     print("Incorrect input format. Expected: python proj.py <input-file-name> <output-file-name>")
    #     sys.exit(1)
    
    # print(sys.argv)

    # input_file = sys.argv[1]
    # output_file = sys.argv[2]

    # print("Input file:", input_file)
    # print("Output file:", output_file)

    check_command_line_arguments()
    read_input_file(sys.argv[1])

    # # Read and process input data
    # input_data = read_input_file(input_file)

    # # Solve the CSP problem
    # solution = solve_csp(input_data)

    # # Write the solution to the output file
    # write_output_file(output_file, solution)

    output_file = sys.argv[2]

    with open(output_file, 'w') as file:
        file.write("Number of Tests: " + str(len(tests)) + "\n\n")
        file.write("Number of Machines: " + str(len(available_machines)) + "\n\n")
        file.write("All Machines: " + str(all_machines) + "\n\n")
        file.write("Number of Resources: " + str(len(required_resources)) + "\n\n")
        file.write("Durations: " + str(durations) + "\n")
        file.write("Required Resources: " + str(required_resources) + "\n")
        file.write("Available Machines: " + str(available_machines) + "\n")


if __name__ == "__main__":
    main()
