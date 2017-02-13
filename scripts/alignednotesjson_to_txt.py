
# coding: utf-8

# In[4]:

import json
import  csv
import os
from compmusic.extractors.makam.fetch_tools import getWork
from compmusic import dunya
import sys

musicbrainzid = '92ef6776-09fa-41be-8661-025f9b33be4f'
symbTrName = 'ussak--sarki--duyek--aksam_oldu_huzunlendim--semahat_ozdenses'
work_mbid = 'c6e43ac6-4a18-42ab-bcc4-46e29360051e' # TODO: use mb to get work

musicbrainzid = 'c7a31756-a7d5-4882-bdf7-9c6b23493597' # TODO
symbTrName = 'rast--sarki--duyek--hicran_olacaksa--ferit_sidal' # TODO
work_mbid = '5f7c74b7-8af6-4ab7-a504-f694bbd347e9' # TODO: use mb to get work


# notes_URI = '/Users/joro/Downloads/derivedfiles_' + musicbrainzid + '/jointanalysis-notes-1-1.json'
#### create recording dir
# notes = json.load(open(notes_URI))

def aligned_notes_to_json(musicbrainzid):
	notes = dunya.docserver.get_document_as_json(musicbrainzid, "jointanalysis", "notes", 1, version="0.1")
	w =  getWork( musicbrainzid)
	work_mbid = w['mbid']
	
	symbtr = dunya.makam.get_symbtr(work_mbid)
	symbTrName = symbtr['name']
	
	symbTr_dir = '/home/georgid/workspace/otmm_audio_score_alignment_dataset/data/' + symbTrName
	if not os.path.isdir(symbTr_dir):
		os.mkdir(symbTr_dir)
	recID_dir = symbTr_dir + '/' + musicbrainzid
	if not os.path.isdir(recID_dir):
		os.mkdir(recID_dir)
		
	URI_notes_aligned_output = os.path.join(recID_dir,'alignedNotes.txt') # convetion name for this repo 
	
	f = open(URI_notes_aligned_output,'wb')
	writer = csv.writer(f, delimiter='\t')
	work_notes = notes[work_mbid]
	
	for note in work_notes: # read intercvals
	    
	    times = note['interval']
	    # times[0] -= 32.04
	    # times[1] -= 32.04
	    row = times
	    
	    row.append(note['performed_pitch']['value'])
	    row.append(note['index_in_score'])
	    
	    writer.writerow(row)
	
	f.close()
	print 'written file ' + URI_notes_aligned_output
	return URI_notes_aligned_output

if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit('Syntax: command MBID ')
	musicbrainzid = sys.argv[1]
	aligned_notes_to_json(musicbrainzid)
