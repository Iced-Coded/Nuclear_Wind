from cx_Freeze import setup, Executable

setup(
    name = "NuclearWind",
    version = "1.0a",
    description = "DEMO",
    executables = [Executable("main.py")],
    requires = ["pygame", "pygame_gui"],
    options = {
        "build_exe": {
            "include_files": [
                "data",
                "snow.png",
                "theme.json",
                "log.txt"
            ],
            "zip_include_packages": [
                "pygame",
                "pygame_gui"
            ]
        }
    }
)