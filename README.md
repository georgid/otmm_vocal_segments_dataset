		
Annotations of vocal segments in Turkish Makam on different levels.  
comments about dataset  here:
https://docs.google.com/spreadsheets/d/1f9wyxB6emGHvVGUhIjNQwSxxhOJhPAdNzA2BieyKVXw/edit?usp=sharing

# Annotation levels:
## vocal_sections_anno: tab-separated file
	audio regions that correspond to sections from score with singing voice present. 
	fetched from sectionLinks in ``generate_voiced_sections`` from ``scripts/main.py`` and manually checked after that.

## vocal_anno: tab-separated 
	audio regions with singing voice present. for singing voice detection. 
	TODO: create manually

## vocal_onsets_anno: tab-separated
	timestamps for onsets of singing voice. 
	Done by intersecting manually annotated onsets with vocal_anno files with script ``generate_voiced_onsets`` in ``scripts/main.py``. Manually annotated onsets taken from https://github.com/MTG/otmm_audio_score_alignment_dataset/tree/vocal-only-annotation/  
	NOTE: if a syllable starts with unvoied sound, onsets is annotated at the beginning of the voiced part (e.g.  'Shi'  will have the onset beginning at i). However, if a background instrument plays same pitch simultaneously to voice, the vocal onset is marked at the instrument onset, as if it were the vocal onset (because predominant melody will include the instrumental pitch). 

## beats 
	timestamps of beats (usually annotated only first 60 seconds)


