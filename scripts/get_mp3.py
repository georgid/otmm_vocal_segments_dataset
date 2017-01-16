from compmusic import dunya
import sys
import csv
import compmusic.extractors.makam.fetch_tools as ft

if len(sys.argv) != 3:
	sys.exit('Syntax: command MBID outputDir')
musicbrainzid = sys.argv[1]
outputDir = sys.argv[2]
# musicbrainzid = 'c7a31756-a7d5-4882-bdf7-9c6b23493597'
# outputDir = '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/turkish_makam_vocal_segments_dataset/data/c7a31756-a7d5-4882-bdf7-9c6b23493597/'
dunya.set_token("69ed3d824c4c41f59f0bc853f696a7dd80707779")

for_polyphonic  = 1
ft.fetch_audio_wav(outputDir, musicbrainzid, for_polyphonic)

# mp3FileURI = dunya.makam.download_mp3(musicbrainzid, outputDir)