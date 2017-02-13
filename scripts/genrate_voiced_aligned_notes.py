'''
Created on Feb 12, 2017

@author: georgid
'''
import sys
from main import generate_voiced_notes




if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Syntax: command <MBID> <output_dir>')
    recID = sys.argv[1]
    output_dir = sys.argv[2]
    
    
    generate_voiced_notes(recID, output_dir)