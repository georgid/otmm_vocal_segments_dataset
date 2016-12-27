
# coding: utf-8

# In[21]:

from csv import reader, writer
from tempfile import NamedTemporaryFile
import shutil

offset = 1.135
offset = 4.16
fout = NamedTemporaryFile(delete=False)
URI = '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/turkish_makam_vocal_segments_dataset/data/f5a89c06-d9bc-4425-a8e6-0f44f7c108ef/f5a89c06-d9bc-4425-a8e6-0f44f7c108ef.beats'
URI_target = URI + '_'
with open(URI,'rb') as fin, fout:
    w = writer(fout)

    reader = reader(fin)
    rows = [r for r in reader]
    
    for row in rows:
            row[0]= float(row[0]) + offset
            w.writerow(row)
shutil.move(fout.name, URI_target)            


# In[ ]:



