#! /usr/bin/env python
# Time-stamp: <2018-03-21 14:34:02 cp983411>


import sys
import io
import os.path as op
import argparse
import csv

import expyriment.control
from expyriment import stimuli
from expyriment.misc import Clock

from queue import PriorityQueue

# constants (to be modified depending on the paradigm) 
WORD_DURATION = 400
PICTURE_DURATION = 1000
TEXT_DURATION = 3000
TOTAL_EXPE_DURATION = 20000 # 10 sec


# process command line options

parser = argparse.ArgumentParser()
parser.add_argument("--splash", help="displays a picture (e.g. containing instructions) before starting the experiment")

parser.add_argument("--rsvp-display-time",
                    type=int,
                    default=WORD_DURATION,
                    help="set the duration of display of single words \
                          in rsvp stimuli")
parser.add_argument("--picture-display-time",
                    type=int,
                    default=PICTURE_DURATION,
                    help="set the duration of display of pictures")
parser.add_argument("--text-display-time",
                    type=int,
                    default=TEXT_DURATION,
                    help="set the duration of display of pictures")
parser.add_argument('csv_files', nargs='+', action="append", default=[])

args = parser.parse_args()
splash_screen = args.splash
WORD_DURATION = args.rsvp_display_time
PICTURE_DURATION = args.picture_display_time
TEXT_DURATION = args.text_display_time
csv_files = args.csv_files[0]


exp = expyriment.design.Experiment(name="HiRes Experiment")
#expyriment.control.defaults.open_gl=1
expyriment.control.defaults.window_size=(1280, 1028)
expyriment.control.set_develop_mode(True)

#%

expyriment.control.initialize(exp)

kb = expyriment.io.Keyboard()
bs = stimuli.BlankScreen()
wm = stimuli.TextLine('Waiting for scanner sync (or press \'t\')')
fs = stimuli.FixCross()

events = PriorityQueue()  # all stimuli will be queued here


# load stimuli

mapsounds = dict()
mapspeech = dict()
maptext = dict()
mappictures = dict()
mapvideos = dict()

for listfile in csv_files:
    stimlist = csv.reader(io.open(listfile, 'r', encoding='utf-8'))
    bp = op.dirname(listfile)
    for row in stimlist:
        onset, stype, f = int(row[0]), row[1], row[2]
        if stype == 'sound':
            if not f in mapsounds:
                mapsounds[f] = stimuli.Audio(op.join(bp, f))
                mapsounds[f].preload()
            events.put((onset, 'sound', f, mapsounds[f]))
        elif stype == 'picture':
            if not f in mappictures:
                mappictures[f] = stimuli.Picture(op.join(bp, f))
                mappictures[f].preload()
            events.put((onset, 'picture', f, mappictures[f]))
            events.put((onset + PICTURE_DURATION, 'blank', 'blank', bs))
        elif stype == 'video':
            if not f in mapvideos:
                mapvideos[f] = stimuli.Video(op.join(bp, f))
                mapvideos[f].preload()
            event.put((onset, 'video', f, mapvideos[f]))
        elif stype == 'text':
            if not f in maptext:
                maptext[f] = stimuli.TextLine(f)
                maptext[f].preload()
            events.put((onset, 'text', f, maptext[f]))
            events.put((onset + TEXT_DURATION, 'blank', 'blank', bs))
        elif stype == 'rsvp':
            for i, w in enumerate(f.split()):
                if not w in maptext:
                    maptext[w] = stimuli.TextLine(w)
                    maptext[w].preload()
                events.put((onset + i * WORD_DURATION, 'text', w, maptext[w]))
            events.put((onset + (i + 1) * WORD_DURATION, 'blank', 'blank', bs))


#%

expyriment.control.start()


if not (splash_screen is None):
    splashs = stimuli.Picture(splash_screen)
    splashs.present()
    kb.wait_char(' ')

wm.present()  
kb.wait_char('t')  # wait for scanner TTL 
fs.present()  # clear screen, presenting fixation cross

a = Clock()

while not(events.empty()):
    onset, stype, id, stim = events.get()
    print('event {} {} @ {}'.format(stype, id, onset))
    if a.time > onset:
        print('...delayed @ {}'.format(a.time))  # TODO
    while a.time < (onset - 10):
        a.wait(10)
        k = kb.check()
        if k is not None:
            print('keypressed: {} @ {}'.format(k, a.time))
            exp.data.add([a.time, k])

    stim.present()

    k = kb.check()
    if k is not None:
        print('keypressed: {} @ {}'.format(k, a.time))
        exp.data.add([a.time, k])

    try:
        TOTAL_EXPE_DURATION
    except NameError:
        None
    else:
        if a.time > TOTAL_EXPE_DURATION:
            expyriment.control.stop_audiosystem()
            break


try:
    TOTAL_EXPE_DURATION
except NameError:
    None
else:
    while a.time < TOTAL_EXPE_DURATION:
        a.wait(100)

expyriment.control.end('Merci !', 2000)
