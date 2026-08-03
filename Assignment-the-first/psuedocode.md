**problem:**
 
 We need to look through library prep files and demultiplex them and start a running sum of three categories: index matches, index hopping, and unknown indexes. This running sum will allows us to report the % of the indezes that fell into each of the categories. Each index pair will then be written to a new fastq file depending on which category it fell into ex:) 

matched file names: (barcode).R1/R2(rev strand prev R4).fq
unknown file names(2): unk.R1.fq, unk.R2.fq
hopped file names(2): hopped.R1.fq, hopped.R2.fq

when we write these reads to their corresponding file we will append the barcode to the end the HEADER of both reads that corresond to the index pairs (ex. AAAAAA(ind1)-CCCCCC(ind2))
By the end of this demultiplex there should be 48 fastq files (2 per 24 index), 2 unknown files, and 2 hopped files.

after this process we can report the number of read pairs with properly matched indexes (per pair), the number of reads with index hopping present, and the number of unknown indexes(qual score too low or Ns present)
functions: do I need more?!?!

def reverse_comp ()
    ```docstring```
    input: "ATCG"
    expected output: "CGAT"
def demultiplex ()
    ```docstring```
    input: two matching indexes corresponding to a read
    expected output: write out to a new file with the full read and indexes appended to the end of he header

psuedocode:

shebang

open indexes file
    loop over it
        save indexes to a set
initialize matched dictionary
initialize hopped dictionary
open four read files (R1, R2, R3, R4)
    readline sequence line for R1, R2, R3, R4
        if R2 or R3 barcodes contain N's
            write R1 record R1 unknown file and append index to header
            +1 to unknown counter
            write R4 record R4 unknown file and append index to header
        elif R2 and R3 barcodes match (reverse complement fxn)
            if R2 and R3 reversed are in set
                write R1 record R1 matched file and append index to header
                add to matched dictionary -- R2/R3 is key and value is +1
                write R4 record R4 matched file and append index to header
            elif R2 and R3 reversed not in set
                write R1 record R1 unknown file and append index to header
                +1 to unknown counter
                write R4 record R4 unknown file and append index to header
        elif R2 and R3 barcodes don't match
            if R2 and R3 reversed are in set
                write R1 record R1 hopped file and append index to header
                add to hopped dictionary -- R2/R3 is key and value is +1
                write R4 record R4 hopped file and append index to header
- add in quality score cut off to logical statement 
        else
            write R1 record R1 unknown file and append index to header
            +1 to unknown counter
            write R4 record R4 unknown file and append index to header