import pathlib
from enum import Enum

SRC_PATH = pathlib.Path(__file__).parent.parent
TEMPLATES_PATH = str(SRC_PATH.parent.absolute()) + "/templates"
GADGETS_PATH = str(SRC_PATH.absolute()) + "/gadgets/"
OUTPUT_PATH = str(SRC_PATH.parent.absolute()) + "/out/"
EXPERIMENTS_PATH = str(SRC_PATH.parent.absolute()) + "/experiments/"
REPO_NAME = "gadgets_repo"

class FW_MODES(Enum):
    COMPILE_ONLY = 1
    WEAVE_ONLY = 2
    FULL = 3
