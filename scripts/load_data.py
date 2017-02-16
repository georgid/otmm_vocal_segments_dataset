'''
Created on Feb 7, 2017

@author: joro
'''
import os
import mir_eval
import numpy as np
from mir_eval.io import load_delimited
import sys



def load_aligned_notes(URI_aligned_notes, offset=0):
    '''
    load annotataion of aligned notes. exported as notes layer from SV 
    '''
    try:
        onsets_ts, offset_ts, pitches, note_numbers = load_delimited(URI_aligned_notes, [float, float, float, int])  # annotated with SV regions layer with last column note index
    except: # sometimes note index is missing
        try:
            onsets_ts, offset_ts, pitches, note_numbers = load_delimited(URI_aligned_notes, [float, float, float, str])
        except:
            onsets_ts, offset_ts, pitches = load_delimited(URI_aligned_notes, [float, float, float])
        note_numbers =   [-1] * len(onsets_ts)
    onsets_ts = np.array(onsets_ts)
    onsets_ts += offset
    
#     offset_ts = np.array(offset_ts)
#     offset_ts += offset
    
    notes = zip (onsets_ts, offset_ts, pitches, note_numbers)
    return np.array(onsets_ts), notes
    
def load_excerpt(URI_excerpt):
    start_ts, end_ts, _ = mir_eval.io.load_delimited(URI_excerpt, [float,float,str],delimiter='\t')
    return float(start_ts[0]), float(end_ts[0])


def modify_time(onsets_ts_URI, excerpt_URI):
        start_ts, _ = load_excerpt(excerpt_URI)
        onsets_ts, notes = load_aligned_notes(onsets_ts_URI, start_ts)
        
#         starts, values, durations = load_delimited(onsets_ts_URI, [float, float, float])
#         starts = np.array(starts)
#         starts += start_ts
#         notes =  zip (starts.tolist(), values, durations)
        
        import csv
        with open(onsets_ts_URI + '_', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(notes)

        

def load_beat_anno(beats_URI, start_ts=0):
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


if __name__ == '__main__':
    a = '/Users/joro/workspace/otmm_vocal_segments_dataset/data/92ef6776-09fa-41be-8661-025f9b33be4f/excerpt.txt'
    b = '/Users/joro/workspace/otmm_audio_score_alignment_dataset/data/ussak--sarki--duyek--aksam_oldu_huzunlendim--semahat_ozdenses/92ef6776-09fa-41be-8661-025f9b33be4f/alignedNotes_for_cut_audio_not_from_zero.txt'
#     a = sys.argv[2]
#     b = sys.argv[1]
    
    # 
    modify_time(b, a)
    