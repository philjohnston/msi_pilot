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
 
#Note to self: match degrees of visual angle to other studies

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
SOA_list= 4*[-40, -35, -30, -25, -20, -15, -10, -8, -5, -2, -1, 0, 1, 2, 5, 8, 10, 15, 20, 25, 30, 35, 40] # SOA in number of frames
all_responses = []
frame_length = 1/60 #length of frame in s (1/refresh rate)

#check for existing subject file
outputFileName = 'data' + os.sep + '1a_sub' + subj + '.csv' 
if os.path.isfile(outputFileName) :
    sys.exit("data for this subject already exists")
    
#create beep stimulus
beep = sound.Sound('2000', secs=0.01, stereo=False)
beep.setVolume(1)

#create flash stimulus
flash = visual.RadialStim(win, size = 0.3, radialCycles = 1, radialPhase = 1/2, 
                                angularPhase = 1/4, angularCycles = 1/2)

#create fixation
fixation = visual.TextStim(win, text = "+", color = "white", height = 0.075)

#run
for block in range(num_blocks):
    shuffle(SOA_list)
    
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
            
        core.wait(0.75)
        
        #collect response
        prompt = visual.TextStim(win, text = "Simultaneous?", height = 0.1, pos = (0, 0.25))
        key_prompt = visual.TextStim(win, text = "NO                      YES", height = 0.1, pos = (0, -0.25))
        prompt.draw()
        key_prompt.draw()
        win.flip()
        trialClock.reset()
        keys = event.waitKeys(timeStamped=trialClock, keyList = ['a', 'l', 'escape'], maxWait = 2)
        
        if keys == None: # check for no response
            keys=[['NaN', 'NaN']]
        elif keys[0][0] == 'escape': #change this so data is saved on force quit (or give second prompt)
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

