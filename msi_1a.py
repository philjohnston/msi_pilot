# msi pilot 1a
# Nov 8 2018
# To determine individual temporal binding windows 
# and choose SOAs for main run 

import numpy as np
import pandas as pd
import os, sys
from psychopy import visual, core, event, gui, logging, sound
from random import shuffle
import matplotlib.pyplot as plt
 
#To do: match degrees of visual angle to other studies. Generate logfile? Remove esc key for final run?

#system setup
framerate = 100 #For debugging purposes only. Must be 100 for data collection 

if framerate != 100:
    print("Warning: framerate not set to 100 Hz")

frame_length = 1/framerate #length of frame in s (1/frame rate)

#get Subject ID
subgui = gui.Dlg() 
subgui.addField("Subject ID:")
subgui.show()
subj = subgui.data[0]


#setup
win = visual.Window(fullscr=True, allowGUI=False, color="black", screen=1, units='height', waitBlanking=True)
trialClock = core.Clock()
expClock = core.Clock()
num_blocks = 5
SOA_list= 4*[-40, -35, -30, -2-
-5, -20, -15, -10, -8, -5, -2, -1, 0, 1, 2, 5, 8, 10, 15, 20, 25, 30, 35, 40] # SOA (in number of frames)
all_responses = []


#check for existing subject file
outputFileName = 'data' + os.sep + '1a_sub' + subj + '.csv' 
if os.path.isfile(outputFileName) :
    sys.exit("Data for this subject already exists")

#check refresh rate
actual_framerate = win.getActualFrameRate(nIdentical=100, nMaxFrames=1000,
    nWarmUpFrames=10, threshold=1)
if actual_framerate < framerate - 0.1 or actual_framerate >  framerate + 0.1:
    sys.exit("Expected refresh rate: " + str(framerate) + ". Actual rate: " + str(actual_framerate))

#create beep stimulus
beep = sound.Sound('3500', secs=0.01, stereo=False)
beep.setVolume(1)

#create flash stimulus
flash = visual.RadialStim(win, size = 0.3, radialCycles = 1, radialPhase = 1/2, 
                                angularPhase = 1/4, angularCycles = 1/2)

#create fixation
fixation = visual.TextStim(win, text = "+", color = "white", height = 0.075)

#instructions
instructions = visual.TextStim(win, text = """You will hear a beep and see a flash. When prompted, please use the left and right arrow keys to report whether they occur simultaneously or not. Press any key to begin. 
                                                        ← = NO              → = YES""", height = 0.075, pos = (0, 0)) #response keys will be counterbalanced in final experiment
start_prompt = visual.TextStim(win, text = "Press any key to begin", height = -0.075)
instructions.draw()
win.flip()
event.waitKeys()

block_count = 0
#run
for block in range(num_blocks):
    shuffle(SOA_list)
    block_count += 1
    
    if block_count != 1:
        
        #prompt any key
        start_prompt = visual.TextStim(win, text = "Press any key to begin", height = 0.075)
        start_prompt.draw()
        win.flip()
        event.waitKeys()
    
    trial_count = 0
    
    for SOA in SOA_list:
        
        trial_count += 1
        beep.stop() #reset beep
        
        #jitter initial fixation
        fixation.draw()
        win.flip()
        core.wait(np.random.uniform(1, 1.5))
        fixation.draw()
        win.flip()
        core.rush(True) #give psychopy priority during presentation
        
        if SOA < 0: #auditory then visual
            
            #beep
            beep.play()
            fixation.draw()
            win.flip()
            trialClock.reset()
            
            #SOA
            for frameN in range(-1*SOA-1):
                fixation.draw()
                win.flip()
            
            #flash
            flash.draw()
            fixation.draw()
            win.flip()
            
            print("SOA Expected: " + str(-1*SOA*frame_length) + #test
                    " Actual: " + str(trialClock.getTime()) + 
                    " Error: " + str(trialClock.getTime() - (-1*SOA*frame_length)))
            fixation.draw()
            win.flip()
            
        elif SOA == 0: #simultaneous
            flash.draw()
            fixation.draw()
            win.flip()
            beep.play()
            fixation.draw()
            win.flip()
            
        else: #visual then auditory
            
            #flash
            flash.draw()
            fixation.draw()
            win.flip()
            fixation.draw()
            win.flip()
            trialClock.reset()
            
            #SOA
            for frameN in range(SOA):
                fixation.draw()
                win.flip()
            
            #beep
            print("SOA Expected: " + str(SOA*frame_length) + #test
            " Actual: " + str(trialClock.getTime()) + 
            " Error: " + str(trialClock.getTime() - (SOA*frame_length)))
            beep.play()
            
        core.rush(False)
        core.wait(0.75)
        
        #collect response
        prompt = visual.TextStim(win, text = "Simultaneous?", height = 0.1, pos = (0, 0.25))
        key_prompt = visual.TextStim(win, text = "NO                      YES", height = 0.1, pos = (0, -0.25))
        prompt.draw()
        key_prompt.draw()
        win.flip()
        trialClock.reset()
        keys = event.waitKeys(timeStamped=trialClock, keyList = ['left', 'right', 'escape', 'backspace'], maxWait = 2)
        
        if keys == None: # check for no response
            keys=[['NaN', 'NaN']]
        elif keys[0][0] == 'escape': #data saves on quit
            win.close()
            df = pd.DataFrame(all_responses)
            df.columns = ['subj', 'block', 'trial', 'SOA', 'resp', 'rt']
            df.to_csv(outputFileName)
            core.quit()
        elif keys[0][0] == 'backspace': #data doesn't save (for debugging)
            win.close()
            core.quit()
            
        all_responses.append([subj, block + 1, trial_count, SOA, keys[0][0], keys[0][1]])
        win.flip()
        core.wait(0.75) #ITI

win.close()

print(expClock.getTime())
df = pd.DataFrame(all_responses)
df.columns = ['subj', 'block', 'trial', 'SOA', 'resp', 'rt']
df.to_csv(outputFileName)

