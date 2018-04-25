# fsm_coder
a python script which converts a transition table (xlsx) to c code

See Example.xlsx  to understand how to define a transition table from one state (state1) to another state (next state) under 
certain conditions (inputs, guards, events).Instead of changing a state one may just execute an action.
type definitions, guard and action function skeletons, as well as a simple fsm (switch statement) is created in C.

I use this script for simple AVR state machines to create the behavioural framework before starting coding.


ToDos:
command line args for script
