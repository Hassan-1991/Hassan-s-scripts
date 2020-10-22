def get_at(sequence):
    return (sequence.count("A")+sequence.count("T"))/len(sequence)

def get_dinucleotides(sequence):
    dinucleotides = ("AA", "AT", "AG", "AC", "TA", "TT", "TG", "TC", "GA", "GT", "GG", "GC", "CA", "CT", "CG", "CC")
    dinucleotide_list=[]
    for i in dinucleotides:
        dinucleotide_list.append(sequence.count(i)/len(sequence))
    return dinucleotide_list

def len_AT_dinuc(sequence):
    feature_list=[]
    feature_list.append(len(sequence))
    feature_list.append(get_at(sequence))
    feature_list.extend(get_dinucleotides(sequence))
    return feature_list

def file_to_seqlist(file2):
    file3=[]
    for i in file2:
        file3.append(i.rstrip('\n'))
    SeqList=[]
    for i in file3:
        if i[0]!=">":
            SeqList.append(i)
    return (SeqList)

def Sequence_Features(file):
    SeqList=file_to_seqlist(file)
    return map(len_AT_dinuc,SeqList)

file1=open("input_file_name.txt")
file2=file1.readlines()
file1.close()

gene_features=open("output_file_name.txt","w")
for i in Sequence_Features(file2):
    for j in i:
        gene_features.write(str(j)+'\t')
    gene_features.write('\n')
