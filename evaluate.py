#! /usr/bin/env python3

import pickle
from subprocess import run
from sys import argv
from os import getcwd
from os.path import isfile
from sys import argv

if __name__ == "__main__":
    
    path = getcwd()
    genome = argv[1]
    eval_levels = []
    if isfile(path + '/levels'):
        with open('levels') as f:
            for line in f:
                x,y = line.split()
                x,y = float(x),float(y)
                eval_levels.append((x,y)) 
    out = open(f'presence_absence/{genome}.csv','w')
    
    with open(f'results/{genome}.pickle','rb') as f:
        results = pickle.load(f)

    for gene,res in results.items():
        if res == 'NA':
            out.write(f'{gene},0,0\n')
        elif res[0] == 1:
            out.write(f'{gene},1,0\n')
        else:
            best_e = res[1]["best reverse hit's evalue"]
            own_e = res[1]["original protein's evalue"]
            if own_e == 0:
                out.write(f'{gene},1,1\n')
            elif own_e == 'original protein not hit by reverse blast':
                out.write(f'{gene},0,0\n')
            elif own_e > 1e-9:
                out.write(f'{gene},0,0\n')
            else:
                written = 0
                for e,d in eval_levels:
                    if best_e > e:
                        continue
                    else:
                        if best_e/own_e < d:
                            out.write(f'{gene},1,1\n')
                            written = 1
                            break
                if written == 0:
                    out.write(f'{gene},0,0\n')

    out.close()
