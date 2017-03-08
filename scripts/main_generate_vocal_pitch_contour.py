import json
from get_vocal_recordings import get_recIDs_OK_vor_vocal
from main import generate_voiced_pitch_contours
   
if __name__ == '__main__': # intersect 
   
   ############# generate vocal pitch contour by intersecting pitch contour with manual vocal annotation (.vocal_anno) or  automatic (.vocal_section_anno)
    f = open( '../data/sarki_vocal_rec_ids.json', 'r')
    sarki_vocal_rec_ids = json.load(f)
    sarki_vocal_rec_ids = get_recIDs_OK_vor_vocal(sarki_vocal_rec_ids) # this line needed if using .vocal_section_anno
    for recID in sarki_vocal_rec_ids:
        generate_voiced_pitch_contours(recID, '../data/') # change file extetnsion in this method 
    
