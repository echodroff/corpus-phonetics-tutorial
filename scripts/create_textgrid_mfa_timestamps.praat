# create_textgrid_mfa_timestamps.praat
# Written by E. Chodroff
# Oct 23 2018

# This script takes as input a series of text files, each with a corresponding wav file
# The text files and wav files are in the same directory and have the exact same name
# The text file has three columns and is tab-delimited
# The first column has the start time of the utterance
# The second column has the end time of the utterance
# The third column has the utterance

### CHANGE ME!
dir$ = "/Users/Eleanor/Desktop/align_input/"
###

Create Strings as file list: "files", dir$ + "*.txt"
nFiles = Get number of strings

for i from 1 to nFiles
	selectObject: "Strings files"
	filename$ = Get string: i
	basename$ = filename$ - ".txt"
	
	# read in transcript
	Read Table from tab-separated file: dir$ + basename$ + ".txt"
	nRows = Get number of rows

	# get names of columns
	startCol$ = Get column label: 1
	endCol$ = Get column label: 2
	uttCol$ = Get column label: 3

	# read in wav
	Read from file: dir$ + basename$ + ".wav"
	dur = Get total duration

	# create TextGrid
	To TextGrid: "utt", ""ß

	# add in boundaries and text
	for j from 1 to nRows
		selectObject: "Table " + basename$
		start = Get value: j, startCol$
		end = Get value: j, endCol$

		# make sure end boundary does not equal the duration of the wav file
		if end >= dur
			end = dur-0.001
		endif
		
		# insert utterance text
		utt$ = Get value: j, uttCol$
		selectObject: "TextGrid " + basename$
		Insert boundary: 1, start
		Insert boundary: 1, end
		labelInt = Get interval at time: 1, end-0.0015
		Set interval text: 1, labelInt, utt$
	endfor

	# save textgrid
	selectObject: "TextGrid " + basename$
	Save as text file: dir$ + basename$ + ".TextGrid"
	
	# clean up
	select all
	minusObject: "Strings files"
	Remove
endfor

