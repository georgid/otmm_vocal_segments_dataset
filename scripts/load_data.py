'''
Created on Feb 7, 2017

@author: joro
'''
import os
import mir_eval
import numpy as np

def load_excerpt(dir_name):
    excerpt_URI = os.path.join(dir_name, 'excerpt.txt')
    start_ts, end_ts, _ = mir_eval.io.load_delimited(excerpt_URI, [float,float,str],delimiter='\t')
    return float(start_ts[0]), float(end_ts[0])


def load_beat_anno(beats_URI, start_ts):
    '''
    load beat annotations 
    
    Returns
    -------------------
    sample_labels: list
        beat labels at each frame 
    '''
    
    try:
        beat_ts, beat_labels = mir_eval.io.load_delimited(beats_URI,[float,int],delimiter=',')
    except:
        beat_ts, beat_labels = mir_eval.io.load_delimited(beats_URI,[float,int],delimiter='\t')
    
    # shift with excerpt

    beat_ts = np.array(beat_ts)
    beat_ts += start_ts
    
    return beat_ts.tolist(), beat_labels