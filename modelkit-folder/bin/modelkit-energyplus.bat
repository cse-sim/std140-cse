@ECHO OFF
SETLOCAL
SET root=%~dp0..
SET ruby=%root%\ruby\ruby-2.0.0
SET lib=%root%\lib\rubygems\gems\modelkit-energyplus-0.3.0
SET GEM_HOME=%root%\lib\rubygems
SET GEM_PATH=%root%\lib\rubygems;%root%\vendor\rubygems
"%ruby%\bin\ruby.exe" "%lib%\bin\modelkit-energyplus" %*
EXIT /B %ERRORLEVEL%
