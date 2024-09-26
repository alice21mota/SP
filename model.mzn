% Define the problem parameters
int: num_tests;            % Number of tests
int: num_machines;         % Number of machines
int: num_resources;        % Number of resources
int: max_time;
int: min_time;

array[1..num_tests] of int: duration;                      % Duration of each test
array[1..num_tests] of set of int: available_machines;     % Available machines for each test
array[1..num_tests] of set of int: required_resources;      % Resources required for each test

% Variables
array[1..num_tests] of var 0..max_time: start_times;       % Start time for each test
array[1..num_tests] of var 1..num_machines: selected_machine; % Selected machine for each test
var int: makespan;                                          % The makespan, which we aim to minimize

% Constraint: Ensure all tests finish within the makespan and select valid machines
constraint makespan <= max_time;
%constraint makespan >= min_time;

constraint 
  forall(t in 1..num_tests)(
    start_times[t] + duration[t] <= makespan /\
    selected_machine[t] in available_machines[t]
  );

% Constraint: No overlapping tests on the same machine
constraint 
  forall(t1, t2 in 1..num_tests where t1 < t2)(
    selected_machine[t1] == selected_machine[t2] -> 
    (start_times[t1] + duration[t1] <= start_times[t2]) \/
    (start_times[t2] + duration[t2] <= start_times[t1])
  );

% Constraint: No overlapping resource usage for tests requiring the same resource
constraint 
  forall(r in 1..num_resources)(
    let {
      array[1..num_tests] of var 0..1: test_resources = 
        [if r in required_resources[t] then 1 else 0 endif | t in 1..num_tests]
    } in
    sum(t in 1..num_tests where test_resources[t] == 1)(
      start_times[t] + duration[t]
    ) <= makespan
  );

% Objective: Minimize makespan
solve minimize makespan;

% Output
output [
  "Makespan: ", show(makespan), "\n",
  "Start times: ", show(start_times), "\n",
  "Selected machines: ", show(selected_machine), "\n"
];