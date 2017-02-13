
# coding: utf-8

# In[21]:

from csv import reader, writer
from tempfile import NamedTemporaryFile
import shutil
import sys
from load_data import load_excerpt
import os

if len(sys.argv) != 5:
    sys.exit('Syntax: command <URI.beats> <URI.excerpt> <output_dir> <MBID>')
uri_excerpt = sys.argv[2]
MBID = sys.argv[4]


start_ts, end_ts = load_excerpt(uri_excerpt)
URI_beats = sys.argv[1]

fout = NamedTemporaryFile(delete=False)


URI_target = os.path.join( sys.argv[3],   MBID+ '.beats' )
with open(URI_beats,'rb') as fin, fout:
    w = writer(fout, delimiter=',')

    reader = reader(fin, delimiter=',')
    rows = [r for r in reader]
    
    for row in rows:
            row[0]= float(row[0]) + start_ts
            w.writerow(row)
# rename to original file name or to another name
shutil.move(fout.name, URI_target)            
print 'written file ' + URI_target




