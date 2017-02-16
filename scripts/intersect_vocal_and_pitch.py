'''
Created on Oct 5, 2016

@author: georgid
'''

import json
import numpy as np

from compmusic import dunya
import os
import subprocess
import sys
from mir_eval.io import load_intervals, load_delimited
import tempfile
from alignednotesjson_to_txt import aligned_notes_to_json
from load_data import load_aligned_notes
dunya.set_token("69ed3d824c4c41f59f0bc853f696a7dd80707779")
import logging
import mir_eval
from compmusic.extractors.makam.fetch_tools import fetchNoteOnsetFile, getWork, download_wav



def intersect_section_links(pitch_contour, voiced_intervals):
    '''
    intersect the given pitch contour with given vocal sections
    
    Parameters
    -------------------
    pitch_contour: list of (ts, pitch) tuples
        given pitch contour
    
    voiced_intervals: list, shape=(n,2)
        vocal intervals
    
    Return
    -------------------
    pitch_contour:  list of (ts, pitch)
        pitch contour with zero on non-intersected parts
    
    
    ''' 
    pitch_contour = np.array(pitch_contour)
    timestamps = pitch_contour[:,0]
    labels = ['voiced'] * len(voiced_intervals)
    timestamp_labels = mir_eval.util.interpolate_intervals(voiced_intervals, labels, timestamps, fill_value=None) # timestamp_labels correspond to timestamps
    timestamp_labels = np.array(timestamp_labels)
    indices_nonvoiced = np.where(timestamp_labels!='voiced')[0]
    pitch_contour[indices_nonvoiced,1] = 0 # make non-vocal have zero pitch
    return pitch_contour   


def sectionLinks_to_intervals(sectionLinks):
    '''
    form sectionLink objects to simple list-like interval objects
    '''
    vocal_intervals = []
    for sectionLink in sectionLinks:
            if 'VOCAL' not in sectionLink['name']:
              continue
            startTime = sectionLink['time'][0]
            endTime = sectionLink['time'][1]
            vocal_intervals.append([startTime,endTime])
    return np.array(vocal_intervals)






# parse section links 
# sections_URI = '/home/georgid/Downloads/derivedfiles_ba1dc923-9b0e-4b6b-a306-346bd5438d35/ba1dc923-9b0e-4b6b-a306-346bd5438d35-jointanalysis-0.1-sections-1.json'

def generate_vocal_segments(musicbrainzid, voiced_intervals, for_pitch=True, from_automatic_alignment=False):
    '''
    make annotation of vocal Vs novocal by intersecting  extracted pitch and section links
    NOTE: intrasection SAZ interludes will remain marked falsely as vocal, so do a successive check by listening
    
    Parameters
    --------------------------
    for_pitch: boolean
        True: for pitch (which is essentially onsets with assigned pitch)
        False: for onsets
        
    from_automatic_alignment: 
        if true, get alignment from Sertan's score-to-audio alignment. Careful not to override some existing onset annotation
        if not true look for automatically annotated onsets. 
    Returns
    ----------------------
    intersected_pitch_contour: nd.array
        pitch contour of only vocal sections
    '''
    if for_pitch: # get pitch from best algorithm. assume it is best estimate of tru e pitch contour
        try:
            pitch_data = dunya.docserver.get_document_as_json(musicbrainzid, "jointanalysis", "pitch", 1, version="0.1")
            pitch_series = pitch_data['pitch']
        except:
            logging.error("no initialmakampitch series could be downloaded. for rec  {}".format(musicbrainzid))
            return None
        selected_vocal_onsets =  intersect_section_links(pitch_series, voiced_intervals) # onsets with pitch
    
    else: 
        if from_automatic_alignment:
            onsets_ts_URI = aligned_notes_to_json(musicbrainzid)  
        else: # fetch onsets from annotation
            dir = tempfile.mkdtemp()
            try:
                onsets_ts_URI = fetchNoteOnsetFile(musicbrainzid, dir , 'alignedNotes.txt') # annotated 
    #             onsets_ts_URI = '/Users/joro/Documents/lyrics-2-audio-test-data/' +  musicbrainzid  + '/' + musicbrainzid + '.vocal_onsets.pYIN' # estimated
            except:
                print 'No alignedNotes.txt for recording. Check internet connection ' + str(musicbrainzid)
                return None
        
#         onsets_ts_URI = '/Users/joro/workspace/otmm_audio_score_alignment_dataset/data/ussak--sarki--duyek--aksam_oldu_huzunlendim--semahat_ozdenses/92ef6776-09fa-41be-8661-025f9b33be4f/alignedNotes.txt'
        onsets_ts, notes = load_aligned_notes(onsets_ts_URI)
        selected_vocal_onsets = intersect_vocal_onsets(onsets_ts, notes, voiced_intervals) # vocal onsets 
        
    return selected_vocal_onsets, onsets_ts_URI


def fetch_voiced_sections(musicbrainzid):
    '''
    fetch audio regions that correspond to sections from score with singing voice present
    '''
    ########## get automatically detected section links
    try:
        sections_all_works = dunya.docserver.get_document_as_json(musicbrainzid, "jointanalysis", "sections", 1, version="0.1")
#         sections_all_works = dunya.docserver.get_document_as_json(musicbrainzid, "lyrics-align", "sectionlinks", 1, version="0.1")
        
    except dunya.conn.HTTPError:
        logging.error("section link for {} is missing".format(musicbrainzid))
        return None

    work = getWork( musicbrainzid)
    sectionLinks = sections_all_works[work['mbid']]
    voiced_sections = sectionLinks_to_intervals(sectionLinks)
    return voiced_sections



def intersect_vocal_onsets(onsets_ts, notes, voiced_intervals):
    '''
    intersect onsets (could be annotated) with intervals 
    and return only the ones within the given intervals
    
    
    Parameters
    -----------------------------
    onsets_ts: list shape=m
         timestamps of all onsets
    
    Returns
    -----------------
    vocal_onsets
     
    '''
    vocal_notes = []
    
    voiced_and_nonvoiced_intervals, labels  = add_novocal_intervals(voiced_intervals)   
    aligned_labels = mir_eval.util.interpolate_intervals(voiced_and_nonvoiced_intervals, labels, onsets_ts, fill_value=None)
    for note, label in zip(notes,aligned_labels):
        if label == 'vocal': # the rest of the labels will be None
            vocal_notes.append(note)
    return np.array(vocal_notes)   


def add_novocal_intervals(voiced_intervals):
    TS_AT_END_OF_REC = 10000
    voiced_boundaries = mir_eval.util.intervals_to_boundaries(voiced_intervals)
    voiced_boundaries = np.insert(voiced_boundaries, 0, -1) # prepend -1
    voiced_boundaries = np.append(voiced_boundaries,TS_AT_END_OF_REC) # append some final ts
       
        ##### assign vocal and novocal labels
    boundary_labels = ['vocal'] * len(voiced_boundaries)
    for i in range(0,len(boundary_labels),2):
            boundary_labels[i] = 'novocal'
    voiced_intervals2 = mir_eval.util.boundaries_to_intervals(voiced_boundaries)
    return voiced_intervals2, boundary_labels

