
/****************************************************
File created with fsm_coder python script by M.Birkner
https://github.com/mbirkner/fsm_coder.git
****************************************************/

#ifndef FSM_INC
#define FSM_INC

/**********************
********* TYPES ******
***********************/

enum input_t {
	press1,
	scru1,
	scrd1
};


extern enum input_t input;

enum event_t {
	rxtab,
	rxgam,
	rxdet,
	rxlive,
	rxerror,
	timeout,
	rxgoal
};

extern enum event_t event;

enum state_t {
	menu,
	tab,
	gg,
	gam,
	request,
	det,
	live,
	error
};
extern enum state_t state;

/**********************
********* ACTIONS ******
***********************/
void exemenu();

void prepareRQ();

void highlight();

void goal();

void fsm();
/**********************
********* GUARDS ******
***********************/

char non_menu();

char in_menu();

#endif