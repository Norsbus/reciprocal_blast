#! /usr/bin/env python3

import pickle
from os import listdir,getcwd
from os.path import isfile
from sys import argv

if __name__ == "__main__":

    genome = argv[1]
    path = getcwd()
    proteins = listdir(path + '/focal_proteins/')
    proteins = [p.strip().split('.fasta')[0] for p in proteins]
    with open('proteome/record_mapping.pickle','rb') as f:
        record_mapping = pickle.load(f)

    res = {}
    for protein in proteins:
        ids,scores = [],[]
        max_score = 1e6
        own = 1e6
        if isfile(path + f'/reblast_out/{genome}/{protein}'):
            with open(f'reblast_out/{genome}/{protein}','r') as f:
                for line in f:
                    line = line.split('\t')
                    if line[0] == '#' or len(line) == 0:
                        continue
                    scores.append(float(line[-2]))
                    ids.append(line[1])
                    if line[1] in record_mapping[protein] or record_mapping[protein] in line[1]:
                        if float(line[-2]) < own:
                            own = float(line[-2])
        else:
            res[record_mapping[protein]] = 'NA'
            continue
            
        if len(ids) == 0:
            res[record_mapping[protein]] = 'NA'
            continue

        idx = scores.index(min(scores))
        best_id = ids[idx]
        best = scores[idx]
        scores.remove(scores[idx])
        ids.remove(ids[idx])
        if len(scores) == 0:
            second_best_id = protein
            second_best = protein
        else:
            idx = scores.index(min(scores))
            second_best = scores[idx]
            second_best_id = ids[idx]
            while (second_best_id in record_mapping[protein] or record_mapping[protein] in second_best_id) and len(scores) > 0:
                scores.remove(scores[idx])
                ids.remove(ids[idx])
                if len(scores) == 0:
                    second_best_id = protein
                    second_best = protein
                    break
                idx = scores.index(min(scores))
                second_best = scores[idx]
                second_best_id = ids[idx]

        if best_id in record_mapping[protein] or record_mapping[protein] in best_id:
            res[record_mapping[protein]] = [1,{'own evalue':best,'second best reverse hit':second_best_id,'second best reverse hit\'s evalue':second_best}]
        else:
            if own >= 1e5:
                own = 'original protein not hit by reverse blast'
            res[record_mapping[protein]] = [0,{'best reverse hit':best_id,'best reverse hit\'s evalue':best,'original protein\'s evalue':own}]

    with open(f'results/{genome}.pickle','wb') as f:
        pickle.dump(res,f)
