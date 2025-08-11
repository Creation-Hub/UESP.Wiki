@ECHO off

ECHO.
ECHO Moving into 'source\' folder.
ECHO ------------------------------
CD source
ECHO "CD:" '%CD%'


REM Install individual packages first (in dependency order).

ECHO.
ECHO Installing %CD%\sharp\pyproject.toml
ECHO ------------------------------
pip install -e sharp

ECHO.
ECHO Installing %CD%\papyrus\pyproject.toml
ECHO ------------------------------
pip install -e papyrus

ECHO.
ECHO Installing %CD%\wiki\pyproject.toml
ECHO ------------------------------
pip install -e wiki

ECHO.
ECHO Installing %CD%\scribe\pyproject.toml
ECHO ------------------------------
pip install -e scribe

ECHO.
ECHO Install developer dependencies.
pip install -e scribe[dev]


ECHO.
ECHO Return to original directory.
ECHO ------------------------------
CD ..
ECHO "CD:" '%CD%'


ECHO.
ECHO Verifying all packages are installed.
ECHO ------------------------------
pip list | findstr -i "sharp papyrus wiki scribe"


ECHO.
ECHO Testing console main script entry point.
ECHO ------------------------------
scribe --help
