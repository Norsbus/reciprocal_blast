#! /usr/bin/env python3

import pathlib
from sys import argv
from subprocess import run,check_output
from os import listdir,getcwd
from time import sleep

if __name__ == "__main__":
   
    conda_lines = ''

    path = getcwd()
    genomes = []
    with open('genomes.txt') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip()
            if len(line) == 0:
                continue
            genomes.append(line)
    
    skip_some = False

    for genome in genomes:
        cmd = f"""\
#!/usr/bin/env bash\n\
#SBATCH -e slurm_log/{genome}_eval.err\n\
#SBATCH -o slurm_log/{genome}_eval.out\n\
#SBATCH --job-name={genome}_eval\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem=8000\n\
#SBATCH --time=7-00:00:00\n\
{conda_lines}\n\
./evaluate.py {genome}
"""
        with open(f'slurm_job_scripts/{genome}_eval','w') as f2:
            f2.write(cmd)
        if skip_some and counter_skip >= 0:
            run(f'sbatch slurm_job_scripts/{genome}_eval',shell=True)
            counter_skip -= 1
            continue
        out = check_output(['sinfo','-o','%C'])
        idle = int(out.decode().split()[1].split('/')[1])
        while idle < 1:
            out = check_output(['sinfo','-o','%C'])
            idle = int(out.decode().split()[1].split('/')[1])
            sleep(1)
        run(f'sbatch slurm_job_scripts/{genome}_eval',shell=True)
        if idle > 10:
            skip_some = True
            counter_skip = 50
        sleep(1)
