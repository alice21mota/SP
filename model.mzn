% Define the problem parameters
int: num_tests;            % Number of tests
int: num_machines;         % Number of machines
int: num_resources;        % Number of resources
int: max_time;             % Maximum allowable makespan
% Tighter bounds for makespan: the lower bound is the sum of durations divided by the number of machines

%int: min_time;             % Minimum allowable makespan (not used directly)

array[1..num_tests] of int: duration;                      % Duration of each test
array[1..num_tests] of set of int: available_machines;     % Available machines for each test
array[1..num_tests] of set of int: required_resources;      % Resources required for each test

% Variables
array[1..num_tests] of var 0..max_time: start_times;       % Start time for each test
array[1..num_tests] of var 1..num_machines: selected_machine; % Selected machine for each test
var int: makespan;                                          % The makespan, which we aim to minimize
var int: min_time = ceil(sum(duration) / num_machines);

% Constraint: Ensure all tests finish within the makespan and select valid machines
constraint makespan <= max_time;
constraint makespan >= min_time;


% nooverlap
predicate no_overlap(var int:s1, int:d1, var int:s2, int:d2) =
    s1 + d1 <= s2 \/ s2 + d2 <= s1;

% Ensure each test starts on a valid machine
constraint 
  forall(t in 1..num_tests)(
    selected_machine[t] in available_machines[t] /\
    start_times[t] + duration[t] <= makespan
  );

% Constraint: No overlapping tests on the same machine
constraint 
  forall(t1, t2 in 1..num_tests where t1 < t2)(
    selected_machine[t1] == selected_machine[t2] -> 
    no_overlap(start_times[t1], duration[t1], start_times[t2], duration[t2])
  );

constraint
  forall(r in 1..num_resources, t1, t2 in 1..num_tests where t1 < t2)(
    (r in required_resources[t1] /\ r in required_resources[t2]) ->
    no_overlap(start_times[t1], duration[t1], start_times[t2], duration[t2])
  );


% Objective: Minimize makespan
solve minimize makespan;

% Output
output [
  "Makespan: ", show(makespan), "\n",
  "Start times: ", show(start_times), "\n",
  "Selected machines: ", show(selected_machine), "\n"
];
