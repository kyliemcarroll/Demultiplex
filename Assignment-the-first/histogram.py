#!/usr/bin/env python

import argparse
import bioinfo
import matplotlib.pyplot as plt
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="Program to modify file name ")
    parser.add_argument("-f", "--file_name", help="Desired filename")
    parser.add_argument("-b", "--index_number", help="Desired index number")
    parser.add_argument("-r", "--read_number", help="Desired read number - 1,2,3,4")
    return parser.parse_args()
args = get_args()

f = args.file_name
b = int(args.index_number)
r = int(args.read_number)

def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    while len(lst) < b:
        lst.append(value)
    return(lst)
my_list: list = []
my_list = init_list(my_list)

def populate_list(fastq: str) -> tuple[list, int]:
    sum_list = init_list([])
    with gzip.open(f, "rt") as fh:
        row = 0
        for line in fh:
            row += 1
            row%4 ==0
            if row%4 ==0:
                qual_score = line.strip("\n")
                for index, c in enumerate(qual_score):
                    sum_list [index]= sum_list[index] + bioinfo.convert_phred(c)
    return sum_list, row
my_list, row = populate_list(f)

for index, v in enumerate(my_list):
    my_list[index] = v/(row/4)

#matplot bar plot
x = range(b)
y = my_list

plt.bar(x,y)
plt.title(f"Mean Phred Quality Scores at each Index -R{r}")
plt.xlabel("Base Index Position")
plt.ylabel("Mean Quality Score")
plt.savefig(f'R{r}_scores.png')