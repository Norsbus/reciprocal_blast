#! /usr/bin/env python3

import pathlib
from sys import argv
from subprocess import run
import pickle
from os import listdir,getcwd
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import SeqIO

def blast(db,query,outfile):
    cmd = 'tblastn -task tblastn-fast -db {} -query {} -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sseq" -evalue 1e-3 -word_size 7 -out {}'.format(db,query,outfile)
    print(cmd)
    run(cmd,shell=True)
    return(0)

def clasp_with_fragments(infile,outfile,l=0.5,e=0):
    cur = str(pathlib.Path(__file__).parents[0])
    bin_dir = cur + '/bin'
    cmd = '{}/clasp.x -m -i {} -c 7 8 9 10 12 -C 1 2 -l {} -e {} --fragment --orig -o {}'.format(bin_dir,infile,l,e,outfile).split()
    run(cmd)
    return(0)

def exec_blast_clasp(genome,protein):
        
    blast(f'./blastdbs/{genome}',f'./focal_proteins/{protein}.fasta',f'./blast_out_both/{genome}/{protein}')
    
    with open(f'./blast_out_both/{genome}/{protein}','r') as f:
        newlines_forward = []
        newlines_reverse = []
        for line in f:
            line = line.split()
            if line[0] == '#' or len(line) == 0:
                continue
            if int(line[8]) > int(line[9]):
                line[8],line[9] = line[9],line[8]
                newlines_reverse.append('\t'.join(line))
            else:
                newlines_forward.append('\t'.join(line))

    with open(f'./blast_out_forward/{genome}/{protein}','w') as f:
        f.write('\n'.join(newlines_forward))
    with open(f'./blast_out_reverse/{genome}/{protein}','w') as f:
        f.write('\n'.join(newlines_reverse))

    for orientation in ['forward','reverse']:
    
        clasp_with_fragments(f'./blast_out_{orientation}/{genome}/{protein}',f'./clasp_out_{orientation}/{genome}/{protein}')

    return(0)

def write_best_hit_and_reblast(genome,protein):
    
    max_score = 0
    fragments_clasp = {}
    ori = None
    for orientation in ['forward','reverse']:

        fragments_clasp[orientation] = {}
        
        if orientation == 'forward':
            clasp_file = f"./clasp_out_forward/{genome}/{protein}"
        else:
            clasp_file = f"./clasp_out_reverse/{genome}/{protein}"
        
        append = False
        with open(clasp_file,'r') as f:
            for line in f:
                line = line.split()
                if line[0] == '#' or len(line) == 0:
                    continue
                if line[0] == "C":
                    append = False
                    chromo = line[2]
                    score = float(line[7])
                    if score < max_score:
                        continue
                    else:
                        append = True
                        max_score = score
                        ori = orientation
                        taken_chromo = chromo
                        fragments_clasp[orientation][chromo] = [[int(line[5]),int(line[6]),'']]
                else:
                    if append:
                        fragments_clasp[orientation][chromo][0][-1] += line[-1]
    if ori != None:
        for cf in fragments_clasp[ori][taken_chromo]:
            seq = fragments_clasp[ori][taken_chromo][0][-1]
            seq = Seq(str(seq).replace('-',''))
            SeqIO.write(SeqRecord(seq,id=f"pot_orthologue_{protein}_on_{taken_chromo}_nuc_start_{cf[0]}_nc_end_{cf[1]}"), f"./best_forward_hits/{genome}/{protein}.fasta", "fasta")

        run(f'blastp -db ./blastdbs/{proteome}_prot -query ./best_forward_hits/{genome}/{protein}.fasta -outfmt 6 -out reblast_out/{genome}/{protein} -word_size 3 -evalue 1e-3',shell=True)

    return(0)

if __name__ == '__main__':

    genome = argv[1]
    protein = argv[2]
    run(f'mkdir -p blast_out_both/{genome} blast_out_forward/{genome} blast_out_reverse/{genome} clasp_out_forward/{genome} clasp_out_reverse/{genome} best_forward_hits/{genome} reblast_out/{genome}',shell=True)
    proteome = [x for x in listdir('proteome') if '.fasta' in x][0]
    exec_blast_clasp(genome,protein)
    write_best_hit_and_reblast(genome,protein)
