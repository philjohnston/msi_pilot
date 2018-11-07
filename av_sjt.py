import numpy as np
import pandas as pd
import os, sys
from psychopy import visual, core, event, gui, logging, sound
from random import shuffle

SOA_20 = [-250, -150, -80, -50, -20, -10, 0, 10, 20, 50, 80, 150, 250] #create and shuffle list of SOAs
SOA_80 = [-300, -200, -100, 100, 200, 300]
SOA_list = 2*SOA_20 + 8*SOA_80

num_blocks = 3
all_responses = []

win = visual.Window(fullscr=True, allowGUI=False, color="black", screen = 1, units = 'height')
trialClock = core.Clock()
expClock = core.Clock()



subgui = gui.Dlg() #get Subject ID
subgui.addField("Subject ID:")
subgui.show()
subj = subgui.data[0]

outputFileName = 'data' + os.sep + 'sub' + subj + '.csv' #check for existing subject file
if os.path.isfile(outputFileName) :
    sys.exit("data for this subject already exists")

for block in range(num_blocks):
    shuffle(SOA_list)
    start_prompt = visual.TextStim(win, text = "Press any key to begin", height = 0.075) #prompt any key to begin
    start_prompt.draw()
    win.flip()
    event.waitKeys()
    trial_count = 0
    
    for SOA in SOA_list:
        trial_count += 1
        beep = sound.Sound('2000', secs=0.01, stereo=True)
        beep.setVolume(1)
        flash = visual.RadialStim(win, size = 0.3, radialCycles = 1, radialPhase = 1/2, 
                                        angularPhase = 1/4, angularCycles = 1/2)
        fixation = visual.TextStim(win, text = "+", color = "white", height = 0.075)
        fixation.draw()
        win.flip()
        core.wait(np.random.uniform(1, 1.5))
        
        if SOA < 0:
            beep.play()
            core.wait(-1*SOA/1000) # SOA
            flash.draw()
            fixation.draw()
            win.flip()
            fixation.draw()
            core.wait(0.016) #change to 0.01 if using a 100 hz monitor
            win.flip()
            
        else:
            flash.draw()
            fixation.draw()
            win.flip()
            fixation.draw()
            core.wait(0.016)
            win.flip()
            core.wait(SOA/1000) #SOA
            beep.play()
            
        core.wait(0.75) #ITI
        prompt = visual.TextStim(win, text = "Simultaneous?", height = 0.1, pos = (0, 0.25))
        key_prompt = visual.TextStim(win, text = "NO                      YES", height = 0.1, pos = (0, -0.25))
        prompt.draw()
        key_prompt.draw()
        win.flip()
        trialClock.reset()
        keys = event.waitKeys(timeStamped=trialClock, keyList = ['a', 'l'], maxWait = 2)
        
        if keys == None: # check for no response
            keys=[['NaN', 'NaN']]
            
        all_responses.append([subj, block + 1, trial_count, SOA, keys[0][0], keys[0][1]])
        win.flip()
        core.wait(0.75)
        
print(expClock.getTime())
df = pd.DataFrame(all_responses)
df.columns = ['subj', 'block', 'trial', 'SOA', 'resp', 'rt']
df.to_csv(outputFileName)

