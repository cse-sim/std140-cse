# Standard 140 Test Suites for CSE

Section 5 - Building Thermal Envelope and Fabric Load Tests
Weather Drivers - Weather File Processing

## Requirements

- [Ruby 2.0.0-p645](https://dl.bintray.com/oneclick/rubyinstaller/rubyinstaller-2.0.0-p645.exe) (must add binaries to PATH): To run rake.
- [Modelkit Catalyst](https://bigladdersoftware.com/projects/modelkit/): To generate input files from templates
- [Python 3.X (Anaconda distribution suggested)](https://www.anaconda.com/distribution/) (must add python to PATH): To process results and create report
    - `pip install mako`

## Running tests

Type `poetry shell`, then
type `rake` from the top level directory.
