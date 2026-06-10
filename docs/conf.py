from importlib.metadata import version as _version

project = "drf-choices-mixin"
version = _version("drf-choices-mixin")
author = "Denny Biasiolli"

extensions = ["myst_parser"]
source_suffix = {".md": "markdown"}

html_theme = "furo"
html_title = "drf-choices-mixin"

exclude_patterns = ["_build"]
