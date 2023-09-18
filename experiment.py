#!/usr/bin/env python
import datetime
from pathlib import Path

import numpy as np
from psychopy import core, event, logging, sound, visual
from psychopy.hardware import keyboard

SUBJECT = 'Wellington'
TESTING = True # overrides SUBJECT if True
EXPERIMENT = 'retinotopic' # 'breathing', 'retinotopic', 'seven', 'images'
COUNTDOWN = True
JITTER_MAX_TIME = 2

if TESTING:
    SUBJECT='test'
    COUNTDOWN = False
    N_TRIALS = 2
    DURATION_REST = 2
    DURATION_STIM = 1
else:
    N_TRIALS = 6
    if EXPERIMENT == 'breathing':
        DURATION_REST = 30
        DURATION_STIM = 20
    elif EXPERIMENT == 'retinotopic':
        N_TRIALS = 10
        DURATION_REST = 15
        DURATION_STIM = 5
    else:
        DURATION_REST = 30
        DURATION_STIM = 30

COUNTDOWN_SECONDS = 3
DPATH_LOGS = Path('logs', SUBJECT)

# set up logging
DPATH_LOGS.mkdir(exist_ok=True, parents=True)
fpath_log = DPATH_LOGS / f'{EXPERIMENT}-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
logger = logging.LogFile(f=fpath_log, level=logging.ERROR)

#create a window
win = visual.Window(fullscr=True, monitor="testMonitor", units="deg")

# common stimuli
fixation = visual.GratingStim(win=win, size=0.2, pos=[0,0], sf=0, color='black')
beep = sound.Sound('./beep-07a.wav')

countdown_frames = [
    visual.TextStim(win=win, text=f'{COUNTDOWN_SECONDS - i}', pos=[0,0], depth=-1.0)
    for i in range(COUNTDOWN_SECONDS)
]

frames = []
if EXPERIMENT == 'breathing':
    inhale = visual.TextStim(win=win, text='Take a deep breath', pos=[0,0], depth=-1.0)
    hold_breath = visual.TextStim(win=win, text='Hold your breath', pos=[0,0], depth=-1.0)
    for i_trial in range(N_TRIALS):
        frames.extend([
            # name, frame, duration
            ('inhale', inhale, 3, False, None),
            ('hold_breath', hold_breath, DURATION_STIM, False, None),
            ('rest', fixation, DURATION_REST, False, None),
        ])
elif EXPERIMENT == 'seven':
    for i_trial in range(N_TRIALS):
        n = np.random.randint(1000)
        frames.extend([
            ('seven', visual.TextStim(win=win, text=f'Count backwards by 7s from: {n}', pos=[0,0], depth=-1.0), DURATION_STIM, False, n),
            ('rest', fixation, DURATION_REST, False, None),
        ])
elif EXPERIMENT == 'retinotopic':
    wedge_size = 180
    stim_size = (60,60)
    radial_cycles = 30
    angular_cycles = 20
    flicker_freq = 5 # in Hz
    fixation.color = 'red'

    wedge_starts = np.tile(np.arange(0, 360, wedge_size), N_TRIALS)
    # np.random.shuffle(wedge_starts)

    frames.append(('rest', fixation, DURATION_REST*2, False, None))
    for wedge_start in wedge_starts:
        # wedge_start = np.random.randint(360//wedge_size) * wedge_size 
        visible_wedge = (wedge_start, wedge_start + wedge_size)
        jitter_time = (np.random.rand() * 2) - 1
        print(f'jitter_time: {jitter_time}')
        frames.extend([
            (
                'retinotopic',
                (
                    visual.RadialStim(win=win, radialPhase=0, size=stim_size, radialCycles=radial_cycles, angularCycles=angular_cycles, visibleWedge=visible_wedge),
                    visual.RadialStim(win=win, radialPhase=0.5, size=stim_size, radialCycles=radial_cycles, angularCycles=angular_cycles, visibleWedge=visible_wedge),
                ),
                DURATION_STIM,
                flicker_freq,
                {'wedge_start': wedge_start, 'wedge_size': wedge_size, 'flicker_freq': flicker_freq},
            ),
            ('rest', fixation, DURATION_REST+jitter_time, False, None),
        ])
else:
    raise ValueError(f'Invalid experiment: {EXPERIMENT}')

kb = keyboard.Keyboard()

# countdown
if COUNTDOWN:
    for countdown_frame in countdown_frames:
        # next_flip = win.getFutureFlipTime(clock='ptb')
        # beep.play(when=next_flip)
        countdown_frame.draw()
        win.flip()
        core.wait(1)
        event.clearEvents()

# main
for name, frame_to_draw, frame_duration, flicker_freq, to_log in frames:

    next_flip = win.getFutureFlipTime(clock='ptb')
    beep.play(when=next_flip)

    if flicker_freq:
        frame_on, frame_off = frame_to_draw
        frame_on.draw()
        fixation.draw()
        flicker_start_time = win.flip()
        half_period = 0.5 * (1/flicker_freq)

        # flicker based on time (better to do frames but this is easier)
        i_frame = 0
        while core.getTime() < flicker_start_time + frame_duration:
            core.wait(half_period)
            i_frame += 1
            frame = frame_to_draw[i_frame % 2]
            frame.draw()
            fixation.draw()
            win.flip()

        to_log['n_flickers'] = i_frame
        logger.write(f'{name}\t{flicker_start_time}\t{to_log}\n')

    else:
        frame_to_draw.draw()
        flip_time = win.flip()
        logger.write(f'{name}\t{flip_time}\t{to_log}\n')

        core.wait(frame_duration)

    end_time = core.getTime()     

    if len(kb.getKeys()) > 0:
        break
    event.clearEvents()

logger.write(f'end\t{core.getTime()}\n')

#cleanup
win.close()
core.quit()
