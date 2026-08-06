#!/usr/bin/env python

import argparse
import gzip


def read_record(fastq):
    '''records the first 4 lines in a fastq file = record'''
    record = []
    for i in range(4):
        record.append(fastq.readline().strip("\n"))
    return(record)

base_dict = {"A":"t","T":"a","G":"c","C":"g","N":"n"}
def rev_comp(seq: str) -> str:
    '''take a DNA seq and output the reverse comp str'''
    seq = seq.upper()
    new_seq = ""
    for base in seq:
        new_seq += base_dict[base]
    new_seq = new_seq.upper()
    new_seq = new_seq [::-1]
    return new_seq

def get_args():
    parser = argparse.ArgumentParser(description="Program to modify file name")
    parser.add_argument("-f1", help="Fwd File", type=str)
    parser.add_argument("-f2", help="Fwd Index", type=str)
    parser.add_argument("-f3", help="Rev Index", type=str)
    parser.add_argument("-f4", help="Rev File", type=str)
    parser.add_argument("-ofp", help="output file path", type=str)
    return parser.parse_args()
args = get_args()
R1 = args.f1
R4 = args.f2
R2 = args.f3
R3 = args.f4
ofp = args.ofp


#path to barcodes
barcodes = "/projects/bgmp/shared/2017_sequencing/indexes.txt"
#creating a set data structure to hold my indices
barcodes_set = set()                                #initializing my set
with open(barcodes, "r") as fh:
    for line in fh:
        if not line.startswith("sample"):           #cutting out header label info
            column = line.strip("\n").split("\t")   #spliting the tab sep line to help pull from it
            indexes = column [4]                    #grab just the barcode
            barcodes_set.add(indexes)               #add the barcode to my set

#making unique barcode labeled files
file_dict = {}
for barcode in barcodes_set:
    file_dict[barcode] = open(f'{ofp}/{barcode}_R1.fq',"w"), open(f'{ofp}/{barcode}_R2.fq',"w")

unk_R1 = open(f'{ofp}/unk_R1.fq', "w")
unk_R2 = open(f'{ofp}/unk_R2.fq', "w")
hopped_R1 = open(f'{ofp}/hopped_R1.fq', "w")
hopped_R2 = open(f'{ofp}/hopped_R2.fq',"w")


def demux(fastq_R1, fastq_R2, fastq_R3,fastq_R4):
    '''when given four zipped fastq files (fwd read, rev read, and fwd and rev barcodes), open all of them at once and read them four lines at a time until you reach the end of the files.
    then, find the number of matched barcodes, hopped barcodes, and unknown barcodes and write them to the corresponding output files.
    while doing this, keep a running count value of how many records outputted to each section.'''
    matched_dict = {}                               #initializing matched dictionary, value is the running sum
    hopped_dict = {}                                #intialzing my hopped dictionary, value is the running sum
    unk_count = 0                                   #running sum for unknown barcode counter, initializing variable
    record_count = 0                                #running sum for the record count
    with gzip.open(fastq_R1,"rt") as fwdfile, gzip.open(fastq_R4,"rt") as revfile, gzip.open(fastq_R2,"rt") as index1, gzip.open(fastq_R3,"rt")as index2:
        while True:                                 #looping through all four files at once
            R1 = read_record(fwdfile)               #reading the first four lines of fwd file
            R4 = read_record(revfile)               #reading the first four lines of rev file
            R2 = read_record(index1)                #reading the first four lines of the fwd barcode file
            R3 = read_record(index2)                #reading the first four lines of the rev barcode file
            fwd_bc = R2[1]                          #storing the fwd barcode line in memory to call to later
            rev_bc = rev_comp(R3[1])                #storing the rev barcode line in memory to call to later, also calling rev comp func here ONCE to save time
            bc_pair = (f'{fwd_bc}-{rev_bc}') #creating a base pair string variable
            if R1[3] == "":                         #empty string == end of file and WE DONE!
                break
            if (fwd_bc not in barcodes_set) or (rev_bc not in barcodes_set):#if fwd barcode or rev comp of the rev barcode not in the barcode set
                unk_count += 1                      #add to the unk counter
                unk_R1.write(f'{R1[0]} {fwd_bc}-{rev_bc}\n{R1[1]}\n{R1[2]}\n{R1[3]}\n') #output the unknown fwd record with barcodes appended to the end of the header
                unk_R2.write(f'{R4[0]} {fwd_bc}-{rev_bc}\n{R4[1]}\n{R4[2]}\n{R4[3]}\n') #output the unknown rev record with barcodes appended to the end of the header
            elif fwd_bc == rev_bc:        #if the fwd barcode is equal to the rev comp of rev barcode, only check this if previous'if' conditional false
                if bc_pair not in matched_dict: #if these barcodes are not in the matched dictionary
                    matched_dict[bc_pair] = 1 #initialize the value to one
                else: #if the barcodes are in matched dictionary already
                    matched_dict[bc_pair] += 1 #add to the current value with the matching key
                file_dict[f'{fwd_bc}'][0].write(f'{R1[0]} {fwd_bc}-{rev_bc}\n{R1[1]}\n{R1[2]}\n{R1[3]}\n') #output the new matched fwd records with barcodes appended to the header no matter the conditional
                file_dict[f'{fwd_bc}'][1].write(f'{R4[0]} {fwd_bc}-{rev_bc}\n{R4[1]}\n{R4[2]}\n{R4[3]}\n') #output the new matched rev records with barcodes appended to the header no matter the conditional
            else: #if its not matched or unknown must? be hopped
                if bc_pair not in hopped_dict: #if the record is not in hopped dictionary
                    hopped_dict[bc_pair] = 1   #initialize the value to one
                else: #if it is in the dictionary already
                    hopped_dict[bc_pair] += 1  #add to current value with the matching hopped key
                hopped_R1.write(f'{R1[0]} {fwd_bc}-{rev_bc}\n{R1[1]}\n{R1[2]}\n{R1[3]}\n') #output the new hopped fwd records with barcodes appended to the header no matter the conditional
                hopped_R2.write(f'{R4[0]} {fwd_bc}-{rev_bc}\n{R4[1]}\n{R4[2]}\n{R4[3]}\n') #output the new hopped rev records with barcodes appended to the header no matter the conditional
            record_count += 1  #count the numb of record in the big file to be able to get percentages later
#PRINT STATEMENTS: MATCHED, HOPPED, UNKNOWN COUNT
    for bc_pair in matched_dict:    #for the barcodes in the matched barcode dictionary
        percentage = round(((matched_dict[bc_pair]/record_count)*100), 2) #take the percentage of matched records and divide by the total record count
        print(f'For matched reads:{bc_pair}:\ntotal count= {matched_dict[bc_pair]}\npercentage= {percentage}%')

    for bc_pair in hopped_dict:    #for the barcodes in the hopped dictionary
        percentage = round(((hopped_dict[bc_pair]/record_count)*100), 2) #take the percentage of hopped records and divide by the total record count
        print(f'For the hopped reads:{bc_pair}:\ntotal count= {hopped_dict[bc_pair]}\npercentage of matched reads is: {percentage}%')

    print(f'The amount of unknown records is {unk_count}')



demux(R1, R2, R3, R4)
