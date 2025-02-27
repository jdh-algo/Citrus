import os
import sys
import json
from pathlib import Path

from dynaconf import Dynaconf

_BASE_DIR = Path(__file__).parent


D_PROMPT_CONFIG = {}

for fname in os.listdir(Path(__file__).parent):
    if not fname.endswith('.prompt'):
        continue
    with open(os.path.join(Path(__file__).parent, fname)) as f:
        D_PROMPT_CONFIG[fname] = f.read()
