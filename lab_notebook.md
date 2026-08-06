# Lab Notebook — Demultiplex

**Base Directory**

`/projects/bgmp/hvsev/bioinfo/Bi622/Demultiplex`

*(within Talapas)*

**Environment / Versions:**

*Compute environment:*

`bgmp compute nodes`

*Software/package versions:*

`bash 4.4.20`
`python 3.14.6`

**Data Source:**

Sequencing data generated from the 2017 BGMP cohort's library preps
```
DATA=/projects/bgmp/shared/2017_sequencing/
R1=$DATA/1294_S1_L008_R1_001.fastq.gz
R2=$DATA/1294_S1_L008_R2_001.fastq.gz
R3=$DATA/1294_S1_L008_R3_001.fastq.gz
R4=$DATA/1294_S1_L008_R4_001.fastq.gz
```
---

### [07-25-2026]

`Assignment the first - Part 2`

`Pseudocode`

**Daily Log:**

*Problem:*
We need to look through library prep files and demultiplex them and start a running sum of three categories: index matches, index hopping, and unknown indexes. This running sum will allows us to report the % of the indezes that fell into each of the categories. Each index pair will then be written to a new fastq file depending on which category it fell into ex:) 

matched file names: (barcode).R1/R2(rev strand prev R4).fq
unknown file names(2): unk.R1.fq, unk.R2.fq
hopped file names(2): hopped.R1.fq, hopped.R2.fq

when we write these reads to their corresponding file we will append the barcode to the end the HEADER of both reads that corresond to the index pairs (ex. AAAAAA(ind1)-CCCCCC(ind2))
By the end of this demultiplex there should be 48 fastq files (2 per 24 index), 2 unknown files, and 2 hopped files.

after this process we can report the number of read pairs with properly matched indexes (per pair), the number of reads with index hopping present, and the number of unknown indexes(qual score too low or Ns present)

*Functions:*
do I need more?!?!

```
def reverse_comp ()
    ```docstring```
    input: "ATCG"
    expected output: "CGAT"
```
```
def demultiplex ()
    ```docstring```
    input: two matching indexes corresponding to a read
    expected output: write out to a new file with the full read and indexes appended to the end of the header
```
```
def read_record () #added in later
'''docstring'''
input: 4 fastq files
expected output: reading all four file four lines (1 record) at a time
```

*Pseudocode:*
```
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
```
---
### [07-29-2026]

`Assignment the first - Part 1`

`Data Exploration & Creating Histograms`

**Daily Log**

*I want to successfully run my python script wrapped in a shell script to have the output be histograms displaying the mean quality score at each index for each of the files.*

**Scripts run:**

[histogram.py](histogram.py)

[R1.sh](R1.sh)

[R2.sh](R2.sh)

[R3.sh](R3.sh)

[R4.sh](R4.sh)

**Commands run:**

```
sbatch R1.sh
sbatch R2.sh
sbatch R3.sh
sbatch R4.sh
```

**Job resource usage (`/usr/bin/time -v` summary from Talapas):**
```
Command being timed: R1: "python histogram.py -f /projects/bgmp/shared/2017_sequencing//1294_S1_L008_R2_001.fastq.gz -b 8 -r 2"
Maximum resident set size (kbytes): 70816
Percent of CPU this job got: 99%
Exit status: 0

Command being timed: R2: "python histogram.py -f /projects/bgmp/shared/2017_sequencing//1294_S1_L008_R1_001.fastq.gz -b 101 -r 1"
Maximum resident set size (kbytes): 71588
Percent of CPU this job got: 99%
Exit status: 0

Command being timed: R3: "python histogram.py -f /projects/bgmp/shared/2017_sequencing//1294_S1_L008_R3_001.fastq.gz -b 8 -r 3"
Maximum resident set size (kbytes): 70588
Percent of CPU this job got: 99%
Exit status: 0

Command being timed: R4: "python histogram.py -f /projects/bgmp/shared/2017_sequencing//1294_S1_L008_R4_001.fastq.gz -b 101 -r 4"
Maximum resident set size (kbytes): 71268
Percent of CPU this job got: 99%
Exit status: 0
```
---
### [07-30-2026]

`Assignment the second`

`Script Feedback`

**Daily Log**

*I recieved feedback on my pseudocode.. here's what I incorporated:*

```
From Imre:
It seems like this is checking that both R2 and R3 are not in the set and then writing to the unknown files. The records should be written to unknown if either index isn't in the set. I think you can just replace this with an 'else' since the preceding if statement checks that both are in the set.
```
```
From Robbie:
You mentioned that you’d open all input files and read the sequence line, but you might want to capture the whole record first, (like we did in… some assignment) then access the sequence line and execute the code. That way you have the record ready to write out when you determine which bucket to put it in. You may have implied that, so apologies if so!
```
```
From Kenlyn:
Also the per-pair index counting is set up correctly through the matched and hopped dictionaries by using the index combos as keys and values are the counts, but the algorithm never shows the final step of returning or printing those values. Make sure to report those numbers. Could also consider initializing the dictionaries with all known pairs/combos so every combo appears in the report even if its count is zero.

I'd flush out both functions with descriptive docstrings, and fill in the headers with their parameters and a return even if just the types of objects. Seems like the logic for demultiplex is outlined in the code above already. You could do a function involved in quality score cutoff, but you could also just set the quality score cutoff.
```

---
### [08-03-2026]

`Assignment the third`

`Starting Demultiplex Functions & Updating Bioinfo.py & Creating the Output Files`

**Daily Log**

*Today, I got to start writing my demultiplex script. I started out by defining my functions I know I wanted to include in my script. As I was writing my script I realzied I should just create a read_record function to make my life easier... So I did end up addding that. I also initalized my set of barcodes and populated it. I then made my file dictionary and passed it my barcode set to be able to make 48 uniquely labeled files, 24 for R1(fwd file) and 24 for R2(rev file previously R4). I then opened my unknown and hopped files. In total my script so far opening up and creating 52 files. Yay!*

**Scripts run:**

[demultiplex.py](demultiplex.py)

**Adding to Bioinfo.py**

[bioinfo.py](bioinfo.py)


```
def read_record(fastq):
    '''records the first 4 lines in a fastq file = record'''
    record = []
    for i in range(4):
        record.append(fastq.readline().strip("\n"))
    return(record)
```

```
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
```

**Creating Barcodes Set**

*Path:*

```
barcodes = "/projects/bgmp/shared/2017_sequencing/indexes.txt"
```

```
barcodes_set = set()                                #initializing my set
with open(barcodes, "r") as fh:
    for line in fh:
        if not line.startswith("sample"):           #cutting out header label info
            column = line.strip("\n").split("\t")   #spliting the tab sep line to help pull from it
            indexes = column [4]                    #grab just the barcode
            barcodes_set.add(indexes)  
```
**Creating Files Dictionary/Creating Unknown and Hopped Files**

*Arg Parse for Context:*

```
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
R2 = args.f2
R3 = args.f3
R4 = args.f4
ofp = args.ofp
```
```
file_dict = {}
for barcode in barcodes_set:
    file_dict[barcode] = open(f'{ofp}/{barcode}_R1.fq',"w"), open(f'{ofp}/{barcode}_R2.fq',"w")
```
```
unk_R1 = open(f'{ofp}/unk_R1.fq', "w")
unk_R2 = open(f'{ofp}/unk_R2.fq', "w")
hopped_R1 = open(f'{ofp}/hopped_R1.fq', "w")
hopped_R2 = open(f'{ofp}/hopped_R2.fq',"w")
```
---
### [08-05-2026]

`Assignment the third`

`Writing Body of Demultiplex Python Script & In Line Comments`

**Daily Log**

*Today I did the entire body of my code, and I think I am ready for running it. I had it double and triple checked. Running on the test files I made worked well. We decided to not include a quality score cut off after all due to the barcodes being very robust. I did in line comments for every line for my future self so I remember what is going on. Tommorrow I will write a bash shell script to wrap my python script in.. fingers crossed it works!* *update: famous last words there was an issue!! haha*

**Creating Demultiplex Function**

```
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
        print(f'For the hopped reads:{bc_pair}:\ntotal count= {hopped_dict[bc_pair]}\npercentage of hopped reads is: {percentage}%')

    print(f'The amount of unknown records is {unk_count}')



demux(R1, R2, R3, R4)

```

---
### [08-06-2026]

`Assignment the third`

`Fine Tuning Demultiplex Python Script & Writing Bash Script & Successful Run!`

**Daily Log**


*I wrote my shell script today and ran the script 4 seperate times after finding minor issues with fresh eyes (I needed to take a nap evidently). My arg parse paths were also ALL jumbled up. After fixing that(thank you Leslie).. my fifth run was successful!!!! YAY!!*


**Scripts run:**

[demux.sh](demux.sh)

```
#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=1
#SBATCH --job-name=demux

DATA=/projects/bgmp/shared/2017_sequencing/
R1=$DATA/1294_S1_L008_R1_001.fastq.gz
R2=$DATA/1294_S1_L008_R2_001.fastq.gz
R3=$DATA/1294_S1_L008_R3_001.fastq.gz
R4=$DATA/1294_S1_L008_R4_001.fastq.gz

OFP=/scratch/bgmp/kymc/demux

/usr/bin/time -v python demultiplex.py -f1 $R1 -f2 $R2 -f3 $R3 -f4 $R4 -ofp $OFP
```
*Final Script:*

[demultiplex.py](demultiplex.py)


**Commands run:**

```
sbatch demux.sh
```


**Job resource usage (`/usr/bin/time -v` summary from Talapas):**
Command being timed:"python demultiplex.py -f1 /projects/bgmp/shared/2017_sequencing//1294_S1_L008_R1_001.fastq.gz -f2 /projects/bgmp/shared/2017_sequencing//1294_S1_L008_R2_001.fastq.gz -f3 /projects/bgmp/shared/2017_sequencing//1294_S1_L008_R3_001.fastq.gz -f4 /projects/bgmp/shared/2017_sequencing//1294_S1_L008_R4_001.fastq.gz -ofp /scratch/bgmp/kymc/demux" 
Maximum resident set size (kbytes): 246332
Percent of CPU this job got: 68%
Exit status: 0

**Output Print Statements Data**

*All slurm output can be found in this markdown file:*

[data_output.md](data_output.md)

---