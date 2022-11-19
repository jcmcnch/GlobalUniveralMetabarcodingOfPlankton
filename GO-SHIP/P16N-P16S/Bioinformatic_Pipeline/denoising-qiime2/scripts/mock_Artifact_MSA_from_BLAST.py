#!/usr/bin/env python

from Bio import SeqIO
import subprocess
import re
import csv
import argparse

parser = argparse.ArgumentParser(description='This script uses tsv output from a BLAST search against the exact mock sequences to retrieve the sequences of both the mock and 1-mismatches to the mock identified by BLAST. They are output in a fasta-formatted MSA so you can see where the mismatches are and what type they are.')

parser.add_argument('--blastresults', help='A tab-separated file blast output file generated by blasting the extra eASVs you find in your mock sequences (i.e. those not exactly matching the mocks).')

parser.add_argument('--repseqs', help='Your eASV sequences as generated by deblur or DADA2. If you are running the script in the folder containing the file and did not rename the file, there is no need to specify this parameter.', default='dna-sequences.fasta')

parser.add_argument('--mockseqs', help='The exact mock sequences. Default file is for 16s, change if you want to run for 18s.', default='/home/db/in-silico-mocks/BLAST-db/16s/mocks_all_non-redundant-renamed-ref.fasta')

args = parser.parse_args()

hashArtifacts = {}

for astrLine in csv.reader(open(args.blastresults), csv.excel_tab):

    if astrLine[4].strip() == "1":

        if astrLine[1] not in hashArtifacts:

            hashArtifacts[astrLine[1]] = []
            hashArtifacts[astrLine[1]].append(astrLine[0])

        elif astrLine[1] in hashArtifacts:

            hashArtifacts[astrLine[1]].append(astrLine[0])

hashMSA = {}

for record in SeqIO.parse(args.mockseqs, "fasta"):

    sequence = str(record.seq).upper()
    header = str(record.id)

    if header in hashArtifacts.keys():
        hashMSA[header] = sequence

for record in SeqIO.parse(args.repseqs, "fasta"):

    sequence = str(record.seq).upper()
    header = str(record.id)

    for key in hashArtifacts.keys():
        if header in hashArtifacts[key]:
            hashMSA[header] = sequence

for key in hashArtifacts.keys():

    outfile = key + ".artifacts.MSA.fasta"

    with open(outfile, "w+") as output_file:
        output_file.write(">" + key + "\n")
        output_file.write(hashMSA[key] + "\n")

        for artifact in hashArtifacts[key]:
            output_file.write(">" + artifact + "\n")
            output_file.write(hashMSA[artifact] + "\n")    
