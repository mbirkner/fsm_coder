# fsm_coder
a python script which converts a transition table (xlsx) to c code

See Example.xlsx  to understand how to define a transition table from one state (state1) to another state (next state) under 
certain conditions (inputs, guards, events).Instead of changing a state one may just execute an action.
type definitions, guard and action function skeletons, as well as a simple fsm (switch statement) is created in C.

I use this script for simple AVR state machines to create the behavioural framework before starting coding.


Usage:
$./fsm.py -i inputfile -o outputfile
where inputfile (w/o extension) is the name of the xlsx file with a "Transition" sheet containing the transition table shown in the example. The table headings need to be present(state1,input,guard,action, next state)!
outputfile(w/o extension) is the name of the .c file which is created by the script.
