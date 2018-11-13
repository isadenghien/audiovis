#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:22:08 2018

@author: id983365
"""

import csv
import io

import pandas

csv_file = '/neurospin/unicog/protocols/IRMf/New_localizers/localizer_standard/exportEprime.csv'
#file_r = csv.reader(io.open(csv_file, 'r', encoding='utf-16-le'), delimiter='\t')
##stimlist = csv.reader(io.open(listfile, 'r', encoding='utf-8-sig'), delimiter='\t')
#encoding='utf-16-le'
#for row in file_r :
#    print(row)

df = pandas.read_csv(csv_file, sep = '\t', header = 0, encoding ='utf-16-le')
for i, r in enumerate(df.itertuples(), 1):
#    if r['manip']
  print(r[65]) # imprime le nom de la colonne
  
  
 csv_file = '/neurospin/unicog/protocols/IRMf/New_localizers/localizer_standard/exportEprime.csv'
#file_r = csv.reader(io.open(csv_file, 'r', encoding='utf-16-le'), delimiter='\t')
##stimlist = csv.reader(io.open(listfile, 'r', encoding='utf-8-sig'), delimiter='\t')
#encoding='utf-16-le'
#for row in file_r :
#    print(row)

df = pandas.read_csv(csv_file, sep = '\t', header = 0, encoding ='utf-16-le')
for i, x in enumerate(df, 1):
    print(i)
    print(x) # imprime le nom de la colonne
 