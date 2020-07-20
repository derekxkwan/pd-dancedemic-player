# pd-dancedemic-player
a video/osc player for art-a-hack 2020

## requirements
- Gem
- Pure Data (any recent version)
- Python 3

## First Steps
- the osc save data comes in a format where essentially every line is an osc bundle. To conver this to Pd's structure format, run the included python script with `python dd-osctopdstruct.py <file to convert>`. This creates a `.pdstruct` extension file of the same name in the same folder as the original text file.

## Getting the video working in Pd
- You need Pd's Gem, which is installable from within Pd by `Help > Find externals` and searching for Gem. There have been some issues on platforms with running Gem, but I could never get the alternative (Ofelia) to work properly on my machine.

## Usage
- the player patch is `dancedemic-player.pd`. Make sure to hit `clear data` and don't save after each use. It doesn't matter much, but Pd tends to save the loaded data and with a 6 minute video, that's about a 1MB of osc data.
- I've included a OSC receiver to complement the player patch's OSC sending capabilities in `dancedemic-oscrcv.pd`. This patch populates Pd's sends with the incoming OSC data from the Pd player. Will need to work on compatibility with the actual OSC data from the Art-a-Hack project once I get more info about that. Due to Pd's flat and global namespacing, these sends are accessible in even separate Pd patches! (so don't open multiple copies of the same patch).
- Please keep the relative file structure intact (don't move things around). These patches rely on some abstractions I've included in `util` and won't know where to look otherwise...
## Further Notes
- Everything else should be relatively self-explanatory. There may be some issues with sync between the reported data vs the scrolling seek bar in the graphed data vs the displayed video that I'll have to work on as time goes on...

