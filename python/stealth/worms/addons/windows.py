import os

base_dirs = [
    r"C:\ProgramData",
    os.path.expandvars(r"%USERPROFILE%\AppData\Roaming"),
    os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow"),
    os.path.expandvars(r"%USERPROFILE%\AppData\Local")
]