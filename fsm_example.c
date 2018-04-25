/**********************
********* TYPES ******
***********************/
enum input_t {
	press1,
	scru1,
	scrd1
};

enum input_t input;

enum event_t {
	rxtab,
	rxgam,
	rxdet,
	rxlive,
	rxerror,
	timeout,
	rxgoal
};

enum event_t event;

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

enum state_t state;

/**********************
********* ACTIONS ******
***********************/
void exemenu() {
}

void prepareRQ() {
}

void highlight() {
}

void goal() {
}

/**********************
********* GUARDS ******
***********************/
char non_menu() {
}

char in_menu() {
}

/**********************
********* FSM ******
***********************/
void fsm() {
	switch (state) {
	case menu: 
		if ((input==press1))  {
			exemenu();
		}
		break;
	case tab: 
		if ( non_menu() &&(input==press1))  {
			prepareRQ();
			 state=request;
		}
		if ( in_menu() &&(input==press1))  {
			 state=menu;
		}
		if ((input==scru1))  {
			highlight();
		}
		if ((input==scrd1))  {
			highlight();
		}
		break;
	case gg: 
		if ( in_menu() &&(input==press1))  {
			 state=menu;
		}
		break;
	case gam: 
		if ( non_menu() &&(input==press1))  {
			prepareRQ();
			 state=request;
		}
		if ( in_menu() &&(input==press1))  {
		}
		if ((input==scru1))  {
			highlight();
		}
		if ((input==scrd1))  {
			highlight();
		}
		break;
	case request: 
		if ((event==rxtab))  {
			 state=tab;
		}
		if ((event==rxgam))  {
			 state=gam;
		}
		if ((event==rxdet))  {
			 state=det;
		}
		if ((event==rxlive))  {
			 state=live;
		}
		if ((event==rxerror))  {
			 state=error;
		}
		if ((event==timeout))  {
			 state=error;
		}
		if ((event==rxgoal))  {
			goal();
			 state=live;
		}
		break;
	}
}
void main() {
	fsm();
}
