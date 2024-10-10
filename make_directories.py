#! /usr/bin/env python3

import os,json,sys,shutil
from subprocess import run
from sys import argv
import pathlib


def make_directories(directories):

    for directory in directories:
        directory = f'{work_dir}/'+directory
        if not os.path.exists(directory):
            os.mkdir(directory)

    return 0


def remove_directories(directories):
    
    for directory in directories:
        directory = f'{work_dir}/'+directory
        try:
            shutil.rmtree(directory)
        except FileNotFoundError as e:
            pass

    return 0

if __name__ == "__main__":
    
    work_dir = pathlib.Path(__file__).parent.resolve()

    with open(f'{work_dir}/config.json','r') as f:

        config = json.loads(f.read())
        
        if "directories" not in config:
            pass
        else:
            d=config["directories"]
            remove_directories(d)
            make_directories(d)
