#! /usr/bin/env python3

from subprocess import run
from os.path import isfile
from os import getcwd,listdir
import multiprocessing as mp
from Bio import SeqIO
import pickle

def mbdb(org):
    if not (isfile(path + "/blastdbs/{}.nin".format(org)) and isfile(path + "/blastdbs/{}.nhr".format(org)) and isfile(path + "/blastdbs/{}.nsq".format(org))):
        run("makeblastdb -in genomes/{}.fasta -out blastdbs/{} -dbtype nucl".format(org,org).split())
    return 0

if __name__ == "__main__":
    run('chmod +x ./*',shell=True)
    run('./make_directories.py')
    path = getcwd()
    genomes = listdir(path + '/genomes/')
    genomes = [g.strip().split('.fasta')[0] for g in genomes if '.fasta' in g]
    with mp.Pool(processes=mp.cpu_count()) as pool:
        res = pool.map_async(mbdb,genomes).get()

    proteome = [x for x in listdir(path + '/proteome') if '.fasta' in x]
    if len(proteome) > 1:
        print('please provide only one proteome in proteome folder and clone a new repo for each separate proteome/genomes set')
        exit(1)
    else:
        proteome = proteome[0]
        run(f"makeblastdb -in proteome/{proteome} -out blastdbs/{proteome}_prot -dbtype prot".split())
    counter = 1
    ids = {}
    for record in SeqIO.parse(path+f'/proteome/{proteome}', "fasta"):
            ids[record.id] = str(counter)
            ids[str(counter)] = record.id
            SeqIO.write(record, f"focal_proteins/{counter}.fasta", "fasta")
            counter += 1
    with open('proteome/record_mapping.pickle','wb') as f:
        pickle.dump(ids,f)
