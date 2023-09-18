# data-experiments

Experimental protocols for collecting fNIRS data.

## Requirements

* Make a new Python/`conda` environment with Python 3.8
* `pip install psychopy` (can take some time)

## Scripts

* `experiment.py`: Run an experiment. See variables in all caps for settings. Will write a log file with timing information for each frame change.
    * `EXPERIMENT='images'` is not implemented yet, but it should be a variation of `'breathing'` or `'seven'` with images instead of text prompts.
    * **IMPORTANT**: When starting the script, make sure to press "Mark Event" on the `brainscanner-matlab` app. This is because data from the MATLAB app only uses relative timestamps (i.e. time from the start of the recording), and we need to match the times from the Psychopy script to the fNIRS data.
* `convert_log_to_events.py`: Write a TSV file that converts a logfile to the `events.tsv` format expected by Homer3. `START_TIME` should be set to the time in the fNIRS recording when the `experiment.py` script was started.
