# track_database

A Python package to gather some default Formula Student tracks as well as some 
utility functions to import/export them in CSV format and to create new custom tracks.

## Installation

You can install this package using `pip` after either cloning this repo or addding 
it as a git submodule to your project. If you have clone access to this repo, then 
you could also do it direclty with: 
```
$ pip3 install git+git://github.com/FormulaStudent/track_database.git
```

## Package description
The package has the following modules: 
- `io`: defines functions `load_track()` and `export_track()` to load and export tracks 
  in CSV format.
- `constants.py`: defines the labels of the CSV columns associated to the center 
  line points, the left and right cones. 
- `primitives.py`: defines some useful functions to create tracks, such as `line()` 
  and `circle()`.
- `tracks.py`: defines some more complex functions to create fresh tracks (not 
  imported from a file) such as skidpad, acceleration track, etc. These tracks can 
  be created with a scale factor to be adapted for different car sizes (in 
  particular for Minimercury).
- `defaults.py`: defines functions to import default FS tracks (acceleration, 
  skidpad and a complete FS track for autocross/trackdrive at 1:1 scale).
