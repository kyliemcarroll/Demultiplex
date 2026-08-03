#!/usr/bin/env python

# Author: kymc@uoregon.edu

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "1.0"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = ["A","T","C","G","N"]
RNA_bases = ["A","T","U","G","N"]

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter) - 33

def qual_score(phred_score: str) -> float:
    add = 0
    for letter in phred_score:
        score = convert_phred(letter)
        add += score
    average = add/len(phred_score)
    return(average)

def validate_base_seq(seq: str, RNAFlag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    seq = seq.upper()
    DNA_bases = ["A","T","C","G","N"]
    RNA_bases = ["A","T","U","G","N"]
    if RNAFlag:
        return seq.count("A") + seq.count ("C") + seq.count("G")+ seq.count("U")  == len(seq)
    else:
        return seq.count("A") + seq.count ("C") + seq.count("G")+ seq.count("T") == len(seq)

def gc_content(seq: str) -> int:
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    assert validate_base_seq(seq)
    seq = seq.upper()
    gc = (seq.count("G") + seq.count("C")) / len(seq)
    return gc

def calc_median(list: list) -> int:
    '''Given a sorted list, returns the median value of the list'''
    list.sort()
    list_length = len(list)
    #for odd numbers:
    if list_length%2 == 1:
        midpos = list_length//2
        median = list[midpos]
    #for even numbers:
    else:
        pos1 = list_length//2
        pos2 =list_length//2-1
        median = (list[pos1]+list[pos2])/2
    return(median)

def oneline_fasta(file_fasta, new_fasta):
    '''Given a FASTA file with multiple seq lines, this will convert the format to only 2 lines: one header line and one seq line'''
    with open(file_fasta,'r') as fin, open(new_fasta,'w') as fout:
        for i, line in enumerate(fin):
            line = line.strip("\n")
        if i == 0:
            fout.write(f'{line}\n')
        elif line.startswith(">"):
            fout.write(f'\n{line}\n')
        else:
            fout.write(f'{line}')

def fastq_record(fastq_file):
    '''takes a FASTQ file grabs the first 4 lines and stores record as a list'''
    with open(fastq_file,"r") as fh:
        while True:
#save the records in memory
            header = fh.readline().strip()
            seq = fh.readline().strip()
            plus = fh.readline().strip()
            qscore = fh.readline().strip()
            if header == "":
                break

if __name__ == "__main__":
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")
#calc median test
    assert calc_median([1,2,3]) == 2
    assert calc_median([5,6,7,8]) == 6.5
    assert calc_median([1,1,1,1,1,1,1,1,100]) == 1
    print("Your calc_median function is working! Nice job")
#gc content test
    assert gc_content("GCGCGC") == 1
    assert gc_content("AATTATA") == 0
    assert gc_content("GCATCGAT") == 0.5
    print("Your gc content function is working! Nice job")
#qual score test
    assert qual_score("A") == 32.0, "wrong average phred score for 'A'"
    assert qual_score("$") == 3.0, "wrong average phred score for '$'"
    print("Your qual score function is working! Nice job")
#validate base seq test
    assert validate_base_seq("AATAGAT"), "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True), "Validate base seq does not work on RNA"
    assert validate_base_seq("aatagat"), "Validate base seq does not work on lowercase DNA"
    assert validate_base_seq("aauagau", True), "Validate base seq does not work on lowercase RNA"
    print("Your validate base seq function is working! Nice job")