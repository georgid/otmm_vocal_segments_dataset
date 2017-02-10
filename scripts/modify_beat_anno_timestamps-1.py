
# coding: utf-8

# In[21]:

from csv import reader, writer
from tempfile import NamedTemporaryFile
import shutil
import sys
from load_data import load_excerpt
import os

if len(sys.argv) != 3:
    sys.exit('Syntax: command <data/MBID_dir> <MBID>')
data_dir = sys.argv[1]
MBID = sys.argv[2]

start_ts, end_ts = load_excerpt(data_dir)
URI = os.path.join(data_dir, MBID + '.beats') 

fout = NamedTemporaryFile(delete=False)


URI_target = URI + '_shifted'
with open(URI,'rb') as fin, fout:
    w = writer(fout, delimiter=',')

    reader = reader(fin, delimiter=',')
    rows = [r for r in reader]
    
    for row in rows:
            row[0]= float(row[0]) + start_ts
            w.writerow(row)
# rename to original file name or to another name
shutil.move(fout.name, URI_target)            
print 'written file ' + URI_target




