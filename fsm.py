#!python
from __future__ import print_function
import pandas as pd
import sys

def create_enums(H,fout):
    print ("/**********************",file=fout)
    print ("********* TYPES ******",file=fout)
    print ("***********************/",file=fout)
    print(file=fout)
    P=H['input'].append(H['post input']).unique()
    ni = len(P)-1
    print ("enum input_t {",file=fout)
    for x in P:
        x=str(x)
        k=""
        if not x=="nan":
            k="\t"+x.strip()
            ni-=1
            if ni>0: k+=","
            print(k,file=fout)
    print("};",file=fout)
    print("\n",file=fout)
    print("extern enum input_t input;",file=fout)
    print(file=fout)
    P=H['event'].append(H['post event']).unique()
    ni = len(P)-1
    print ("enum event_t {",file=fout)
    for x in P:
        x=str(x)
        k=""
        if not x=="nan":
            k="\t"+x.strip()
            ni-=1
            if ni>0: k+=","
            print(k,file=fout)
    print("};",file=fout)
    print(file=fout)
    print("extern enum event_t event;",file=fout)
    print(file=fout)

    P=H['state1'].append(H['next state'])
    P=P.unique()
    ni = len(P)
    print ("enum state_t {",file=fout)
    for x in P:
        x=str(x)
        k=""
        if not (x=="nan" or x=="any"):
            k="\t"+x.strip()
            ni-=1
            if ni>0: k+=","
            print(k,file=fout)
    print("};",file=fout)
    print("extern enum state_t state;",file=fout)
    print(file=fout)

    
    
def create_actions(H,fout,impl=False):
    print( "/**********************",file=fout)
    print ("********* ACTIONS ******",file=fout)
    print ("***********************/",file=fout)
    print("\n")
    P=H['action'].unique()
    for a in P:
        a=str(a)
        if  a=='nan':
            continue
        if not impl:
            print ("void "+a.strip()+"();",file=fout)
        else:
            print ("void "+a.strip()+"(){\n}",file=fout)

        #print ("}")
        print(file=fout)
    if not impl: print("void fsm();",file=fout)
        
def create_guards(H,fout,impl=False):
    print ("/**********************",file=fout)
    print ("********* GUARDS ******",file=fout)
    print ("***********************/",file=fout)
    print(file=fout)
    P=H['guard'].unique()
    for a in P:
        a=str(a)
        if  a=='nan':
            continue
        if not impl: 
            print("char "+a.strip()+"();",file=fout)
        else:
            print("char "+a.strip()+"(){\n}",file=fout)

        #print("}")
        print(file=fout)

def do_anystates(H,fout):
    P=H[H['state1']=="any"]
    
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
        pe= str(x['post event'])
        pi = str(x['post input'])
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
        print ("\t\tif ("+k+")  {",file=fout)
        if not a=='nan':
            print ('\t\t\t'+a.strip()+"();",file=fout)
        if not n=='nan':
            if not n=="any":
                print("\t\t\tstate="+n+";",file=fout)
        if not pi=='nan':
            if not pi==j:
                print("\t\t\tinput="+pi+";",file=fout)
        if not pe=='nan':
            if not pe==e:
                print("\t\t\tevent="+pe+";",file=fout)
        print ('\t\t}',file=fout)
            
        
        
def create_fsmfun(H,fout):
    print( "/**********************",file=fout)
    print ("********* FSM ******",file=fout)
    print ("***********************/",file=fout)
    print

    states1 = H['state1'].unique()

    print ("void fsm() {",file=fout)


    if "any" in states1:
        do_anystates(H,fout)
    

    print ("\tswitch (state) {",file=fout)


    for s in states1:
        if s=="any": continue
        print ("\tcase ("+s+"): ",file=fout)
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
            pe= str(x['post event'])
            pi = str(x['post input'])

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
            print ("\t\tif ("+k+")  {",file=fout)
            if not a=='nan':
                print ('\t\t\t'+a.strip()+"();",file=fout)
            if not n=='nan':
                if not n==s:
                    print("\t\t\t state="+n+";",file=fout)
            if not pi=='nan':
                if not pi==j:
                    print("\t\t\tinput="+pi+";",file=fout)
            if not pe=='nan':
                if not pe==e:
                    print("\t\t\tevent="+pe+";",file=fout)

            print ('\t\t}',file=fout)
            
        print("\t\tbreak;",file=fout)
        
    print("\t}",file=fout)                     
    print("}",file=fout)

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('-i','--inp',default=False, help='input xlsx file containing the transition table')
    parser.add_argument('-o','--out',default=False, help='output .c-file containing the FSM code')
    args=parser.parse_args()
    #sys.stdout = open(args.out+".c", "w")
    fout = open(args.out+".c","w")
    fhead = open(args.out+".h","w")   
    fwork= open(args.out+'_worker.c',"w") 
    H=pd.read_excel(args.inp+'.xlsx',"Transition")

    
    print(
"""
/****************************************************
File created with fsm_coder python script by M.Birkner
https://github.com/mbirkner/fsm_coder.git
****************************************************/

#include "fsm.h"

enum event_t event;
enum input_t input;
enum state_t state;
""",file=fout)

    print(
"""
/****************************************************
File created with fsm_coder python script by M.Birkner
https://github.com/mbirkner/fsm_coder.git
****************************************************/

#ifndef FSM_INC
#define FSM_INC
""",file=fhead)

    print(
"""
/****************************************************
File created with fsm_coder python script by M.Birkner
https://github.com/mbirkner/fsm_coder.git
****************************************************/

#include "fsm.h"

enum event_t event;
enum input_t input;
enum state_t state;
""",file=fwork)

  
    create_enums(H,fhead)
    create_actions(H,fhead)
    create_guards(H,fhead)
    create_actions(H,fwork,True)
    create_guards(H,fwork,True)

    create_fsmfun(H,fout)
##    print(
##"""
##void main() {
##        while(1) {
##            fsm();
##        }
##}""")
##    sys.stdout.close()
    fhead.write("#endif")
    fout.close()
    fhead.close()
    fwork.close()

if __name__=='__main__':
    main()
