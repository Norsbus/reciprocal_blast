- ONLY USABLE ON SLURM CLUSTERS (tweak configs in main1.py, main2.py, main3.py)

- put genomes in "genomes" folder and focal proteome in "proteome" folder

- pipeline will produce csv files in presence_absence/{genome}.csv with structure:

gene,present,changed to present although not primary reverse hit because its still very significant and the difference to the primary reverse hit is not too large as defined in "levels" and applied in "evaluate.py"

- run:
	python3 prep.py
	python3 main1.py
	python3 main2.py
	python3 main3.py

- optional to get the presence absence per gene in pa_per_gene/{gene}.csv (after running the above):
./get_pa_per_gene.py

- if you have genomes and a proteome as mentioned above (point 2) and set any custom slurm settings (point 1) you can also just copy and run the following to run the whole pipeline:

	python3 prep.py && python3 main1.py && python3 main2.py && python3 main3.py && python3 get_pa_per_gene.py
