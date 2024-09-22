% Define the problem parameters
int: num_tests;    % Number of tests
int: num_machines; % Number of machines
int: num_resources;% Number of resources
int: max_time;

array[1..num_tests] of int: duration;  % Duration of each test
array[1..num_tests] of set of int: available_machines; % Available machines for each test
array[1..num_tests] of set of int: required_resources; % Resources required for each test

% Variables
array[1..num_tests] of var 0..max_time: start_times;  % Start time for each test
array[1..num_tests] of var 1..num_machines: selected_machine; % Selected machine for each test
var int: makespan;  % The makespan, which we aim to minimize

% Constraints
constraint
  forall(t in 1..num_tests)(
    start_times[t] + duration[t] <= makespan % Ensure that all tests finish within the makespan
  )
  /\
  % Ensure that the machine selected for the test is one of the available machines
  forall(t in 1..num_tests)(
    selected_machine[t] in available_machines[t]
  )
  /\
  % Enforce that no two tests overlap on the same machine
  forall(m in 1..num_machines)(
    forall(t1, t2 in 1..num_tests where t1 < t2)(
      if selected_machine[t1] == m /\ selected_machine[t2] == m then
        (start_times[t1] + duration[t1] <= start_times[t2]) \/
        (start_times[t2] + duration[t2] <= start_times[t1])
      else
        true
      endif
    )
  )
  /\
  % Ensure that no two tests overlap on the same resource
  forall(r in 1..num_resources)(
    forall(t1, t2 in 1..num_tests where t1 < t2)(
      if (r in required_resources[t1]) /\ (r in required_resources[t2]) then
        (start_times[t1] + duration[t1] <= start_times[t2]) \/
        (start_times[t2] + duration[t2] <= start_times[t1])
      else
        true
      endif
    )
  );

% Objective
solve minimize makespan;

% Output
output [
  "Makespan: ", show(makespan), "\n",
  "Start times: ", show(start_times), "\n",
  "Selected machines: ", show(selected_machine), "\n"
];
