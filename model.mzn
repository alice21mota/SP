include "cumulative.mzn";

% Define the problem parameters
int: num_tests;
int: num_machines;
int: num_resources;
int: max_time;
int: min_time;

array[1..num_tests] of int: duration;
array[1..num_tests] of set of int: available_machines;
array[1..num_tests] of set of int: required_resources;

% Variables
array[1..num_tests] of var 0..max_time: start_times;
array[1..num_tests] of var 1..num_machines: selected_machine;
var min_time..max_time: makespan;

% Calculate makespan directly
constraint makespan = max([start_times[t] + duration[t] | t in 1..num_tests]);

% Ensure each test starts on a valid machine and finishes within the makespan
constraint 
  forall(t in 1..num_tests)( 
    selected_machine[t] in available_machines[t]
  );

% No overlapping tests on the same machine
constraint 
  forall(t1, t2 in 1..num_tests where t1 < t2)(
    selected_machine[t1] == selected_machine[t2] ->
    (start_times[t1] + duration[t1] <= start_times[t2] \/ 
      start_times[t2] + duration[t2] <= start_times[t1])
  );

% No overlapping tests on the same resource (cumulative constraint)
constraint 
  forall(r in 1..num_resources)(
    cumulative([start_times[t] | t in 1..num_tests where r in required_resources[t]],
               [duration[t] | t in 1..num_tests where r in required_resources[t]],
               [1 | t in 1..num_tests where r in required_resources[t]], 1)
  );

solve :: seq_search([
  int_search(selected_machine, first_fail, indomain_random),
  int_search(start_times, input_order, indomain_min)
]) minimize makespan;

% %Output
output [
  "Makespan: ", show(makespan), "\n",
  "Start times: ", show(start_times), "\n",
  "duration: ", show(duration ), "\n",
  "Selected machines: ", show(selected_machine), "\n"
];