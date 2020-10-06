#Takes a single file/a bunch of fasta format sequence files as input, and converts them into a single file with all the sequence linebreaks removed

import glob
import re

#Step 1, option A: in case where the input consists of multiple fasta files
#Take all files with .faa extension from a directory, put all of them in the same file, and mark the sequence identifier lines

Fasta_files=glob.glob("<directory_path>/*.faa")

file3=[]
for i in Fasta_files:
    file1=open(i)
    file2=file1.readlines()
    for i in file2:
        if i[0]==">":
            file3.append(i.rstrip('\n')+'<') #This marks the sequence identifier lines with a "<" at the end
        else:
            file3.append(i.rstrip('\n'))

#Step 1, option B: in case where the input is just one fasta file
#Convert the file into a list and mark the sequence identifier lines

file1=open(<file_path>)
file2=file1.readlines()
file1.close()
for i in file2:
    if i[0]==">":
        file3.append(i.rstrip('\n')+'<') #This marks the sequence identifier lines with a "<" at the end
    else:
        file3.append(i.rstrip('\n'))

#Step 2: Make a giant string by concatenating all lines, split the string into a list with < and > as delimiters.
#The output will be exactly what we want, minus the starting ">" in front of every identifier.

file4=""
file6=[]
for k in file3:
    file4=file4+k #a giant string with all lines concatenated
file5=re.split(r"[><]",file4) #list with all elements demarcated with > and <
for l in file5[1:len(file5)]: #since the first item is an empty string
    file6.append(l) #This has all identifiers and their sequences in a list

#Step 3: Output the sequence identifiers and their corresponding sequences in a file, with the ">" added in front of each identifier.

Linearized_Fasta=open("<output_file_path>","w")
for i in file6:
    if file6.index(i)%2==0:
        Linearized_Fasta.write(">"+i+'\n')
    else:
        Linearized_Fasta.write(i+'\n')
