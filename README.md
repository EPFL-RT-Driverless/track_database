# track_database

A Python package to gather some default Formula Student tracks as well as some
utility functions to import/export them in CSV format and to create new custom
tracks.
These tracks are stored in a compatible format with FSDS to be loadable at
runtime.

## Installation

You can install this package using `pip` after either cloning this repo or addding
it as a git submodule to your project. If you have clone access to this repo, then
you could also do it direclty with:
```
$ pip3 install git+git://github.com/FormulaStudent/track_database.git
```

## Package description
The package has the following modules:
- `tracks.py`: defines the `Track` class (a *Plain Old Data Structure*, aka PODS,
  containing the blue, yellow, big orange, small orange, left and right cones
  positions, the center line points and the track widths) and the available tracks.
- `primitives.py`: defines some useful functions to create tracks, such as
- `line()`, `circle()` and `circular_arc()`.
- `utils.py`: defines several utility functions (e.g. IO functions to save and
  load track files).

## Track file format description
A track with name `track_name` is stored in the folder [`track_database/data`](track_database/data/)
as a folder named `track_name` containing the following files:
- `track_name_cones.csv`: contains the cones positions in a format compatible with FSDS to
  be loadable at runtime: `cone_type,X,Y,Z,std_X,std_Y,std_Z,right,left`.
  The `cone_type` is either `blue`, `yellow`, `big_orange` or `small_orange`.
  The `right` and `left` columns are binary (0 or 1) values indicating if the cone
  is on the right or left side of the track.
  `std_X`, `std_Y` and `std_Z` are the standard deviations of the cone position,
  usually 0.
- `track_name_center_line.csv`: contains the center line points in the following format:
  `x,y,right_width,left_width`.
