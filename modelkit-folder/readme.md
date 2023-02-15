# *Modelkit Caboodle*

*Modelkit Caboodle* packages together everything you need to use *Modelkit* to perform energy modeling with the *EnergyPlus* simulation engine. The package includes:

- *Modelkit* framework and command-line tools
- *Modelkit for EnergyPlus* library and command-line tools
- Ruby 2.0 interpreter and standard libraries
- Ruby gem dependencies
- Net Zero Template library for *EnergyPlus*
- Example projects for *Modelkit*.

Because *Modelkit Caboodle* includes its own Ruby interpreter **you do not need to have Ruby installed to use *Modelkit***. You can download installers here:

[Modelkit Caboodle installer for Windows](https://download.bigladdersoftware.com/?ref=modelkit-caboodle-latest-win)<br>
[Modelkit Caboodle installer for Mac](https://download.bigladdersoftware.com/?ref=modelkit-caboodle-latest-mac)

You should be able to type `modelkit` at the command-line prompt to verify that it installed correctly. (NOTE: The Windows installer adds *Modelkit Caboodle* to your PATH environment variable.)

## Development Environment

These instructions are intended to help you set up a development environment for working on *Modelkit Caboodle* and any of its components (e.g., *Modelkit*, *Modelkit for EnergyPlus*, etc.).

Make sure the following required software is installed before proceeding:

### Windows

- ***Ruby 2.0.0*** - Install 32-bit version using [*RubyInstaller*](http://rubyinstaller.org/downloads/).
- ***Git*** - Install [*msysgit* command-line interface](http://git-scm.com/download/win)
  - `C:\Program Files (x86)\Git\cmd` (or similar) must be added to the [PATH environment variable](http://www.computerhope.com/issues/ch000549.htm).
- ***Inno Setup*** - Install [*Inno Setup*](http://www.jrsoftware.org/isdl.php) if you need to build the installer program.

### Mac

- ***Ruby 2.0.0*** - We recommend using a version manager such as [*rbenv*](https://github.com/rbenv/rbenv) or [*RVM*](https://rvm.io/rvm/install) to install Ruby rather than using your system Ruby.
- ***Git*** - Should already be installed on your system.

## Build Process

The development environment uses Ruby's [*Rake*](https://github.com/ruby/rake#description) build automation tool. To execute a command with *Rake*, open a console/shell window and navigate to the root directory of the repository where you will find `rakefile.rb`.

From the shell window, type:

    rake

The `rake` command should kick off the build process. If this is your first time building *Modelkit*, the program will prompt for your [Bitbucket](https://bitbucket.org) username and password in order to clone the dependent repositories.

To make changes to *Modelkit*, only edit the files under the source directory. When you are ready to test your changes, type:

    rake compile

The compile process copies files to the build directory. Use the files under the build directory for testing only. (NOTE: The build output files are set to read-only so that you don't try to edit them accidentally. Make your changes in the source, and then do `rake compile`.)

To see the other available *Rake* tasks, type:

    rake --tasks

Or simply:

    rake -T

## Copyright

All files copyright (c) 2011-2020 Big Ladder Software LLC. All rights reserved.
