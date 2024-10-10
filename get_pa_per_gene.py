#! /usr/bin/env python3

from subprocess import run
from os.path import isfile
from os import getcwd,listdir
import multiprocessing as mp
from Bio import SeqIO
import pickle

if __name__ == "__main__":
    run(f'mkdir -p pa_per_gene',shell=True)
    path = getcwd()
    genomes = listdir(path + '/genomes/')
    genomes = [g.strip().split('.fasta')[0] for g in genomes]
    proteins = listdir(path + '/focal_proteins/')
    proteins = [p.strip().split('.fasta')[0] for p in proteins]
    res = {}
    pa = {}
    eval_levels = []
    if isfile(path + '/levels'):
        with open('levels') as f:
            for line in f:
                x,y = line.split()
                x,y = float(x),float(y)
                eval_levels.append((x,y)) 
    with open('proteome/record_mapping.pickle','rb') as f:
        record_mapping = pickle.load(f)

    for genome in genomes:
        with open(f'results/{genome}.pickle','rb') as f:
            res[genome] = pickle.load(f)
    for protein in proteins:
        protein = record_mapping[protein]
        with open(f'pa_per_gene/{protein}.csv','w') as f:
            for genome in genomes:
                if res[genome][protein] == "NA":
                    f.write(f'{genome},0\n')
                elif res[genome][protein][0] == 1:
                    f.write(f'{genome},1\n')
                else:
                    best_e = res[genome][protein][1]["best reverse hit's evalue"]
                    own_e = res[genome][protein][1]["original protein's evalue"]
                    if own_e == 0:
                        f.write(f'{genome},0\n')
                    elif own_e == 'original protein not hit by reverse blast':
                        f.write(f'{genome},0\n')
                    elif own_e > 1e-9:
                        f.write(f'{genome},0\n')
                    else:
                        written = 0
                        for e,d in eval_levels:
                            if best_e > e:
                                continue
                            else:
                                if best_e/own_e < d:
                                    f.write(f'{genome},1\n')
                                    written = 1
                                    break
                        if written == 0:
                            f.write(f'{genome},0\n')
