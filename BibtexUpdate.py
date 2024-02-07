import numpy as np
import spires
import re
import sys

"""
 Usage: python BibtexUpdate.py <path to bibtex file>
 The code queries the inspirehep data base for updtes of entries in a bibtex file
 and reports output.
 andreas.juttner@cern.ch

 Requries: spires (https://www.stringwiki.org/wiki/SPIRES_script)
"""

path=sys.arg[1]
cnt=0
beprint=0
bjournal=0
for line in open(path, 'r'):
   match_ampersand = re.findall('^@',line)
   if match_ampersand and cnt==0:
    current=line
    cnt=1
    match_ampersand=[]
    continue
   cnt+=1
   match_eprint = re.findall('eprint',line.split('=')[0])
   if match_eprint:
    eprintline=line
    beprint=1
   match_journal = re.findall('journal',line)
   if match_journal:
    bjournal=1
   match_ampersand = re.findall('^@',line)
   #print match_ampersand
   if match_ampersand:
    curr=re.compile("^@.*{(.*),").match(current).groups()
    if beprint==0:
     print("############################################################################")
     print("%s has no eprint tag in current input file"%curr[0])
    if ((bjournal==0) and (beprint==1)):
     eprint=re.findall('\".*',eprintline)[0][1:-2]
     rType, ref = spires.findRefType(eprint)
     print(rType,ref)
     print("############################################################################")
     print("%s has no journal entry in current input file "%curr[0])
     inputString = spires.getBiBTeX(ref,rType).decode("utf-8")
     new = inputString.split('\n')
     for line2 in new:
      if re.findall('journal',line2):
       print("this entry now has a journal entry:\n")
       print(inputString)
       continue
    beprint=0
    bjournal=0
    current=line
   

