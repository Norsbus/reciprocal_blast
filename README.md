- ONLY USABLE ON SLURM CLUSTERS (tweak configs in main1.py, main2.py, main3.py)

- make sure you have a proteome you want to compute for and a genomes.txt with all genomes specified on a single line and those genomes available at a path (to be specified to prep.py, see below) <br>
- example genomes.txt: <br>
GCA_0000.1<br>
GCF_1111.2<br>
Drosophila_melanogaster<br>
- then at a genomes_path there should be: <br>
GCA_0000.1.fasta<br>
GCF_1111.2.fasta<br>
Drosophila_melanogaster.fasta<br>
available<br>

- pipeline will produce csv files in presence_absence/{genome}.csv with structure: <br>

gene,present,changed to present although not primary reverse hit because its still very significant and the difference to the primary reverse hit is not too large as defined in "levels" and applied in "evaluate.py"

- run (and wait until all slurm jobs generated by a script are finished): <br>
	python3 prep.py /path/to/genomes/ /path/to/proteome/ /path/to/blastdbs/ [the paths need to be absolute and if blastdbs do not exist just put {absolute path of this directory}/blastdbs] <br>
	python3 main1.py <br>
	python3 main2.py <br>
	python3 main3.py <br>

- optional to get the presence absence per gene in pa_per_gene/{gene}.csv (after running the above): <br>
python3 get_pa_per_gene.py
