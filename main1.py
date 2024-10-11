#! /usr/bin/env python3

from sys import argv
from subprocess import run,check_output
from os import listdir,getcwd
from time import sleep

if __name__ == "__main__":
   
    conda_lines = ''

    path = getcwd()
    genomes = listdir(path + '/genomes/')
    genomes = [g.strip().split('.fasta')[0] for g in genomes if '.fasta' in g]
    proteins = listdir(path + '/focal_proteins/')
    proteins = [p.strip().split('.fasta')[0] for p in proteins]
    
    skip_some = False

    for genome in genomes:
        for protein in proteins:
            cmd = f"""\
#!/usr/bin/env bash\n\
#SBATCH -e slurm_log/{genome}_{protein}.err\n\
#SBATCH -o slurm_log/{genome}_{protein}.out\n\
#SBATCH --job-name={genome}_{protein}\n\
#SBATCH --cpus-per-task=1\n\
#SBATCH --mem=8000\n\
#SBATCH --time=7-00:00:00\n\
{conda_lines}\n\
./job.py {genome} {protein}
"""
            with open(f'slurm_job_scripts/{genome}_{protein}','w') as f2:
                f2.write(cmd)
            if skip_some and counter_skip >= 0:
                run(f'sbatch slurm_job_scripts/{genome}_{protein}',shell=True)
                counter_skip -= 1
                continue
            out = check_output(['sinfo','-o','%C'])
            idle = int(out.decode().split()[1].split('/')[1])
            while idle < 1:
                out = check_output(['sinfo','-o','%C'])
                idle = int(out.decode().split()[1].split('/')[1])
                sleep(1)
            run(f'sbatch slurm_job_scripts/{genome}_{protein}',shell=True)
            if idle > 10:
                skip_some = True
                counter_skip = 50
            sleep(1)
