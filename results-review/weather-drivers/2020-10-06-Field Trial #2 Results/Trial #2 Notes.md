# Field Trial Description

Second iteration of results from participating tools. Tim McDowell shared results from all tools on October 6, 2020. 

# Changes from previous iteration

- Tim McDowell requested subhourly outputs for full year instead of multiple aggregations (subhourly, hourly, etc.) over specific days.
- Added subhourly outputs for:
  - Outdoor air relative humidity
  - Outdoor air dewpoint temperature
  - Outdoor air humidity ratio
  - Outdoor air wetbulb temperature
  - Wind speed
  - Wind direction
  - Station pressure
  - Total cloud cover
  - Sky temperature
- Added hourly outputs for:
  - Outdoor air relative humidity
- Set exterior surface absorptance to 1 for all surfaces.
- Updated CSE EXE from 0.868.1 to 0.875.0.

# Issues with CSE Results

### Omitted Test Results

Some results were requested by test case description, but CSE does not currently allow output of:
- opaque cloud cover (only total cloud cover)

**SOLUTION**: opaque cloud cover needs to come from weather file

### Anomalous Test Results

Some results were requested by test case description, and CSE has behavior that differs from most other tools:
- constant station pressure and outdoor air density (CSE currently uses elevation of the building site to calculate a fixed value for both outputs)

**SOLUTION**: no change required, applying varying station pressure and outdoor air density will have low impact on other air state parameters

- hourly wind direction and total cloud cover have same hourly value applied to all subhours within the hour

**SOLUTION**: no change required, just know that subhourly values won't vary within the same hour

In addition to these omitted and anomalous results, Tim specifically mentioned the following for CSE (Program B) compared to other participating tools:

Program B
Some potential issues for discussion we noticed (you may notice others):
- Solar radiation – both direct/diffuse split and tilted surface radiation show differences from the other programs
- Relative humidity sometimes differs
- Hourly integrated total horizontal radiation – daily plots (WD100 9/6, WD200 8/26, WD300 2/7, WD300 8/13, WD400 7/1, WD500 3/1, WD500 9/14)
- Hourly integrated diffuse horizontal radiation – daily plots (WD100 7/14, WD100 9/6, WD200 8/26, WD300 2/7, WD300 8/13, WD400 7/1, WD500 3/1, WD500 9/14)

Tim thought CSE differences were caused by using Hay & Davies model vs. Perez model and shared results where TRNSYS used both sky models (email dated Oct 15, 2020). These results are saved in *2020-10-15-TRNSYS-CSE_Charts* folder.