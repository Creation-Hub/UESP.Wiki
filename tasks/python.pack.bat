REM Install individual packages first (in dependency order).
pip install -e source/sharp
pip install -e source/papyrus
pip install -e source/wiki
pip install -e source/scribe

REM Install dev dependencies.
pip install -e source/scribe[dev]

REM Verify all packages are installed.
pip list | findstr -i "sharp papyrus wiki scribe"
