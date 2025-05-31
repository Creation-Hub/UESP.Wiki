import os
import datetime

# Timestamps
#---------------------------------------------

DATE_TIME_FORMAT = "%Y/%m/%d %I:%M:%S %p"
"""Format for date and time string as YYYY/MM/DD hh:mm:ss AM/PM."""


def generation_date() -> str:
    """Gets the current date and time."""
    dt = datetime.datetime.now()
    pretty_date = dt.strftime(DATE_TIME_FORMAT)
    return f"* GENERATED: {pretty_date}"


def script_date_modified(script_path:str) -> str:
    """Gets the last modified date of the source script file."""
    mod_time = os.path.getmtime(script_path)
    dt = datetime.datetime.fromtimestamp(mod_time)
    pretty_date = dt.strftime(DATE_TIME_FORMAT)
    return f"* PAPYRUS:   {pretty_date}"

# Writer
#---------------------------------------------

def write(file, script_path:str):
    """Writes meta data related to the generator and game files."""
    file.write(generation_date())
    file.write("\n")
    file.write(script_date_modified(script_path))
