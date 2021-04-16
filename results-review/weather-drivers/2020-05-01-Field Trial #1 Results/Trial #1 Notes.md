# Field Trial Description

First iteration of results from participating tools. Results for all tools were shared by Tim McDowell on April 27, 2020.

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
