#! /usr/bin/env python3

import pathlib
from sys import argv
from subprocess import run,check_output
from os import listdir,getcwd
from time import sleep

if __name__ == "__main__":
   
    conda_lines = ''

    path = getcwd()
    genomes = listdir(path + '/genomes/')
    genomes = [g.strip().split('.fasta')[0] for g in genomes]
    
    skip_some = False

    for genome in genomes:
        cmd = f"""\
#!/usr/bin/env bash\n\
#SBATCH -e slurm_log/{genome}_collect.err\n\
#SBATCH -o slurm_log/{genome}_collect.out\n\
#SBATCH --job-name={genome}_collect\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem=8000\n\
#SBATCH --time=7-00:00:00\n\
{conda_lines}\n\
./collect.py {genome}
"""
        with open(f'slurm_job_scripts/{genome}_collect','w') as f2:
            f2.write(cmd)
        if skip_some and counter_skip >= 0:
            run(f'sbatch slurm_job_scripts/{genome}_collect',shell=True)
            counter_skip -= 1
            continue
        out = check_output(['sinfo','-o','%C'])
        idle = int(out.decode().split()[1].split('/')[1])
        while idle < 1:
            out = check_output(['sinfo','-o','%C'])
            idle = int(out.decode().split()[1].split('/')[1])
            sleep(1)
        run(f'sbatch slurm_job_scripts/{genome}_collect',shell=True)
        if idle > 10:
            skip_some = True
            counter_skip = 50
        sleep(1)
