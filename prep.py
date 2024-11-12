#! /usr/bin/env python3

from subprocess import run
from os.path import isfile
from os import getcwd,listdir
import multiprocessing as mp
from Bio import SeqIO
import pickle
from sys import argv 

def mbdb(org):
    if not (isfile(f"{blastdbs_path}/{org}.nin") and isfile(f"{blastdbs_path}/{org}.nhr") and isfile(f"{blastdbs_path}/{org}.nsq")):
        run(f"makeblastdb -in {genomes_path}/{org}.fasta -out {blastdbs_path}/{org} -dbtype nucl".split())
    return 0

if __name__ == "__main__":
    if len(argv) < 4:
        print('please run like python3 prep.py /path/to/genomes/ /path/to/proteomes/ /path/to/blastdbs/')
        exit(1)
    else:
        genomes_path = argv[1]
        proteome_path = argv[2]
        blastdbs_path = argv[3]
        with open('paths','w') as f:
            f.write(f'{genomes_path}\n{proteome_path}\n{blastdbs_path}\n')
    genomes = []
    with open('genomes.txt') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip()
            if len(line) == 0:
                continue
            genomes.append(line)
    run('chmod +x ./*',shell=True)
    run('./make_directories.py')
    with mp.Pool(processes=mp.cpu_count()) as pool:
        res = pool.map_async(mbdb,genomes).get()

    proteome = [x for x in listdir(f'{proteome_path}') if '.fasta' in x]
    if len(proteome) > 1:
        print('please provide only one proteome in proteome folder and clone a new repo for each separate proteome/genomes set')
        exit(1)
    else:
        proteome = proteome[0]
        run(f"makeblastdb -in {proteome_path}/{proteome} -out {blastdbs_path}/{proteome}_prot -dbtype prot".split())
    counter = 1
    ids = {}
    for record in SeqIO.parse(f'{proteome_path}/{proteome}', "fasta"):
            ids[record.id] = str(counter)
            ids[str(counter)] = record.id
            SeqIO.write(record, f"focal_proteins/{counter}.fasta", "fasta")
            counter += 1
    with open('proteome/record_mapping.pickle','wb') as f:
        pickle.dump(ids,f)
