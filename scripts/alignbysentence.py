#!/bin/sh

#  alignbysentence.py
#  
#  Created by Eleanor Chodroff on 12/30/14.
#
import os
import sys
import getopt
import wave
import re
import os.path
import fnmatch
import csv
import align

indir = os.path.join('/Users', 'Eleanor', 'Desktop', 'MixerFiles2','pfa')
sr_override = 16000 #choose sampling rate: 8000, 11025, 16000
# at beginning of align.py, insert line: sr_models = None
mypath = "/Users/Eleanor/Documents/p2fa/model"
surround_token = "sp"
between_token = "sp"


wavestartlist = []
waveendlist = []
sentence = []
for file in os.listdir(indir):
    if fnmatch.fnmatch(file, '*.txt'):
        with open(indir + "/" + file) as f:
            wavname = file.lstrip("clean_")
            wavname = wavname.rstrip("_trans.txt")
            wavfile = indir + "/" + wavname + ".wav"
            sequence = [0]
            for line in f:
                columns = line.split(",")
                sequence.append(sequence[-1] + 1)
                wavestartlist.append(str(columns[0]))
                waveendlist.append(str(columns[1]))
                senttmp = str(columns[2])
                senttmp = senttmp.replace("\"","")
                senttmp = senttmp.replace("\n", "")
                sentence.append(senttmp)
            del sequence[-1]
            for x in sequence:
                with open(indir + "/"+"tmp.txt", 'w') as fwrite:
                    writer = csv.writer(fwrite)
                    writer.writerow([sentence[x]])
                    fwrite.close()
                    wave_start = wavestartlist[x]
                    wave_end = waveendlist[x]
                    trsfile = indir + "/" + "tmp.txt"
                    outfile = indir + "/" + wavname + "_out" + str(x) + ".TextGrid"
                    # If no model directory was said explicitly, get directory containing this script.
                    hmmsubdir = ""
                    sr_models = None
                    hmmsubdir = "FROM-SR"
                    
                    #sr_models = [8000, 11025, 16000]
                    word_dictionary = "./tmp/dict"
                    input_mlf = './tmp/tmp.mlf'
                    output_mlf = './tmp/aligned.mlf'
                    
                    # create working directory
                    align.prep_working_directory()
                    
                    # create ./tmp/dict by concatening our dict with a local one
                    if os.path.exists("dict.local"):
                        os.system("cat " + mypath + "/dict dict.local > " + word_dictionary)
                    else:
                        os.system("cat " + mypath + "/dict > " + word_dictionary)
                
                    #prepare wavefile: do a resampling if necessary
                    tmpwav = "./tmp/sound.wav"
                    SR = align.prep_wav(wavfile, tmpwav, sr_override, wave_start, wave_end)
                    
                    if hmmsubdir == "FROM-SR" :
                        hmmsubdir = "/" + str(SR)
        
                    #prepare mlfile
                    align.prep_mlf(trsfile, input_mlf, word_dictionary, surround_token, between_token)
                
                    #prepare scp files
                    align.prep_scp(tmpwav)
                    
                    # generate the plp file using a given configuration file for HCopy
                    align.create_plp(mypath + hmmsubdir + '/config')
                    
                    # run Verterbi decoding
                    #print "Running HVite..."
                    mpfile = mypath + '/monophones'
                    if not os.path.exists(mpfile) :
                        mpfile = mypath + '/hmmnames'
                    align.viterbi(input_mlf, word_dictionary, output_mlf, mpfile, mypath + hmmsubdir)
            
                    # output the alignment as a Praat TextGrid
                    align.writeTextGrid(outfile, align.readAlignedMLF(output_mlf, SR, float(wave_start)))
            del sequence[:]
            del wavestartlist[:]
            del waveendlist[:]
            del sentence[:]
