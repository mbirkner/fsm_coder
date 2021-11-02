
/****************************************************
File created with fsm_coder python script by M.Birkner
https://github.com/mbirkner/fsm_coder.git
****************************************************/

#include "fsm.h"

enum event_t event;
enum input_t input;
enum state_t state;

/**********************
********* FSM ******
***********************/
void fsm() {
	switch (state) {
	case (menu): 
		if ((input==press1))  {
			exemenu();
		}
		break;
	case (tab): 
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
	case (gg): 
		if ( in_menu() &&(input==press1))  {
			 state=menu;
		}
		break;
	case (gam): 
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
	case (request): 
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
