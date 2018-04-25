#!/usr/bin/python
from __future__ import print_function
import pandas as pd
import sys

def create_enums(H):
    print ("/**********************")
    print ("********* TYPES ******")
    print ("***********************/")
    print
    P=H['input'].unique()
    ni = len(P)-1
    print ("enum input_t {")
    for x in P:
        x=str(x)
        k=""
        if not x=="nan":
            k="\t"+x.strip()
            ni-=1
            if ni>0: k+=","
            print(k)
    print("};")
    print()
    print("enum input_t input;")
    print()
    P=H['event'].unique()
    ni = len(P)-1
    print ("enum event_t {")
    for x in P:
        x=str(x)
        k=""
        if not x=="nan":
            k="\t"+x.strip()
            ni-=1
            if ni>0: k+=","
            print(k)
    print("};")
    print()
    print("enum event_t event;")
    print()

    P=H['state1'].append(H['next state'])
    P=P.unique()
    ni = len(P)
    print ("enum state_t {")
    for x in P:
        x=str(x)
        k=""
        if not x=="nan":
            k="\t"+x.strip()
            ni-=1
            if ni>0: k+=","
            print(k)
    print("};")
    print()
    print("enum state_t state;")
    print()

    
    
def create_actions(H):
    print( "/**********************")
    print ("********* ACTIONS ******")
    print ("***********************/")
    print
    P=H['action'].unique()
    for a in P:
        a=str(a)
        if  a=='nan':
            continue
        print ("void "+a.strip()+"() {")
        print ("}")
        print()
        
def create_guards(H):
    print ("/**********************")
    print ("********* GUARDS ******")
    print ("***********************/")
    print
    P=H['guard'].unique()
    for a in P:
        a=str(a)
        if  a=='nan':
            continue
        print("char "+a.strip()+"() {")
        print("}")
        print()

        
def create_fsmfun(H):
    print( "/**********************")
    print ("********* FSM ******")
    print ("***********************/")
    print

    states1 = H['state1'].unique()

    print ("void fsm() {")

    print ("\tswitch (state) {")


    for s in states1:
        print ("\tcase "+s+": ")
        P=H[H['state1']==s]
        #print P
        nc=0
        for i,x in P.iterrows():
          #  print x
            R=3*[False]
            nc=0
            e=str(x['event'])
            if not e=='nan':
                R[0]=True
                nc+=1
            g=str(x['guard'])
            if not g=='nan':
                R[1]=True
                nc+=1
            j=str(x['input'])
            if not j=='nan':
                R[2]=True
                nc+=1
            if nc==0:
                raise("state transition for  needs to have at least 1 condition.")
            a=str(x['action'])
            n=str(x['next state'])
            #print e,g,j,a,n
            k=""
            if R[0]:
                k+="(event=="+e+")"
                nc-=1
                if nc>0: k+="&&"
            if R[1]:
                k+=" "+g.strip()+"() " 
                nc-=1
                if nc>0: k+="&&"
            if R[2]:
                k+="(input=="+j+")" 
                
            #print k
            print ("\t\tif ("+k+")  {")
            if not a=='nan':
                print ('\t\t\t'+a.strip()+"();")
            if not n=='nan':
                if not n==s:
                    print("\t\t\t state="+n+";")
                print ('\t\t}')
                
        print("\t\tbreak;")
        
    print("\t}")                     
    print("}")

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('-i','--inp',default=False, help='input xlsx file containing the transition table')
    parser.add_argument('-o','--out',default=False, help='output .c-file containing the FSM code')
    args=parser.parse_args()
    sys.stdout = open(args.out+".c", "w")
    H=pd.read_excel(args.inp+'.xlsx',"Transition")
    print(
"""
/****************************************************
File created with fsm_coder python script by M.Birkner
https://github.com/mbirkner/fsm_coder.git
****************************************************/

""")
    create_enums(H)
    create_actions(H)
    create_guards(H)
    create_fsmfun(H)
    print(
"""
void main() {
        while(1) {
            fsm();
        }
}""")
    sys.stdout.close()


if __name__=='__main__':
    main()

