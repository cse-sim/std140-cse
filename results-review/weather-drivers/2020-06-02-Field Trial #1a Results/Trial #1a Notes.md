# Field Trial Description

Revision of first iteration of results from participating tools. Tim McDowell shared results from all tools on June 1, 2020 with statistical measurements (mean bias error, root mean square error, etc.) between participating tools and actual weather files.

# Changes from previous iteration

- Tim McDowell provided updated weather files (WD100.tmy3, e.g.) with modified albedo to match ground reflectance values in the test suite.
- Updated CSE inputs to match these albedo values as well.
- Fixed subhourly outputs for incident solar radiation to remove subhour duration multiplier.
- Updated CSE EXE from 0.861.1 to 0.868.1.

# Issues with CSE Results

### Omitted Test Results

Some results were requested by test case description, but CSE does not currently allow output of:
- outdoor air relative humidity (only zone air relative humidity)
- opaque cloud cover (only total cloud cover)

**SOLUTION**: add outdoor air RH as a new output, but not opaque cloud cover (needs to come from weather file)

### Anomalous Test Results

Some results were requested by test case description, and CSE has behavior that differs from most other tools:
- station pressure and outdoor air density (CSE currently uses elevation of the building site to calculate a fixed value for both outputs)

**SOLUTION**: no change required, applying varying station pressure and outdoor air density will have low impact on other air state parameters

- hourly total, beam, and diffuse solar radiation incident on each surface (CSE currently only generates these at subhourly frequency)

**SOLUTION**: no change required, can sum subhourly outputs from CSE using scripts or spreadsheets to calculate hourly values
