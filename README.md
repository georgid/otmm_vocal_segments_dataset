		
Annotations of vocal segments in Turkish Makam on different levels.  
------------------------------------------------------------

status of dataset here:
https://docs.google.com/spreadsheets/d/1f9wyxB6emGHvVGUhIjNQwSxxhOJhPAdNzA2BieyKVXw/edit?usp=sharing



# Annotation levels:
## vocal_sections_anno: tab-separated file
audio regions that correspond to sections from score with singing voice present. 
fetched from sectionLinks in `generate_voiced_sections` from `scripts/main.py` and manually checked after that.

## vocal_anno: tab-separated 
audio regions with singing voice present. for singing voice detection. 
TODO: create manually

## vocal_onsets_anno: tab-separated
timestamps for onsets of singing voice. 

Done by intersecting automatic aligned onsets with vocal_anno files with script `genrate_voiced_aligned_notes` 

Then manually adjust onsets in SV and push new file with extension .alignedNotes_vocal.txt to 
https://github.com/MTG/otmm_audio_score_alignment_dataset/tree/vocal-only-annotation/  
	NOTE: Annotation strategy: 
	if a syllable starts with unvoied sound, onsets is annotated at the beginning of the voiced part (e.g.  'Shi'  will have the onset beginning at i). However, if a background instrument plays same pitch simultaneously to voice, the vocal onset is marked at the instrument onset, as if it were the vocal onset (because predominant melody will include the instrumental pitch). 

then use `generate_vocal_onsets()` -> read the first row


## beats 
timestamps of beats (usually annotated only first 60 seconds)
cp ~/Documents/TurkishMakam/an data/<MBID>

## wav file (download from dunya )
`python scripts/get_mp3.py a2e650dc-8822-4647-9f4c-c41c0f81b601 data/`


---------------------------------
FOR MORE DEATAILS ON how to generate each annotation see: 
see `steps_annotate_data`


