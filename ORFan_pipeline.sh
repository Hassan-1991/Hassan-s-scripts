#Given a fasta file of protein sequences from E. coli, this script extracts all proteins without homologs in bacteria.
#K12 is an example, this can be done with any strain
#Target sequence lists provided by Zach

#STEPS
Search steps:
1. Blast this query file against non-redundant list of Salmonella enterica serovar Typhimurium proteins
2. Extract ORFans
3. Blast this list of ORFans against non-redundant list of all bacterial proteins except E. coli
4. Extract ORFans2
5. Blast this list of ORFans2 against the nr.dmnd database, excluding E. coli, eukaryotes, archaea and viruses
6. Extract ORFans3

#!/bin/bash

#SBATCH --time=10:00:00
#SBATCH -p normal
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=68
#SBATCH --job-name="K12_ORFans_pipeline"
#SBATCH --output="K12_ORFans_pipeline_output"
./genomics_toolbox/diamond blastp -q ./K12_dedupe_sorted.faa -d Salmurium_dedupe.dmnd --out K12blastout_1.tsv --outfmt 6 -b8 -c1
grep ">" ./K12_dedupe_sorted.faa | cut -f 1 -d ' ' | tr -d '>' | sort -u > K12_IDs.txt
cut -f 1 -d " " K12blastout_1.tsv | sort -u > K12_nORFan_IDs1.txt #add a tab
comm -3 K12_IDs.txt K12_nORFan_IDs1.txt > K12_ORFan_IDs1.txt
./faSomeRecords K12_dedupe_sorted.faa K12_ORFan_IDs1.txt K12_ORFans1.faa
./genomics_toolbox/diamond blastp -q ./K12_ORFans1.faa -d bacteria_woEC_dedupe.dmnd --ultra-sensitive --out K12blastout_2.tsv --outfmt 6 -b8 -c1
cut -f 1 -d " " K12blastout_2.tsv | sort -u > K12_nORFan_IDs2.txt #add a tab
comm -3 K12_ORFan_IDs1.txt K12_nORFan_IDs2.txt > K12_ORFan_IDs2.txt
./faSomeRecords K12_dedupe_sorted.faa K12_ORFan_IDs2.txt K12_ORFans2.faa
./genomics_toolbox/diamond blastp -q ./K12_ORFans2.faa -d nr.dmnd --taxon-exclude 10239,2157,2759,562 --ultra-sensitive --out K12blastout_3.tsv --outfmt 6 -b8 -c1
cut -f 1 -d " " K12blastout_3.tsv | sort -u > K12_nORFan_IDs3.txt #add a tab
comm -3 K12_ORFan_IDs2.txt K12_nORFan_IDs3.txt > K12_ORFan_IDs3.txt
./faSomeRecords K12_dedupe_sorted.faa K12_ORFan_IDs3.txt K12_ORFans3.faa

#Then to extract lengths of sequences from this file:
cat K12_ORFans3.faa | awk '$0 ~ ">" {if (NR > 1) {print c;} c=0;printf substr($0,2,100) "\t"; } $0 !~ ">" {c+=length($0);} END { print c; }' > K12_ORFans3_lengths.tsv
