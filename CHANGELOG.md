# v3.7.1 

fixed order of points in random track generation and regenerated tracks 1 to 5 (not the same anymore)

# v3.7.0

added support for random track generation as well as 5 new tracks

# v3.6.0

added new file to export csv track as a .world file for the baudousim

# v3.5.0

added new (small) autoX track for Vaudoise event

# v3.4.0

able to load unregistered tracks now

# v3.3.0

added VSV_XS variantn and removed big orange cones from all VSV tracks

# v3.2.1

corrected positions of big_orange cones in VSV_XL

# v3.2.0

added VSV and VSV_XL track (U-turns and acceleration tests)

# v3.1.0

added new track (oval) for the tests on 21/05/2023

# v3.0.3

added `COLCON_IGNORE` file to ignore this package in colcon builds (for brains repo)

# v3.0.2

removed two misplaced points on the center line of the acceleration track

# v3.0.1

Renamed all data files to the format `<track_name>_cones.csv` and `<track_name>_center_line.csv`
to facilitate the extraction of the track name from `fsds_client`.

# v3.0.0

Integrated the FSDS tracks and changed the way the tracks and cones are stored
and interfaced. Now each track is stored using only two files (one for the cones
positions and one for the center line points and the track widths).

# v2.1.1

Changed the initial point to have initial heading angle=pi/2 and to avoid weird stuff in interpolation.

# v2.1.0

Added modified skidpad tracks to have short version (only one times each loop)
as well ass the full version (two times each loop).
They can be imported with `load_default_skidpad()` and `load_default_short_skidpad()`

# v2.0.1

Fixed import of git deps in `setup.py`

# v2.0.0

updated everything to match `python_boilerplate` v2.0.1 and removed ReferencePath tests

# v1.1.0

- changed data storage to include left and right widths
- the `center_line`, `left_cones` and `right_cones` are now returned in column major
  format, i.e. a row corresponds to a single point.
